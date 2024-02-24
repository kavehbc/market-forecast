# Cryptocurrency & Stock Market Forecast (Predictive AI)

Like many, I used to track Crypto and Stock progress either for investment or curiosity.
There are numerous amount of recommendations from financial advisors, traders, investors, business analysts, brokers
and so on available on Internet, and interestingly, sometimes, there are contradicting each other.

This is a fun open-source project in `streamlit` using `Facebook Prophet` and `Neural Prophet` to analyze and forecast
Stock and Crypto-currency market based on their historical price only.
The data is extracted from Yahoo! Finance using the `yfinance` library.

> **Warning:** This tool neither recommends nor guarantees the performance of the given symbol.
> Use this tool and its forecasts at your own risk.

## Demo
You can access the demo version deployed on Streamlit server at:

[https://stock-market.streamlit.app/](https://stock-market.streamlit.app/)

## Run
In order to run this tool, you must have Streamlit installed on your machine/environment:

    streamlit run app.py

## Run on Docker
This application is available on [Docker Hub](https://hub.docker.com/r/kavehbc/market-analyzer), and it can be run directly using:

    docker run -p 80:8501 kavehbc/market-forecast

Once you run it, you can open it in your browser on [http://127.0.0.1](http://127.0.0.1).

## GitHub Repo
This project is open-source, and it is available on GitHub at [https://github.com/kavehbc/market-forecast](https://github.com/kavehbc/market-analyzer).

## Usage Tracking
### User Hits/Views
The app usage is tracked using [statcounter.com](https://statcounter.com/),
and it does not contain any personal information. The file containing the script is located at
`injection\statcounter.html`.

Injection functions are managed inside `libs\injection.py`.

### Searched Tickers/Symbols
The searched tickers are stored in `db\popular.json` file.
This file is being used for the autocomplete feature on the ticker's text input field.
The functions related to the data storage and retrieval are managed inside `libs\db.py`.

This database is stored where the app is hosted, and it does not transmit these data elsewhere automatically.

## Limitations

1. `Recommendation` section is removed since `yfinance` module can not decrypt data.


## Developer(s)
Kaveh Bakhtiyari - [Website](http://bakhtiyari.com) | [Medium](https://medium.com/@bakhtiyari)
  | [LinkedIn](https://www.linkedin.com/in/bakhtiyari) | [GitHub](https://github.com/kavehbc)

## Contribution
Feel free to join the open-source community and contribute to this repository.
