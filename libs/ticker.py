import streamlit as st
import yfinance as yf


def ui_ticker_details(ui_params):
    yf_ticker = yf.Ticker(ui_params.ticker_name)
    with st.beta_expander("Info", expanded=True):
        st.write(yf_ticker.info)

    df_recommendations = yf_ticker.recommendations
    st.subheader("Recommendations")
    if df_recommendations is None:
        st.error("There is no recommendation available.")
    else:
        df_recommendations_desc = df_recommendations.sort_index(ascending=False)
        st.write(df_recommendations_desc)

    df_history = yf_ticker.history(period=ui_params.period, interval=ui_params.interval)
    if df_history is not None:
        df_history_desc = df_history.sort_index(ascending=False)

        st.subheader("History")
        st.write(df_history_desc)

    return df_history
