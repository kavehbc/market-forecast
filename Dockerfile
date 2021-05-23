# docker build -t market-analyzer .
FROM alpine:3.8

RUN apk add --no-cache python3 python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

    RUN apk --update add --no-cache gcc freetype-dev libpng-dev

RUN apk add --no-cache --virtual .build-deps \
    musl-dev \
    g++

RUN pip install --no-cache-dir fbprophet

RUN pip install --no-cache-dir yfinance
RUN pip install --no-cache-dir streamlit

COPY . /app
WORKDIR /app
# RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["app.py"]