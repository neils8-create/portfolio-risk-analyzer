# Imports
import streamlit as st
import time
from Portfolio_Tracker import fetch_stock_data, calculate_return, calculate_position_value, calculate_weight, calculate_volatility, calculate_portfolio_volatility, calculate_sharpe, plot_weights, plot_risk_return, plot_position_values, plot_volatility

# Initialize session state for portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# Title
st.title('Portfolio Risk Analyzer')
st.write('Enter your holdings below:')

# User Inputs
ticker = st.text_input('Enter a ticker symbol', value = '').upper()
buy_price = st.number_input('Buy price', min_value = 0.0, value = 0.0)
shares = st.number_input('Number of shares', min_value = 0, value = 0)


# Add Stock button Confirms user input and adds to portfolio list in session state. Checks user inputs as for invlaid price, shares, and ticker symbol

if st.button('Add Stock'):
    already_exists = any(stock['ticker'] == ticker.upper() for stock in st.session_state.portfolio)
    if already_exists:
        st.error(f"'{ticker.upper()}' is already in your portfolio. Please remove it first if you want to update the position.")
    elif buy_price <= 0 or shares <= 0:
        st.error('Buy price and number of shares must be greater than 0.')
    else: 
        with st.spinner('Validating Ticker...'):
            data = fetch_stock_data(ticker)
        if data is None:
            st.error(f"'{ticker}' doesn't appear to be a valid ticker. Please check and try again.")
        else:
            st.session_state.portfolio.append({
                'ticker': ticker.upper(),
                'buy_price': buy_price,
                'shares': shares
            })
            success_box = st.empty()
            success_box.success(f"Added {shares} shares of {ticker.upper()} at ${buy_price:.2f} to portfolio.")
            time.sleep(2)
            success_box.empty()

# Prints current portfolio with remove buttons
for i, stock in enumerate(st.session_state.portfolio):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"{stock['ticker']} - {stock['shares']} shares at ${stock['buy_price']}")
    with col2:
        if st.button('Remove', key = f'remove_{i}'):
            st.session_state.portfolio.pop(i)
            st.rerun()
    

# Runs analysis on user portfolio when button is clicked
if st.button('Analyze Portfolio'):
    with st.spinner('Analyzing...'):

        # Fetch data for each stock and calculate metrics
        for stock in st.session_state.portfolio:
            data = fetch_stock_data(stock['ticker'])
            if data:
                stock['current_price'] = data['current_price']
                stock['monthly_returns'] = data['monthly_returns']
                
        total_value = 0
        total_cost = 0

        for stock in st.session_state.portfolio:
            stock['value'] = calculate_position_value(stock['current_price'], stock['shares'])
            stock['cost'] = calculate_position_value(stock['buy_price'], stock['shares'])
            total_value += stock['value']
            total_cost += stock['cost']

        st.divider()
        st.subheader('Position Summary')
        st.write('  ')
        for stock in st.session_state.portfolio:
            ret = calculate_return(stock['buy_price'], stock['current_price'])
            weight = calculate_weight(stock['value'], total_value)
            volatility = calculate_volatility(stock['monthly_returns'])
            st.write(f"{stock['ticker']}: ${stock['value']:,.2f} | return: {ret:.1f}% | weight: {weight:.2f}% | volatility: {volatility:.2f}%")

        overall_return = calculate_return(total_cost, total_value)
        portfolio_volatility = calculate_portfolio_volatility(st.session_state.portfolio)
        portfolio_sharpe_ratio = calculate_sharpe(overall_return, 4.5, portfolio_volatility)

        st.divider()
        st.write('  ')
        st.subheader(f'Portfolio Summary')
        st.write('  ')

        st.write(f'Total Portfolio Value: ${total_value:,.2f}')
        st.write(f'Overall Return: {overall_return:.1f}%')
        st.write(f'Portfolio Volatility: {portfolio_volatility:.2f}%')
        st.write(f'Sharpe Ratio: {portfolio_sharpe_ratio:.2f}')

        st.plotly_chart(plot_weights(st.session_state.portfolio, total_value))
        st.plotly_chart(plot_risk_return(st.session_state.portfolio))
        st.plotly_chart(plot_position_values(st.session_state.portfolio))
        st.plotly_chart(plot_volatility(st.session_state.portfolio))