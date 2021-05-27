# Cryptocurrency & Stock Exchange Market Technical Analysis

Like many, I used to track Crypto and Stock progress either for investment or curiosity.
There are numerous amount of recommendations from financial advisors, traders, investors, business analysts, brokers
and so on available on Internet, and interestingly, sometimes, there are contradicting each other.

This is a fun open-source project in `streamlit` using `Facebook Prophet` to analyze and forecast
Stock and Crypto-currency market based on their historical price only.
The data is extracted from Yahoo! Finance using the `yfinance` library.

> **Warning:** This tool neither recommends nor guarantees the performance of the given ticker.
> Use this tool and its forecasts at your own risk.

## Demo
You can access the demo version deployed on Streamlit server at:

[https://share.streamlit.io/kavehbc/market-analyzer/app.py](https://share.streamlit.io/kavehbc/market-analyzer/app.py)

## Run
In order to run this tool, you must have Streamlit installed on your machine/environment:

    streamlit run app.py

## Run on Docker
This application is available on [Docker Hub](https://hub.docker.com/r/kavehbc/market-analyzer), and it can be run directly using:

    docker run -p 8501:80 kavehbc/market-analyzer

Once you run it, you can open it in your browser on [http://127.0.0.1](http://127.0.0.1).

## Github Repo
This project is open-source, and it is available on Github at [https://github.com/kavehbc/market-analyzer](https://github.com/kavehbc/market-analyzer).

## Developer(s)
Kaveh Bakhtiyari - [Website](http://bakhtiyari.com) | [Medium](https://medium.com/@bakhtiyari)
  | [LinkedIn](https://www.linkedin.com/in/bakhtiyari) | [Github](https://github.com/kavehbc)

## Contribution
Feel free to join the open-source community and contribute to this repository.