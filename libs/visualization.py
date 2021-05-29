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


def plot_fbprophet_components(model, prediction):
    fig_components = model.plot_components(prediction)
    _lock = RendererAgg.lock
    with _lock:
        st.pyplot(fig_components)
