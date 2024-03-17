# docker build --progress=plain --no-cache -t kavehbc/market-forecast .
# docker save -o market-forecast.tar kavehbc/market-forecast
# docker load --input market-forecast.tar

FROM python:3.9-buster

LABEL version="1.1.2"
LABEL maintainer="Kaveh Bakhtiyari"
LABEL url="http://bakhtiyari.com"
LABEL vcs-url="https://github.com/kavehbc/market-forecast"
LABEL description="Cryptocurrency and Stocks Exchange Market Forecast"

WORKDIR /app
COPY . .

# installing the requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]