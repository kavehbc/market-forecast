import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg


def plot_predictions(ui_params, model, prediction):
    _lock = RendererAgg.lock
    with _lock:
        model.plot(prediction)
        plt.title("Prediction")
        plt.xlabel("Date")
        plt.ylabel(ui_params.price_column + " Price")
        # plt.show()
        st.pyplot(plt)


def plot_fbprophet_components(ui_params, model, prediction):
    if ui_params.model == "fbprophet":
        fig_components = model.plot_components(prediction)

        _lock = RendererAgg.lock
        with _lock:
            st.pyplot(fig_components)

    elif ui_params.model == "neuralprophet":
        fig_components = model.plot_components(prediction)
        fig_parameters = model.plot_parameters()
        st.write(type(fig_components))

        _lock = RendererAgg.lock
        with _lock:
            st.plotly_chart(fig_components)
            if fig_parameters:
                st.plotly_chart(fig_parameters)


