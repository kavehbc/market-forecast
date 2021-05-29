import streamlit as st
from fbprophet import Prophet


# hash_funcs={DotDict: hash},
@st.cache(max_entries=50, allow_output_mutation=True,
          suppress_st_warning=True, show_spinner=False)
def create_model(ui_params, data):
    # data training
    m = Prophet(changepoint_range=ui_params.training_percentage,
                yearly_seasonality=ui_params.yearly_seasonality,
                weekly_seasonality=ui_params.weekly_seasonality,
                daily_seasonality=ui_params.daily_seasonality,
                seasonality_mode=ui_params.seasonality_mode)

    if ui_params.future_volume > 0:
        m.add_regressor('Volume')
    if ui_params.holidays is not None:
        m.add_country_holidays(country_name=ui_params.holidays)

    m.fit(data)

    return m


def generate_future(ui_params, model):
    # we need to specify the number of days in future
    future = model.make_future_dataframe(periods=ui_params.future_days)
    if ui_params.future_volume > 0:
        future['Volume'] = ui_params.future_volume
    return future


def predict(model, future):
    prediction = model.predict(future)
    return prediction
