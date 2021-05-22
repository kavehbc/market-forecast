import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
import yfinance as yf
from fbprophet import Prophet

from contextlib import contextmanager
from io import StringIO
from streamlit.report_thread import REPORT_CONTEXT_ATTR_NAME
from threading import current_thread
import sys

from libs.constants import *


@contextmanager
def st_redirect(src, dst):
    placeholder = st.empty()
    output_func = getattr(placeholder, dst)

    with StringIO() as buffer:
        old_write = src.write

        def new_write(b):
            if getattr(current_thread(), REPORT_CONTEXT_ATTR_NAME, None):
                buffer.write(b + '')
                output_func(buffer.getvalue() + '')
            else:
                old_write(b)

        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write


@contextmanager
def st_stdout(dst):
    "this will show the prints"
    with st_redirect(sys.stdout, dst):
        yield


@contextmanager
def st_stderr(dst):
    "This will show the logging"
    with st_redirect(sys.stderr, dst):
        yield


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
    st_future_days = st.sidebar.number_input("Future Days", value=365, min_value=1, step=1)

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

        # data preparation
        df_history_prep = df_history.reset_index()
        data = df_history_prep[["Date", "Close"]]  # select Date and Price
        data = data.rename(columns={"Date": "ds", "Close": "y"})

        # data training
        m = Prophet(daily_seasonality=True)
        m.fit(data)

        # predicting the future
        future = m.make_future_dataframe(periods=st_future_days)  # we need to specify the number of days in future
        prediction = m.predict(future)
        st.subheader("Prediction")
        st.write(prediction)

        # plot the result
        st.subheader("Visualization")

        _lock = RendererAgg.lock
        with _lock:
            m.plot(prediction)
            plt.title("Prediction")
            plt.xlabel("Date")
            plt.ylabel("Close Price")
            # plt.show()
            st.pyplot(plt)


if __name__ == '__main__':
    st.set_page_config("Ticker Analysis")
    with st_stdout("code"), st_stderr("error"):
        main()
