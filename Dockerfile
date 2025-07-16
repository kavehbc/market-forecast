# docker build --progress=plain --no-cache -t kavehbc/market-forecast:latest -t kavehbc/market-forecast:1.1.4 .
# docker save -o market-forecast.tar kavehbc/market-forecast
# docker load --input market-forecast.tar

FROM python:3.11-slim

LABEL version="1.1.4"
LABEL maintainer="Kaveh Bakhtiyari"
LABEL url="http://bakhtiyari.com"
LABEL vcs-url="https://github.com/kavehbc/market-forecast"
LABEL description="Cryptocurrency and Stocks Exchange Market Forecast"

# Set environment variables for Python and Streamlit
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501

WORKDIR /app

# Use .dockerignore to avoid copying unnecessary files (add .dockerignore in your project)
COPY . .

# Upgrade pip and install requirements, then clean up cache
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
