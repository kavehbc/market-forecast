import streamlit as st
from libs.constants import *
from libs.dot_dict_class import DotDict


def format_crypto(x):
    if x is None:
        return CRYPTOS[x]
    else:
        return x + " - " + CRYPTOS[x]


def create_ui_params():
    st.title("Market Forecast")
    st.warning(
        ":warning: **Warning:** This tool neither recommends nor guarantees the performance of the given symbol. "
        "Use this tool and its forecasts at your own risk.")
    st.caption("Raw data is extracted from `Yahoo! Finance`.")
    st.caption("The app usage is tracked using [statcounter.com](https://statcounter.com/),"
               " and it does not contain any personal information, since we never ask you any personal info."
               " The symbol names searched are stored for the auto-complete future."
               " That locally stored database can be accessed via `Popular Symbols` menu option."
               " This is an open-source application, and for more information you can check the `About app` section."
               " By using this app, you agreed with these terms and conditions.")
    st_ml_model = st.sidebar.selectbox("Predictive Model", options=list(ML_MODELS.keys()), index=0,
                                       format_func=lambda x: ML_MODELS[x])
    st_crypto_stock = st.sidebar.radio("Symbol Type", options=TICKER_TYPE)
    if st_crypto_stock == TICKER_TYPE[0]:
        st_crypto_name = st.sidebar.selectbox("Crypto Symbol", options=list(CRYPTOS.keys()),
                                              format_func=format_crypto)
        st_currency_name = st.sidebar.selectbox("Currency", options=CURRENCIES)

        if st_crypto_name is None:
            st_ticker_name = None
        else:
            st_ticker_name = st_crypto_name + "-" + st_currency_name

    elif st_crypto_stock == TICKER_TYPE[1]:

        st_ticker_name_list = st.sidebar.text_input('Stock Symbol')
        st_ticker_name_list = [st_ticker_name_list]

        if len(st_ticker_name_list) > 0:
            st_ticker_name = st_ticker_name_list[0].upper()
        else:
            st_ticker_name = None

        # st_ticker_name = st.sidebar.text_input("Stock Symbol", value="MSFT").upper()
        st.sidebar.caption("Add `.TO` for the symbol in TSX")
    st_period = st.sidebar.selectbox("Period (History)", options=list(PERIODS.keys()), index=7,
                                     format_func=lambda x: PERIODS[x])
    st_interval = st.sidebar.selectbox("Interval", options=list(INTERVALS.keys()), index=8,
                                       format_func=lambda x: INTERVALS[x])
    st_price_column = st.sidebar.selectbox("Price",
                                           options=TICKER_DATA_COLUMN,
                                           index=3)
    st_future_days = st.sidebar.number_input("Future Days", value=365, min_value=1, step=1)
    st_future_volume = st.sidebar.number_input("Future Volume Assumption", value=0, min_value=0, step=1)
    st.sidebar.caption("Set Volume to 0 to ignore")
    st_training_percentage = st.sidebar.slider("Training Percentage", min_value=0.0, max_value=1.0, step=0.1, value=0.8)
    st_yearly_seasonality = st.sidebar.selectbox("Yearly Seasonality",
                                                 options=SEASONALITY_OPTIONS,
                                                 index=0)
    st_weekly_seasonality = st.sidebar.selectbox("Weekly Seasonality",
                                                 options=SEASONALITY_OPTIONS,
                                                 index=0)
    st_daily_seasonality = st.sidebar.selectbox("Daily Seasonality",
                                                options=SEASONALITY_OPTIONS,
                                                index=0)
    st_holidays = st.sidebar.selectbox("Holidays", options=list(HOLIDAYS.keys()), index=0,
                                       format_func=lambda x: HOLIDAYS[x])

    if st_crypto_stock == TICKER_TYPE[0]:
        st_seasonality_mode_index = 0
    else:
        st_seasonality_mode_index = 1
    st_seasonality_mode = st.sidebar.selectbox("Seasonality Mode",
                                               options=SEASONALITY_MODE_OPTIONS,
                                               index=st_seasonality_mode_index)

    dic_return = DotDict(model=st_ml_model,
                         ticker_name=st_ticker_name,
                         period=st_period,
                         interval=st_interval,
                         future_days=st_future_days,
                         price_column=st_price_column,
                         future_volume=st_future_volume,
                         training_percentage=st_training_percentage,
                         yearly_seasonality=st_yearly_seasonality,
                         weekly_seasonality=st_weekly_seasonality,
                         daily_seasonality=st_daily_seasonality,
                         holidays=st_holidays,
                         seasonality_mode=st_seasonality_mode)
    return dic_return


def create_cross_validation_form(ui_params):
    col1, col2, col3 = st.columns(3)
    with col1:
        st_cv_initial_days = st.number_input("Initial days", value=730, min_value=1, step=1)
    with col2:
        st_cv_period_days = st.number_input("Period days", value=180, min_value=1, step=1)
    with col3:
        st_cv_horizon_days = st.number_input("Horizon days", value=365, min_value=1, step=1)

    st_validation_metric = st.selectbox("Validation Metric", options=VALIDATION_METRICS,
                                        index=3)
    show_cross_validation = st.form_submit_button(label='Cross-Validate')
    # show_cross_validation = st.checkbox("Show Cross-Validation", value=False)
    st.caption("This can take some time.")

    dic_return = DotDict(initial_days=st_cv_initial_days,
                         period_days=st_cv_period_days,
                         horizon_days=st_cv_horizon_days,
                         validation_metric=st_validation_metric,
                         cross_validation=show_cross_validation)

    return dic_return
