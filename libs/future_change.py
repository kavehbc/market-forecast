import streamlit as st
import datetime
import numpy as np
import pandas as pd


def highlight_negative(s):
    return ['color: red;'] * len(s) if s.Change < 0 else ['color: green'] * len(s)


def display_future_change(ui_params, data, filtered_prediction):
    if ui_params.model == "fbprophet":
        yhat_label_low = "yhat_lower"
        yhat_label_mid = "yhat"
        yhat_label_high = "yhat_upper"
    elif ui_params.model == "neuralprophet":
        yhat_label_low = "yhat1"
        yhat_label_mid = "yhat1"
        yhat_label_high = "yhat1"

    last_day_price = data[data["ds"] == data["ds"].max()].iloc[0]["y"]

    # next day predictions
    next_day_price_low = filtered_prediction[filtered_prediction["ds"] == filtered_prediction["ds"].min()].iloc[0][
        yhat_label_low]
    next_day_price_mid = filtered_prediction[filtered_prediction["ds"] == filtered_prediction["ds"].min()].iloc[0][
        yhat_label_mid]
    next_day_price_high = filtered_prediction[filtered_prediction["ds"] == filtered_prediction["ds"].min()].iloc[0][
        yhat_label_high]

    # next day predictions (change)
    next_day_change_low = next_day_price_low - last_day_price
    next_day_change_percentage_low = (next_day_change_low / last_day_price) * 100

    next_day_change_mid = next_day_price_mid - last_day_price
    next_day_change_percentage_mid = (next_day_change_mid / last_day_price) * 100

    next_day_change_high = next_day_price_high - last_day_price
    next_day_change_percentage_high = (next_day_change_high / last_day_price) * 100

    # next year predictions
    last_future_day_price_low = \
        filtered_prediction[filtered_prediction["ds"] == filtered_prediction["ds"].max()].iloc[0][yhat_label_low]
    last_future_day_price_mid = \
        filtered_prediction[filtered_prediction["ds"] == filtered_prediction["ds"].max()].iloc[0][yhat_label_mid]
    last_future_day_price_high = \
        filtered_prediction[filtered_prediction["ds"] == filtered_prediction["ds"].max()].iloc[0][yhat_label_high]

    # next year predictions (change)
    future_day_change_low = last_future_day_price_low - last_day_price
    future_day_change_percentage_low = (future_day_change_low / last_day_price) * 100

    future_day_change_mid = last_future_day_price_mid - last_day_price
    future_day_change_percentage_mid = (future_day_change_mid / last_day_price) * 100

    future_day_change_high = last_future_day_price_high - last_day_price
    future_day_change_percentage_high = (future_day_change_high / last_day_price) * 100

    # getting next day and next year dates
    last_day_date = datetime.datetime.date(data["ds"].max())
    next_day_price_date = datetime.datetime.date(filtered_prediction["ds"].min())
    last_future_day_price_date = datetime.datetime.date(filtered_prediction["ds"].max())

    st.write(f"Base line ({last_day_date}): {last_day_price:,.2f}")

    # df_future_change = pd.DataFrame(
    #     np.array(
    #         [[next_day_price_date, float(next_day_price), float(next_day_change), float(next_day_change_percentage)],
    #          [last_future_day_price_date, float(last_future_day_price), float(future_day_change),
    #           float(future_day_change_percentage)]]),
    #     columns=['Date', 'New Price', 'Change', 'Change %'])

    # df_future_change = df_future_change.style.format({"New Price": "{:.2f}",
    #                                                   "Change": "{:.2f}",
    #                                                   "Change %": "{:.2f}%"}) \
    #     .apply(highlight_negative, axis=1)
    # st.write(df_future_change)

    if ui_params.model == "fbprophet":
        st.subheader("Tomorrow")
        st_metric_next_day_low, st_metric_next_day_mid, st_metric_next_day_high = st.columns(3)
        st.subheader("Next Year")
        st_metric_next_year_low, st_metric_next_year_mid, st_metric_next_year_high = st.columns(3)

        # next day (Tomorrow)
        st_metric_next_day_low.metric(label=f"Low {next_day_price_date}",
                                      value=f"{next_day_price_low:,.4f}",
                                      delta=f"{next_day_change_low:,.4f} | {next_day_change_percentage_low:,.4f}%")
        st_metric_next_day_mid.metric(label=f"Mid {next_day_price_date}",
                                      value=f"{next_day_price_mid:,.4f}",
                                      delta=f"{next_day_change_mid:,.4f} | {next_day_change_percentage_mid:,.4f}%")
        st_metric_next_day_high.metric(label=f"High {next_day_price_date}",
                                       value=f"{next_day_price_high:,.4f}",
                                       delta=f"{next_day_change_high:,.4f} | {next_day_change_percentage_high:,.4f}%")

        # next year
        st_metric_next_year_low.metric(label=f"Low {last_future_day_price_date}",
                                       value=f"{last_future_day_price_low:,.4f}",
                                       delta=f"{future_day_change_low:,.4f} | {future_day_change_percentage_low:,.4f}%")
        st_metric_next_year_mid.metric(label=f"Mid {last_future_day_price_date}",
                                       value=f"{last_future_day_price_mid:,.4f}",
                                       delta=f"{future_day_change_mid:,.4f} | {future_day_change_percentage_mid:,.4f}%")
        st_metric_next_year_high.metric(label=f"High {last_future_day_price_date}",
                                        value=f"{last_future_day_price_high:,.4f}",
                                        delta=f"{future_day_change_high:,.4f} | {future_day_change_percentage_high:,.4f}%")

    elif ui_params.model == "neuralprophet":
        st_header_next_day_mid, st_header_next_year_mid = st.columns(2)
        st_header_next_day_mid.subheader("Tomorrow")
        st_header_next_year_mid.subheader("Next Year")

        st_metric_next_day_mid, st_metric_next_year_mid = st.columns(2)
        st_metric_next_day_mid.metric(label=f"Mid {next_day_price_date}",
                                      value=f"{next_day_price_mid:,.4f}",
                                      delta=f"{next_day_change_mid:,.4f} | {next_day_change_percentage_mid:,.4f}%")
        st_metric_next_year_mid.metric(label=f"Mid {last_future_day_price_date}",
                                       value=f"{last_future_day_price_mid:,.4f}",
                                       delta=f"{future_day_change_mid:,.4f} | {future_day_change_percentage_mid:,.4f}%")
