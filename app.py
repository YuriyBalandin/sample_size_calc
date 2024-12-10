import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm

st.set_page_config(page_title="A/B Test Sample Size Calculator", layout="wide")

st.title("A/B Test Sample Size Calculator")
st.markdown("This app calculates the required sample size for different metric types.")
st.markdown("For multiple groups (>2), a Bonferroni correction is applied to the significance level.")

metric_type = st.radio(
    "Select the type of metric:",
    ["Continuous metric", "Conversion (binomial)", "Ratio metric"]
)

st.sidebar.header("Test Parameters")
alpha = st.sidebar.number_input("Significance level (alpha)", value=0.05, format="%.4f")
power = st.sidebar.number_input("Power (1 - beta)", value=0.8, format="%.2f")
beta = 1 - power
n_groups = st.sidebar.number_input("Number of groups (including control)", min_value=2, value=2)

# Apply Bonferroni correction if multiple groups
comparisons = n_groups - 1
if comparisons > 1:
    alpha_eff = alpha / comparisons
else:
    alpha_eff = alpha

z_alpha = norm.ppf(1 - alpha_eff/2)
z_beta = norm.ppf(1 - beta)

st.write("### Baseline Metric Parameters")

if metric_type == "Continuous metric":
    mu = st.number_input("Baseline mean (μ)", value=100.0)
    std = st.number_input("Baseline std (σ)", value=15.0)
    mde_values = st.text_input("Enter MDE values (absolute difference), separated by commas", "5,10,20")
    mde_list = [float(x.strip()) for x in mde_values.split(",") if x.strip()]
    daily_users = st.number_input("Average number of users per day", value=1000)

    results = []
    for delta in mde_list:
        # Formula for continuous:
        # n per group = 2 * ((z_alpha + z_beta)*std/delta)^2
        n_per_group = 2 * ((z_alpha + z_beta)*std/delta)**2
        n_total = np.ceil(n_per_group * n_groups)
        days = n_total / daily_users
        rel_effect = (delta/mu)*100
        results.append({
            "MDE (absolute)": delta,
            "MDE (relative %)": f"{rel_effect:.2f}",
            "Total Sample Size": int(n_total),
            "Sample Size per Group": int(np.ceil(n_per_group)),
            "Duration (days)": f"{days:.2f}"
        })

    df = pd.DataFrame(results)
    st.write("## Results")
    st.dataframe(df)

elif metric_type == "Conversion (binomial)":
    p = st.number_input("Baseline conversion rate (p)", min_value=0.0, max_value=1.0, value=0.1, format="%.3f")
    mde_values = st.text_input("Enter MDE values (absolute difference in decimal), separated by commas", "0.02,0.05")
    mde_list = [float(x.strip()) for x in mde_values.split(",") if x.strip()]
    daily_users = st.number_input("Average number of users per day", value=1000)

    results = []
    for d in mde_list:
        p_t = p + d
        p_pooled = (p + p_t)/2
        numerator = z_alpha*np.sqrt(2*p_pooled*(1-p_pooled)) + z_beta*np.sqrt(p*(1-p)+p_t*(1-p_t))
        n_per_group = 2 * (numerator/d)**2
        n_total = np.ceil(n_per_group * n_groups)
        days = n_total / daily_users
        rel_effect = (d/p)*100 if p > 0 else np.nan
        results.append({
            "MDE (absolute)": d,
            "MDE (relative %)": f"{rel_effect:.2f}" if p > 0 else "N/A",
            "Total Sample Size": int(n_total),
            "Sample Size per Group": int(np.ceil(n_per_group)),
            "Duration (days)": f"{days:.2f}"
        })

    df = pd.DataFrame(results)
    st.write("## Results")
    st.dataframe(df)

elif metric_type == "Ratio metric":
    x_mean = st.number_input("X mean (numerator)", value=200.0)
    x_std = st.number_input("X std (numerator)", value=50.0)
    y_mean = st.number_input("Y mean (denominator)", value=100.0)
    y_std = st.number_input("Y std (denominator)", value=20.0)

    R0 = x_mean / y_mean
    var_R = (R0**2) * ((x_std**2)/(x_mean**2) + (y_std**2)/(y_mean**2))
    sigma_R = np.sqrt(var_R)

    mde_values = st.text_input("Enter MDE values (absolute change in ratio), separated by commas", "0.2,0.4")
    mde_list = [float(x.strip()) for x in mde_values.split(",") if x.strip()]
    daily_users = st.number_input("Average number of users per day", value=1000)

    results = []
    for delta in mde_list:
        # n per group = 2 * ((z_alpha+z_beta)*sigma_R/delta)^2
        n_per_group = 2 * ((z_alpha + z_beta)*sigma_R/delta)**2
        n_total = np.ceil(n_per_group * n_groups)
        days = n_total / daily_users
        rel_effect = (delta/R0)*100
        results.append({
            "MDE (absolute)": delta,
            "MDE (relative %)": f"{rel_effect:.2f}",
            "Total Sample Size": int(n_total),
            "Sample Size per Group": int(np.ceil(n_per_group)),
            "Duration (days)": f"{days:.2f}"
        })

    df = pd.DataFrame(results)
    st.write("## Results")
    st.dataframe(df)

st.markdown("---")
st.markdown("**Note:** For multiple groups, Bonferroni correction is applied to alpha.")
