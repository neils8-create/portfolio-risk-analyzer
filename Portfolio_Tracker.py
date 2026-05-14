# Portfolio tracker

import numpy as np
import yfinance as yf
import plotly.graph_objects as go

def calculate_return(buy_price, current_price):
    gain = current_price - buy_price
    percent_return = (gain / buy_price) * 100
    return percent_return

def calculate_position_value(price, shares):
    return price * shares

def calculate_weight(position_value, total_portfolio_value):
    position_weight = (position_value / total_portfolio_value) * 100
    return position_weight

def calculate_volatility(monthly_returns):
    stock_volatility_array = np.array(monthly_returns)
    volatility_standard_deviation = np.std(stock_volatility_array)
    annual_standard_deviation = volatility_standard_deviation * np.sqrt(12)
    return annual_standard_deviation

def calculate_sharpe(portfolio_return, risk_free_rate, portfolio_volatility):
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return sharpe_ratio

def calculate_portfolio_volatility(portfolio):
    volatilities = []
    for stock in portfolio:
        vol = calculate_volatility(stock['monthly_returns'])
        volatilities.append(vol)
    return np.mean(volatilities)

def fetch_stock_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        history = ticker.history(period='6mo')
        current_price = history['Close'].iloc[-1]
        monthly_prices = history['Close'].resample('ME').last()
        monthly_returns = monthly_prices.pct_change().dropna() * 100
        return {
            'current_price': current_price,
            'monthly_returns': monthly_returns.tolist()
        }
    except Exception as e:
        print(f'Error fetching data for {ticker_symbol}: {e}')
        return None

def plot_weights(portfolio, total_value):
    tickers = [stock['ticker'] for stock in portfolio]
    weights = [calculate_weight(stock['value'], total_value) for stock in portfolio]
    fig = go.Figure(go.Pie(
        labels=tickers,
        values=weights,
        hole=0.4
    ))
    fig.update_layout(title='Portfolio Weights')
    return fig

def plot_risk_return(portfolio):
    tickers = [stock['ticker'] for stock in portfolio]
    returns = [calculate_return(stock['buy_price'], stock['current_price']) for stock in portfolio]
    volatilities = [calculate_volatility(stock['monthly_returns']) for stock in portfolio]
    fig = go.Figure(go.Scatter(
        x=volatilities,
        y=returns,
        mode='markers+text',
        text=tickers,
        textposition='top center',
        marker=dict(size=12)
    ))
    fig.update_layout(
        title='Risk vs Return',
        xaxis_title='Volatility (%)',
        yaxis_title='Return (%)'
    )
    return fig

def plot_position_values(portfolio):
    tickers = [stock['ticker'] for stock in portfolio]
    values = [stock['value'] for stock in portfolio]
    fig = go.Figure(go.Bar(
        x=tickers,
        y=values,
        text=[f'${v:,.0f}' for v in values],
        textposition='outside'
    ))
    fig.update_layout(
        title='Position Values',
        yaxis_title='Value ($)'
    )
    return fig

def plot_volatility(portfolio):
    tickers = [stock['ticker'] for stock in portfolio]
    volatilities = [calculate_volatility(stock['monthly_returns']) for stock in portfolio]
    fig = go.Figure(go.Bar(
        x=volatilities,
        y=tickers,
        orientation='h',
        text=[f'{v:.1f}%' for v in volatilities],
        textposition='outside'
    ))
    fig.update_layout(
        title='Volatility by Position',
        xaxis_title='Annualized Volatility (%)'
    )
    return fig

if __name__ == '__main__':
    total_value = 0
    total_cost = 0

    portfolio = [
        {'ticker': 'AAPL', 'buy_price': 178.0, 'shares': 15},
        {'ticker': 'MSFT', 'buy_price': 378.0, 'shares': 8},
        {'ticker': 'GOOGL', 'buy_price': 165.0, 'shares': 12},
        {'ticker': 'NVDA', 'buy_price': 875.0, 'shares': 6},
        {'ticker': 'TSLA', 'buy_price': 215.0, 'shares': 10},
        {'ticker': 'AMZN', 'buy_price': 185.0, 'shares': 11},
    ]

    for stock in portfolio:
        data = fetch_stock_data(stock['ticker'])
        if data:
            stock['current_price'] = data['current_price']
            stock['monthly_returns'] = data['monthly_returns']
        else:
            print(f"Skipping {stock['ticker']} - could not fetch data")

    for stock in portfolio:
        stock['value'] = calculate_position_value(stock['current_price'], stock['shares'])
        stock['cost'] = calculate_position_value(stock['buy_price'], stock['shares'])
        total_value += stock['value']
        total_cost += stock['cost']

    for stock in portfolio:
        ret = calculate_return(stock['buy_price'], stock['current_price'])
        weight = calculate_weight(stock['value'], total_value)
        volatility = calculate_volatility(stock['monthly_returns'])
        print(f"{stock['ticker']}: ${stock['value']:,.2f} | return: {ret:.1f}% | weight: {weight:.2f}% | volatility: {volatility:.2f}%")

    overall_return = calculate_return(total_cost, total_value)
    portfolio_volatility = calculate_portfolio_volatility(portfolio)
    portfolio_sharpe_ratio = calculate_sharpe(overall_return, 4.5, portfolio_volatility)

    print(f'\n --- Portfolio Summary ---')
    print(f'Total Portfolio Value: ${total_value:,.2f}')
    print(f'Overall Return: {overall_return:.1f}%')
    print(f'Portfolio Volatility: {portfolio_volatility:.2f}%')
    print(f'Sharpe Ratio: {portfolio_sharpe_ratio:.2f}')

    plot_weights(portfolio, total_value).show()
    plot_risk_return(portfolio).show()
    plot_position_values(portfolio).show()
    plot_volatility(portfolio).show()