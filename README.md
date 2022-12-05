# Roomplan Graph Prediction

## Description

This project was created for UCSD's DSC 180A: Data Science Capstone. According to the university, the course:

> Span(s) the entire lifecycle, including assessing the problem, learning domain knowledge, collecting/cleaning data, creating a model, addressing ethical issues, designing the system, analyzing the output, and presenting the results.
>
> https://catalog.ucsd.edu/courses/DSC.html#dsc180a

## Setup

### Installing Dependencies

Make sure you have Python 3.10 on your system, then run

```sh
poetry install
```

### Downloading Data

This project uses the Cubicasa5k dataset, which can be found [here](https://zenodo.org/record/2613548). To download the entire dataset into the default location (`data/raw`), run:

```sh
make download
```

## Preprocessing Data

In order for the model to train at maximum speed, we preprocess all the data into PyG format. To do this, run the following command after downloading the data:

```sh
poetry run make_dataset --buffer-pct [pct] [input_dir] [output_dir]
```

where `pct` is the percentage (0-1) of the dataset to use, `input_dir` is the directory containing the raw Cubicasa data, and `output_dir` is the directory to save the processed data to.

By default, `pct` is .03, `input_dir` is `data/raw`, and `output_dir` is `data/processed`.

## Training the Model

You must have a CUDA-enabled GPU to train the model. CPU support may come at a later date.

First, you must create a run config file. This file is a JSON file that contains all the parameters for training the model. These generally live in the `models/` directory. You can use the `models/example.json` file as a template.

To train the model, run the following command:

```sh
poetry run train [config_file]
```

To view Tensorboard logs of the running/completed training, run:

```sh
make tensorboard
```

## Project Organization

    ├── Makefile           <- Makefile with commands like `make download`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   └── raw            <- The original, immutable data dump.
    │   └── processed      <- The PyG processed data.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a YYMMDD date (for ordering),
    │                         the creator's username, and a short `-` delimited description, e.g.
    │                         `221128-nickthegroot-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── roomgraph                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes recipe_recommendation a Python module
    │   │
    │   ├── cli            <- Scripts used for training, validating, etc
    │   │   └── train.py
    │   ├── data           <- Scripts to download or generate data
    │   ├── models         <- Scripts to train models and then use trained models to make

---

<small>
Project based on the <a href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a></small>
```
