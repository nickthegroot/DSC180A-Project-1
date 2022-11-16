# DSC 180 Q1 Project

> :paperclip: https://dsc-capstone.github.io/assignments/projects/q1/

## Local Development

This project uses the following tools.

- Python 3.10
- Mamba/Conda

With both installed, run `make requirements` to setup your python venv.

## Downloading the Data

The data can be found [here](https://zenodo.org/record/2613548). The original paper was created using Version 1.0 of the dataset. Simply download the `cubicasa5k.zip` file, unzip it, and edit `config/data-params.yaml` to reflect the location.

By default, the config assumes the zip file is located in `data/raw`. This can easily be created by running `make data`.
