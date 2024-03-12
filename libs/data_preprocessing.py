def prepare_hisotry_for_fbprophet(ui_params, df_history):
    # data preparation
    df_history_prep = df_history.reset_index()

    # selecting the correct date column
    date_column = "Date" if "Date" in df_history_prep.columns else 'Datetime'

    if ui_params.future_volume > 0:
        data = df_history_prep[[date_column, ui_params.price_column, "Volume"]]
    else:
        data = df_history_prep[[date_column, ui_params.price_column]]  # select Date and Price
    data = data.rename(columns={date_column: "ds", ui_params.price_column: "y"})

    return data
