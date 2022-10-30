# DSC 180 Q1 Project

> :paperclip: https://dsc-capstone.github.io/assignments/projects/q1/

## Local Development

This project uses the following tools.
- Python 3.10
- [Poetry](https://python-poetry.org/)

With both installed, run `poetry install` to setup your python venv.

## Downloading the Data

The data can be found [here](https://zenodo.org/record/2613548). The original paper was created using Version 1.0 of the dataset. Simply download the `cubicasa5k.zip` file, unzip it, and edit `config/data-params.yaml` to reflect the location.

By default, the config assumes the zip file is located in `data/raw`. If you have httpie installed, this can be quickly downloaded by running the following from the project root:

```sh
mkdir data/raw
http -d -o data/raw/cubicasa5k.zip "https://zenodo.org/record/2613548/files/cubicasa5k.zip?download=1"
unzip data/raw/cubicasa5k.zip
rm -rf data/raw/cubicasa5k.zip
```
