import streamlit as st
import numpy as np
import os
import datetime

from libs.constants import *
from libs.cross_validation import cross_validating, evaluating, plot_validation, plot_validation_neural
from libs.data_preprocessing import prepare_hisotry_for_fbprophet
from libs.db import update_db, tickers_to_df, reset_tmp_db
from libs.future_change import display_future_change
from libs.injection import manage_injections
from libs.model import create_model, predict, generate_future
from libs.readme import show_readme
from libs.ticker import ui_ticker_details
from libs.ui_params import create_ui_params, create_cross_validation_form
from libs.visualization import plot_predictions, plot_fbprophet_components


# this is to prevent the conflict of OpenMP runtime
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def main():
    # reading query strings
    qs_data = st.experimental_get_query_params()
    for key, value in qs_data.items():
        if key == "reset_db" and str(value[0]) == "true":
            if reset_tmp_db():
                st.success("tmp database is deleted successfully.")
            st.experimental_set_query_params(reset_db="false")

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
        st.warning(":heavy_exclamation_mark: Please enter a valid symbol or select a crypto from the sidebar menu")
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
            m, train_metrics, val_metrics = create_model(ui_params, data)

            # predicting the future
            ph_app_status.info("Generating the future dataset...")
            ph_training.info("Generating the future dataset...")
            future = generate_future(ui_params, m, data)

            ph_app_status.info("Forecasting...")
            ph_training.info("Forecasting...")
            prediction = predict(m, future)
            col1, col2 = st.columns(2)
            with col1:
                today_date = data["ds"].max()
                tomorrow_date = today_date + datetime.timedelta(days=1)
                st_from_date = np.datetime64(st.date_input("From",
                                                           value=tomorrow_date,
                                                           min_value=tomorrow_date))
            with col2:
                st_to_date = np.datetime64(st.date_input("Until",
                                                         value=prediction["ds"].max(),
                                                         max_value=prediction["ds"].max()))

            filtered_prediction = prediction[(prediction["ds"] >= st_from_date) &
                                             (prediction["ds"] <= st_to_date)]
            st.write(filtered_prediction)
            ph_training.empty()

            st.header(":dizzy: Future Change")
            display_future_change(ui_params, data, filtered_prediction)

            # plot the result
            st.subheader(":chart_with_upwards_trend: Visualization")
            plot_predictions(ui_params, m, prediction)
            plot_fbprophet_components(ui_params, m, prediction)

            # Execute cross validation
            st.subheader(":question: Cross-Validation")
            ph_cross_validation = st.empty()

            if ui_params.model == "fbprophet":
                with st.form(key="cross-validation"):
                    ui_cv_params = create_cross_validation_form(ui_params)

                if ui_cv_params.cross_validation:
                    ph_app_status.info("Cross-Validating...")
                    ph_cross_validation.info("Cross-Validation started. Please wait...")

                    df_cv = cross_validating(m,
                                             ui_cv_params.initial_days,
                                             ui_cv_params.period_days,
                                             ui_cv_params.horizon_days)

                    ph_cross_validation.info("Calculating performance metrics. Please wait...")
                    pm = evaluating(df_cv)

                    ph_cross_validation.info("Displaying the results...")
                    plot_validation(pm, df_cv, metric=ui_cv_params.validation_metric)
            elif ui_params.model == "neuralprophet":
                st.write("**Training Metrics**")
                st.write(train_metrics)
                plot_validation_neural(train_metrics, "Loss")
                plot_validation_neural(train_metrics, "RMSE")
                plot_validation_neural(train_metrics, "MAE")
                plot_validation_neural(train_metrics, "RegLoss")

                st.write("**Validation Metrics**")
                st.write(val_metrics)
                plot_validation_neural(val_metrics, "Loss_test")
                plot_validation_neural(val_metrics, "RegLoss_test")

                ph_cross_validation.empty()

        # resetting the app status
        ph_app_status.empty()


if __name__ == '__main__':
    st.set_page_config(page_title="Market Forecast",
                       page_icon="💹",
                       initial_sidebar_state="expanded")
    main()
