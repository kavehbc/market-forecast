import streamlit as st
import numpy as np

from libs.constants import *
from libs.cross_validation import cross_validating, evaluating, plot_validation
from libs.data_preprocessing import prepare_hisotry_for_fbprophet
from libs.db import update_db, tickers_to_df
from libs.future_change import display_future_change
from libs.injection import manage_injections
from libs.model import create_model, predict, generate_future
from libs.readme import show_readme
from libs.ticker import ui_ticker_details
from libs.ui_params import create_ui_params
from libs.visualization import plot_predictions, plot_fbprophet_components


def main():
    # inject required HTML/CSS/JS into the project
    manage_injections()

    st_app_menu = st.sidebar.selectbox("Main Menu", options=list(MENU_OPTIONS.keys()), index=0,
                                       format_func=lambda x: MENU_OPTIONS[x])

    if st_app_menu == "about":
        show_readme()
        st.stop()

    if st_app_menu == "popular":
        df_tickers = tickers_to_df()
        top_n = 100
        st.title(f"Top {top_n} Tickers")
        st.caption("These data is stored where this app is hosted."
                   " This app would **NOT** transmit these data elsewhere automatically."
                   " These data is stored for the autocomplete feature.")
        st.write(df_tickers.head(top_n))
        st.stop()

    ui_params = create_ui_params()

    if ui_params.ticker_name is None or len(ui_params.ticker_name) == 0:
        st.warning(":heavy_exclamation_mark: Please enter a valid ticker or select a crypto from the sidebar menu")
    else:
        ph_app_status = st.empty()
        st.subheader(ui_params.ticker_name)

        df_history = ui_ticker_details(ui_params)
        if df_history is not None:
            # update ticker database
            update_db(ui_params.ticker_name)

            # data preparation
            data = prepare_hisotry_for_fbprophet(ui_params, df_history)

            st.subheader(":boom: Prediction")

            # data training
            ph_training = st.empty()
            ph_app_status.info("Training started. It may take a while...")
            ph_training.info("Training started. It may take a while...")
            m = create_model(ui_params, data)

            # predicting the future
            ph_app_status.info("Generating the future dataset...")
            ph_training.info("Generating the future dataset...")
            future = generate_future(ui_params, m)

            ph_app_status.info("Forecasting...")
            ph_training.info("Forecasting...")
            prediction = predict(m, future)
            col1, col2 = st.beta_columns(2)
            with col1:
                st_from_date = np.datetime64(st.date_input("From",
                                                           value=data["ds"].max(),
                                                           min_value=data["ds"].max()))
            with col2:
                st_to_date = np.datetime64(st.date_input("Until",
                                                         value=prediction["ds"].max(),
                                                         max_value=prediction["ds"].max()))

            filtered_prediction = prediction[(prediction["ds"] >= st_from_date) &
                                             (prediction["ds"] <= st_to_date)]
            st.write(filtered_prediction)
            ph_training.empty()

            st.subheader(":dizzy: Future Change")
            display_future_change(data, filtered_prediction)

            # plot the result
            st.subheader(":chart_with_upwards_trend: Visualization")
            plot_predictions(ui_params, m, prediction)
            plot_fbprophet_components(m, prediction)

            # Execute cross validation
            st.subheader(":question: Cross-Validation")
            with st.form(key="cross-validation"):
                col1, col2, col3 = st.beta_columns(3)
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

            ph_cross_validation = st.empty()

            if show_cross_validation:
                ph_app_status.info("Cross-Validating...")
                ph_cross_validation.info("Cross-Validation started. Please wait...")
                df_cv = cross_validating(m,
                                         st_cv_initial_days, st_cv_period_days, st_cv_horizon_days)

                ph_cross_validation.info("Calculating performance metrics. Please wait...")
                pm = evaluating(df_cv)

                ph_cross_validation.info("Displaying the results...")
                plot_validation(pm, df_cv, metric=st_validation_metric)
                ph_cross_validation.empty()

        # resetting the app status
        ph_app_status.empty()


if __name__ == '__main__':
    st.set_page_config(page_title="Market Technical Analysis",
                       page_icon="💹",
                       initial_sidebar_state="expanded")
    main()
