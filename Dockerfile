FROM ucsdets/datahub-base-notebook:2022.3-stable

LABEL org.opencontainers.image.source=https://github.com/nickthegroot/DSC180A-Project-1

RUN mamba install --yes pytorch=1.13.0 -c pytorch
RUN mamba install --yes pyg=2.1.0 -c pyg

RUN pip install --no-cache-dir \
    beautifulsoup4==4.11.1 \
    geopandas==0.12.1 \
    lxml==4.9.1 \
    matplotlib==3.6.2 \
    numpy==1.23.4 \
    pytorch-lightning==1.7.7 \
    pyyaml==6.0

COPY data/test data/test

COPY setup.py setup.py
COPY config config
COPY run.py run.py

COPY roomgraph/ roomgraph/