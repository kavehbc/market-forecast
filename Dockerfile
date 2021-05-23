# docker build --progress=plain --no-cache -t market-analyzer .
# docker save -o market-analyzer.tar market-analyzer
FROM continuumio/miniconda3:4.9.2-alpine
RUN conda update -n base -c defaults conda
RUN conda install -c conda-forge fbprophet
RUN conda install -c anaconda pip
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit","run"]
CMD ["app.py"]

# removing dependencies
RUN apk del .build-deps