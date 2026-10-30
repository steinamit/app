# Employee Pricing Calculator

A Streamlit calculator that turns an employee's salary and employer costs into a monthly price to charge a client.

**Context:** personal tool · **Author:** Amit Stein

## What it does
- **Inputs:** gross salary, bonus, reimbursements, pension and severance %, employer national insurance %, other benefits, overhead % and profit margin %.
- **Output:** a breakdown of direct cost, overhead and profit, and the final monthly client price.
- **History:** every calculation is saved to a CSV and the last 50 are shown.

## Run
```bash
pip install streamlit pandas
streamlit run streamlit_app.py
```

**Tools:** Python · Streamlit · pandas
