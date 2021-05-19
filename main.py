import streamlit as st
import yfinance as yf

PERIODS = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
INTERVALS = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]


def main():
    st.title("YF")
    st_ticker_name = st.sidebar.text_input("Ticker", value="MSFT").upper()
    st_period = st.sidebar.selectbox("Period", options=PERIODS, index=10)
    st_interval = st.sidebar.selectbox("Interval", options=INTERVALS, index=8)

    yf_ticker = yf.Ticker(st_ticker_name)
    st.write(yf_ticker.info)
    st.write(yf_ticker.recommendations)
    df_history = yf_ticker.history(period=st_period, interval=st_interval)
    st.write(df_history)


if __name__ == '__main__':
    main()
