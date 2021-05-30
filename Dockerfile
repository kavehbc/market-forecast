# docker build --progress=plain --no-cache -t market-analyzer .
# docker save -o market-analyzer.tar market-analyzer
# docker load --input market-analyzer.tar

FROM python:3.8-buster

LABEL version="1.0.0"
LABEL maintainer="Kaveh Bakhtiyari"
LABEL url="http://bakhtiyari.com"
LABEL vcs-url="https://github.com/kavehbc/market-analyzer"
LABEL description="Cryptocurrency and Stocks Exchange Market Technical Analysis"

WORKDIR /app
COPY . .

# installing the requirements
RUN pip install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]