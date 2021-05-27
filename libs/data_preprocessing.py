def prepare_hisotry_for_fbprophet(ui_params, df_history):
    # data preparation
    df_history_prep = df_history.reset_index()
    if ui_params.future_volume > 0:
        data = df_history_prep[["Date", "Close", "Volume"]]
    else:
        data = df_history_prep[["Date", "Close"]]  # select Date and Price
    data = data.rename(columns={"Date": "ds", "Close": "y"})

    return data
