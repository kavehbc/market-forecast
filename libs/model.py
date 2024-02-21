import streamlit as st
import pandas as pd
from prophet import Prophet
from neuralprophet import NeuralProphet


# @st.cache_data(max_entries=50, show_spinner=False)
def create_model(ui_params, data):
    # data training
    if ui_params.model == "fbprophet":
        m = Prophet(changepoint_range=ui_params.training_percentage,
                    yearly_seasonality=ui_params.yearly_seasonality,
                    weekly_seasonality=ui_params.weekly_seasonality,
                    daily_seasonality=ui_params.daily_seasonality,
                    seasonality_mode=ui_params.seasonality_mode)

        if ui_params.future_volume > 0:
            m.add_regressor('Volume')
        if ui_params.holidays is not None:
            m.add_country_holidays(country_name=ui_params.holidays)

        data["ds"] = pd.to_datetime(data["ds"]).dt.tz_localize(None)

        m.fit(data)
        train_metrics = None
        val_metrics = None

    elif ui_params.model == "neuralprophet":
        # changepoint_range=ui_params.training_percentage,
        # replaced with n_changepoint
        m = NeuralProphet(yearly_seasonality=ui_params.yearly_seasonality,
                          weekly_seasonality=ui_params.weekly_seasonality,
                          daily_seasonality=ui_params.daily_seasonality,
                          seasonality_mode=ui_params.seasonality_mode,
                          n_forecasts=ui_params.future_days,
                          num_hidden_layers=5)

        if ui_params.training_percentage < 1.0:
            validation_percentage = 1.0 - ui_params.training_percentage
            data["ds"] = pd.to_datetime(data["ds"]).dt.tz_localize(None)
            df_train, df_val = m.split_df(data, valid_p=validation_percentage)
        else:
            df_train = data
            df_val = None

        train_metrics = m.fit(df_train, freq="D")  # validate_each_epoch=True
        if df_val is None:
            val_metrics = None
        else:
            val_metrics = m.test(df_val)

    return m, train_metrics, val_metrics


# @st.cache_data(max_entries=50, ttl=900, show_spinner=False)
def generate_future(ui_params, model, data):
    # we need to specify the number of days in future
    if ui_params.model == "fbprophet":
        future = model.make_future_dataframe(periods=ui_params.future_days)
        if ui_params.future_volume > 0:
            future['Volume'] = ui_params.future_volume

    elif ui_params.model == "neuralprophet":
        future = model.make_future_dataframe(data,
                                             periods=ui_params.future_days,
                                             n_historic_predictions=len(data))
    return future


# @st.cache_data(max_entries=50, ttl=900, show_spinner=False)
def predict(model, future):
    prediction = model.predict(future)
    return prediction
