import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
import yfinance as yf
import fbprophet
from fbprophet import Prophet
from libs.constants import *


def format_crypto(x):
    if x is None:
        return CRYPTOS[x]
    else:
        return x + " - " + CRYPTOS[x]


def main():
    st.title("Market Technical Analysis")
    st.warning("**Warning:** This tool neither recommends nor guarantees the performance of the given ticker. "
               "Use this tool and its forecasts at your own risk.")
    st.caption("Data is extracted from Yahoo! Finance")
    st.caption("Data analysis is done by Facebook Prophet v." + fbprophet.__version__)

    st_crypto_stock = st.sidebar.radio("Ticker Type", options=TICKER_TYPE)
    if st_crypto_stock == TICKER_TYPE[0]:
        st_crypto_name = st.sidebar.selectbox("Crypto Ticker", options=list(CRYPTOS.keys()),
                                              format_func=format_crypto)
        st_currency_name = st.sidebar.selectbox("Currency", options=CURRENCIES)
        if st_crypto_name is None:
            st_ticker_name = None
        else:
            st_ticker_name = st_crypto_name + "-" + st_currency_name
    elif st_crypto_stock == TICKER_TYPE[1]:
        st_ticker_name = st.sidebar.text_input("Stock Ticker", value="MSFT").upper()
        st.sidebar.caption("Add `.TO` for the tickers in Toronto Stock Exchange")
    st_period = st.sidebar.selectbox("Period", options=list(PERIODS.keys()), index=7,
                                     format_func=lambda x: PERIODS[x])
    st_interval = st.sidebar.selectbox("Interval", options=list(INTERVALS.keys()), index=8,
                                       format_func=lambda x: INTERVALS[x])
    st_future_days = st.sidebar.number_input("Future Days", value=365, min_value=1, step=1)
    st_future_volume = st.sidebar.number_input("Future Volume Assumption", value=0, min_value=0, step=1)
    st_training_percentage = st.sidebar.slider("Training Percentage", min_value=0.0, max_value=1.0, step=0.1, value=0.8)
    st_yearly_seasonality = st.sidebar.selectbox("Yearly Seasonality",
                                                 options=seasonality_options,
                                                 index=0)
    st_weekly_seasonality = st.sidebar.selectbox("Weekly Seasonality",
                                                 options=seasonality_options,
                                                 index=0)
    st_daily_seasonality = st.sidebar.selectbox("Daily Seasonality",
                                                options=seasonality_options,
                                                index=0)
    st_holidays = st.sidebar.selectbox("Holidays", options=list(HOLIDAYS.keys()), index=0,
                                       format_func=lambda x: HOLIDAYS[x])
    st_seasonality_mode = st.sidebar.selectbox("Seasonality Mode",
                                               options=seasonality_mode_options,
                                               index=0)

    if st_ticker_name is None or len(st_ticker_name) == 0:
        st.warning("Please enter a valid ticker or select a crypto")
    else:
        st_app_status_placeholder = st.empty()
        st.subheader(st_ticker_name)
        yf_ticker = yf.Ticker(st_ticker_name)
        with st.beta_expander("Info", expanded=True):
            st.write(yf_ticker.info)

        df_recommendations = yf_ticker.recommendations
        st.subheader("Recommendations")
        if df_recommendations is None:
            st.error("There is no recommendation available.")
        else:
            df_recommendations_desc = df_recommendations.sort_index(ascending=False)
            st.write(df_recommendations_desc)

        df_history = yf_ticker.history(period=st_period, interval=st_interval)
        if df_history is not None:
            df_history_desc = df_history.sort_index(ascending=False)

            st.subheader("History")
            st.write(df_history_desc)

            # data preparation
            df_history_prep = df_history.reset_index()
            if st_future_volume > 0:
                data = df_history_prep[["Date", "Close", "Volume"]]
            else:
                data = df_history_prep[["Date", "Close"]] # select Date and Price
            data = data.rename(columns={"Date": "ds", "Close": "y"})

            # data training
            m = Prophet(changepoint_range=st_training_percentage,
                        yearly_seasonality=st_yearly_seasonality,
                        weekly_seasonality=st_weekly_seasonality,
                        daily_seasonality=st_daily_seasonality,
                        seasonality_mode=st_seasonality_mode)
            if st_future_volume > 0:
                m.add_regressor('Volume')
            if st_holidays is not None:
                m.add_country_holidays(country_name=st_holidays)

            st_app_status_placeholder.info("Training started. It may take a while...")
            m.fit(data)
            st_app_status_placeholder.empty()

            # predicting the future
            st_app_status_placeholder.info("Generating the future dataset...")
            future = m.make_future_dataframe(periods=st_future_days)  # we need to specify the number of days in future
            if st_future_volume > 0:
                future['Volume'] = st_future_volume

            st_app_status_placeholder.info("Forecasting the future...")
            prediction = m.predict(future)
            st_app_status_placeholder.empty()
            fig_components = m.plot_components(prediction)

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

                st.pyplot(fig_components)


if __name__ == '__main__':
    st.set_page_config("Market Technical Analysis")
    main()
