FROM ucsdets/scipy-ml-notebook:2022.3-stable

LABEL org.opencontainers.image.source=https://github.com/nickthegroot/room-graph

RUN pip install --upgrade pip
RUN pip install poetry

# disable virtualenv for poetry
RUN poetry config virtualenvs.create false

# install dependencies
# older dependencies required on UCSD DSMLP server >:(
RUN pip install --no-cache-dir \
    torch-scatter==2.0.9 \
    torch-sparse==0.6.12 \
    torch-cluster==1.5.9 \
    torch-spline-conv==1.2.1 \
    torch-geometric==1.7.2 \
    -f https://pytorch-geometric.com/whl/torch-1.9.0+cu111.html
RUN pip install --no-cache-dir pytorch-lightning==1.4.9

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-cache --only main

# add source code
COPY ./data/test ./data/test
COPY ./Makefile Makefile
COPY ./models/example ./models/example
COPY ./roomgraph roomgraph
RUN poetry install --no-cache --only-root