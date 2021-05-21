import streamlit as st
import yfinance as yf

PERIODS = {"1d": "1 day", "5d": "5 days", "1mo": "1 month", "3mo": "3 months", "6mo": "6 months",
           "1y": "1 year", "2y": "2 years", "5y": "5 years", "10y": "10 years",
           "ytd": "year today", "max": "Max"}
INTERVALS = {"1m": "1 minute", "2m": "2 minutes", "5m": "5 minutes", "15m": "15 minutes",
             "30m": "30 minutes", "60m": "60 minutes", "90m": "90 minutes",
             "1h": "1 hour", "1d": "1 day", "5d": "5 days", "1wk": "1 week",
             "1mo": "1 month", "3mo": "3 months"}
TICKER_TYPE = ["Crypto", "Stock"]
CURRENCIES = ["USD", "EUR", "CAD", "GBP", "AUD", "JPY", "KRW", "RUB"]
CRYPTOS = {"BTC": "Bitcoin", "ETH": "Ethereum", "BNB": "BinanceCoin", "USDT": "Tether",
           "ADA": "Cardano", "XRP": "XRP", "DOGE": "DogeCoin", "DOT1": "Polkadot", "BCH": "BitcoinCash",
           "UNI3": "Uniswap", "USDC": "USDCoin", "LTC": "Litecoin", "LINK": "Chainlink", "SOL1": "Solana",
           "XLM": "Stellar", "MATIC": "MaticNetwork", "HEX": "HEX", "ETC": "EthereumClassic",
           "VET": "VeChain", "THETA": "THETA", "TRX": "TRON", "FIL": "FilecoinFutures", "EOS": "EOS",
           "AAVE": "Aave", "XMR": "Monero", "NEO": "NEO", "LUNA1": "Terra", "MKR": "Maker",
           "MIOTA": "IOTA", "BSV": "BitcoinSV", "XTZ": "Tezos", "KSM": "Kusama", "CRO": "CryptocomCoin",
           "ATOM1": "Cosmos", "ALGO": "Algorand", "AVAX": "Avalanche", "BTT1": "BitTorrent", "COMP": "Compound",
           "WAVES": "Waves", "CTC1": "Creditcoin", "DASH": "Dash", "HBAR": "HederaHashgraph",
           "ZEC": "Zcash", "XEM": "NEM", "SNX": "SynthetixNetworkToken", "EGLD": "Elrond",
           "SUSHI": "Sushi", "CHZ": "Chiliz", "DCR": "Decred", "YFI": "yearnfinance"}


def main():
    st.title("Ticker Analysis")
    st.caption("Data is extracted from Yahoo! Finance")
    st_crypto_stock = st.sidebar.radio("Ticker Type", options=TICKER_TYPE)
    if st_crypto_stock == TICKER_TYPE[0]:
        st_crypto_name = st.sidebar.selectbox("Crypto Ticker", options=list(CRYPTOS.keys()),
                                              format_func=lambda x: x + " - " + CRYPTOS[x])
        st_currency_name = st.sidebar.selectbox("Currency", options=CURRENCIES)
        st_ticker_name = st_crypto_name + "-" + st_currency_name
    elif st_crypto_stock == TICKER_TYPE[1]:
        st_ticker_name = st.sidebar.text_input("Stock Ticker", value="MSFT").upper()
    st_period = st.sidebar.selectbox("Period", options=list(PERIODS.keys()), index=10,
                                     format_func=lambda x: PERIODS[x])
    st_interval = st.sidebar.selectbox("Interval", options=list(INTERVALS.keys()), index=8,
                                       format_func=lambda x: INTERVALS[x])

    st.subheader(st_ticker_name)
    yf_ticker = yf.Ticker(st_ticker_name)
    with st.beta_expander("Info", expanded=True):
        st.write(yf_ticker.info)

    df_recommendations = yf_ticker.recommendations
    if df_recommendations is not None:
        df_recommendations_desc = df_recommendations.sort_index(ascending=False)
        st.subheader("Recommendations")
        st.write(df_recommendations_desc)

    df_history = yf_ticker.history(period=st_period, interval=st_interval)
    if df_history is not None:
        df_history_desc = df_history.sort_index(ascending=False)
        st.subheader("History")
        st.write(df_history_desc)


if __name__ == '__main__':
    st.set_page_config("Ticker Analysis")
    main()
