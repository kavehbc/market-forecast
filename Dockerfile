# docker build --progress=plain --no-cache -t market-analyzer .
# docker save -o market-analyzer.tar market-analyzer
# docker load --input market-analyzer.tar

FROM continuumio/miniconda3 AS build

# Updating conda
RUN conda update -n base -c defaults conda
# Installing git in case required by conda
RUN apt install git

WORKDIR /app
COPY . .

# Creating the environment
RUN conda env create -f environment.yml

# Installing conda-pack
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n myenv -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

# RUN conda clean -a -y

# The runtime-stage image
FROM debian:buster AS runtime
LABEL version="1.0.0"
LABEL maintainer="Kaveh Bakhtiyari"
LABEL url="http://bakhtiyari.com"
LABEL vcs-url="https://github.com/kavehbc/market-analyzer"
LABEL description="Cryptocurrency and Stocks Exchange Market Technical Analysis"

# Copy /venv from the previous stage
COPY --from=build /venv /venv

# Copy /app from the previous stage
COPY --from=build /app /app

WORKDIR /app
EXPOSE 8501

# Run the code with the environment activated
SHELL ["/bin/bash", "-c"]

# change file permision to prevent access denied error
RUN chmod +x run.bash

# ENTRYPOINT ["./run.bash"]
CMD ["./run.bash"]