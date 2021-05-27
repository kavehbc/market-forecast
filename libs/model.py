from fbprophet import Prophet


def create_model(ui_params, data, st_app_status_placeholder):
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

    st_app_status_placeholder.info("Training started. It may take a while...")
    m.fit(data)
    st_app_status_placeholder.empty()

    return m


def predict(ui_params, model, st_app_status_placeholder):
    st_app_status_placeholder.info("Generating the future dataset...")
    # we need to specify the number of days in future
    future = model.make_future_dataframe(periods=ui_params.future_days)
    if ui_params.future_volume > 0:
        future['Volume'] = ui_params.future_volume

    st_app_status_placeholder.info("Forecasting the future...")
    prediction = model.predict(future)
    st_app_status_placeholder.empty()

    return prediction
