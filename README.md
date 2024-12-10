# A/B Test Sample Size Calculator

This repository contains a Streamlit-based web application to quickly calculate the required sample size for A/B tests across various metric types. The app supports:

- **Continuous Metric** (e.g., revenue, session length)
- **Binary Conversion Metric** (e.g., click-through rate, conversion rate)
- **Ratio Metric** (e.g., ARPU = Revenue / Users, or any ratio of two metrics)

The tool calculates and displays the sample size needed for detecting a given Minimum Detectable Effect (MDE), considering statistical significance and power. It also accounts for multiple groups by applying a Bonferroni correction to the significance level.

## Features

1. **Interactive Web UI**:  
   Built with [Streamlit](https://streamlit.io/) for a quick, responsive, and user-friendly interface.

2. **Multiple Metric Types**:  
   Choose from Continuous, Conversion (Binomial), and Ratio metrics.

3. **Adjustable Test Parameters**:  
   Set the significance level (`alpha`), power (`1 - beta`), and number of groups.

4. **Bonferroni Correction**:  
   For tests with more than two groups, the app automatically applies Bonferroni correction to maintain appropriate family-wise error rates.

5. **Flexible Inputs**:  
   - For Continuous metrics: Set baseline mean and standard deviation.  
   - For Conversion metrics: Set a baseline conversion rate and detect absolute increases.  
   - For Ratio metrics: Provide means and standard deviations for numerator and denominator.

6. **Tabular Output**:  
   Results are displayed in a pandas DataFrame, making it easy to review, compare, and export:
   - Absolute MDE
   - Relative MDE (%)
   - Total Sample Size
   - Per-Group Sample Size
   - Estimated Test Duration (days), based on user-provided daily traffic.

## Getting Started

### Prerequisites

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)
- [Streamlit](https://docs.streamlit.io/library/get-started/installation)
- [numpy](https://numpy.org/)
- [pandas](https://pandas.pydata.org/)
- [scipy](https://scipy.org/)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sample_size_calc.git
   cd sample_size_calc
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Unix-based systems
   # or
   venv\Scripts\activate  # For Windows
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

Run the Streamlit app locally:

```bash
streamlit run app.py
```

This will open a local URL (usually http://localhost:8501/) where you can interact with the calculator.

## Usage

1. Select the metric type (Continuous, Conversion, or Ratio) from the main page.
2. Enter the baseline parameters (mean/std for continuous, conversion rate for binomial, or numerator/denominator metrics for ratio).
3. Specify test parameters in the sidebar:
   - Significance level (alpha)
   - Power (1 - beta)
   - Number of groups
   - Daily traffic (to estimate test duration)
4. Input one or multiple MDE values (comma-separated).
5. The results table will dynamically update to show required sample sizes and test durations.

## Example

- **Continuous Metric Example**:
  - Baseline mean: 100
  - Std: 15
  - MDE: 5 (absolute)
  - Alpha: 0.05, Power: 0.8
  - Groups: 2
  - Daily users: 1000

  The table will show how many participants per group and total are needed, along with how many days the test would take given 1000 users per day.

## Bonferroni Correction

If you have more than two groups (e.g., 3 or 4), the significance level is adjusted to control the family-wise error rate. For example, if `alpha = 0.05` and you have `n_groups = 3`, then:
\[
\alpha_{\text{eff}} = \frac{\alpha}{(3-1)} = \frac{0.05}{2} = 0.025
\]
This adjusted alpha is used in the calculations for critical values.


## License

This project is licensed under the [MIT License](LICENSE).
