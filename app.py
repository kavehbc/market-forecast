import streamlit as st
from libs.constants import *
from libs.data_preprocessing import prepare_hisotry_for_fbprophet
from libs.model import create_model, predict
from libs.readme import show_readme
from libs.ticker import ui_ticker_details
from libs.ui_params import create_ui_params
from libs.visualization import plot_predictions, plot_fbprophet_components


def main():
    st_app_menu = st.sidebar.selectbox("Main Menu", options=list(MENU_OPTIONS.keys()), index=0,
                                       format_func=lambda x: MENU_OPTIONS[x])

    if st_app_menu == "about":
        show_readme()
        st.stop()

    ui_params = create_ui_params()

    if ui_params.ticker_name is None or len(ui_params.ticker_name) == 0:
        st.warning("Please enter a valid ticker or select a crypto")
    else:
        st_app_status_placeholder = st.empty()
        st.subheader(ui_params.ticker_name)

        df_history = ui_ticker_details(ui_params)
        if df_history is not None:

            # data preparation
            data = prepare_hisotry_for_fbprophet(ui_params, df_history)

            # data training
            m = create_model(ui_params, data, st_app_status_placeholder)

            # predicting the future
            prediction = predict(ui_params, m, st_app_status_placeholder)
            fig_components = m.plot_components(prediction)

            st.subheader("Prediction")
            st.write(prediction)

            # plot the result
            st.subheader("Visualization")
            plot_predictions(m, prediction)
            plot_fbprophet_components(m, prediction)


if __name__ == '__main__':
    st.set_page_config("Market Technical Analysis")
    main()
