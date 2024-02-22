import streamlit as st
from prophet.plot import plot_plotly, plot_components_plotly


def plot_predictions(ui_params, model, prediction):
    if ui_params.model == "fbprophet":
        fig_forecast = plot_plotly(model, prediction)
        st.plotly_chart(fig_forecast, use_container_width=True)

    elif ui_params.model == "neuralprophet":
        fig_forecast = model.plot(prediction)
        st.plotly_chart(fig_forecast, use_container_width=True)


def plot_fbprophet_components(ui_params, model, prediction):
    if ui_params.model == "fbprophet":

        fig_components = plot_components_plotly(model, prediction)
        st.plotly_chart(fig_components, use_container_width=True)

    elif ui_params.model == "neuralprophet":
        fig_components = model.plot_components(prediction)
        fig_parameters = model.plot_parameters()

        st.plotly_chart(fig_components, use_container_width=True)
        if fig_parameters:
            st.plotly_chart(fig_parameters, use_container_width=True)


