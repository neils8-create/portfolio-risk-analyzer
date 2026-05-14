# Portfolio Risk Analyzer

A web app that analyzes your stock portfolio in real time. Enter your holdings and instantly see position values, returns, volatility, and Sharpe ratio — plus four interactive charts.

## Live App
https://portfolio-risk-analyzer-ns23.streamlit.app/

## Features
- Real-time stock data via yfinance
- Per-position analysis: value, return, weight, and annualized volatility
- Portfolio-level metrics: total value, overall return, volatility, and Sharpe ratio
- Four interactive charts: portfolio weights, risk vs return, position values, and volatility comparison
- Input validation and duplicate ticker detection

## Tech Stack
- Python
- Streamlit
- Plotly
- yfinance
- NumPy

## Run Locally
1. Clone the repository
2. Create a virtual environment and activate it
3. Run `pip install -r requirements.txt`
4. Run `streamlit run app.py`

## Roadmap
This project is Phase 1 of a longer roadmap toward building a full-featured portfolio risk platform. Future phases will add more advanced risk analytics, deeper performance metrics, and additional tools for self-directed investors and independent financial advisors.