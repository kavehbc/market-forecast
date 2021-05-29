import streamlit as st
import yfinance as yf
from libs.dot_dict_class import DotDict


@st.cache(max_entries=50, ttl=900, allow_output_mutation=True,
          suppress_st_warning=True, show_spinner=False)
def get_ticker_details(ui_params):
    yf_ticker = yf.Ticker(ui_params.ticker_name)

    ticker = DotDict(info=yf_ticker.info,
                     recommendations=yf_ticker.recommendations,
                     history=yf_ticker.history(period=ui_params.period, interval=ui_params.interval))
    return ticker


def ui_ticker_details(ui_params):
    ticker = get_ticker_details(ui_params)
    with st.beta_expander("Ticker/Symbol Details", expanded=True):
        st.write(ticker.info)

    df_recommendations = ticker.recommendations
    st.subheader(":ribbon: Recommendations")
    if df_recommendations is None:
        st.error("There is no recommendation available.")
    else:
        df_recommendations_desc = df_recommendations.sort_index(ascending=False)
        st.write(df_recommendations_desc)

    df_history = ticker.history
    if df_history is not None:
        df_history_desc = df_history.sort_index(ascending=False)

        st.subheader(":page_with_curl: History")
        st.write(df_history_desc)

    return df_history
