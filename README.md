# data-labeling-filtering
ML project for getting metadata from a speech dataset

## Description

The aim of this project is to generate metadata and label it using automated labelling tools and models. The goal is to convert an unlabelled dataset into one with more rich annotations that can be used to train more kinds of models with increased capabilities. The voxCeleb1 test dataset has been used as an example.

For each analyzed file of the dataset several metadata is extracted which can be used later on to filter. This is an example of what can be extracted in json format:
```shell
    "data/vox1_test/wav/id10295/nt7dNRvlEHE/00005.wav": {
        "file": "data/vox1_test/wav/id10295/nt7dNRvlEHE/00005.wav",
        "id": "id10295",
        "framerate": 16000,
        "nchannels": 1,
        "sampwidth": 2,
        "duration": 4.8000625,
        "text": " Egyptian guy was telling me that Dubai is amazing. He said, but it's summer. Stay.",
        "language": "en",
        "arousal": 0.3700000047683716,
        "dominance": 0.47999998927116394,
        "valence": 0.6800000071525574,
        "age": 44,
        "female": -0.8799999952316284,
        "male": 4.570000171661377,
        "child": -2.7699999809265137,
        "gender": "male",
        "OVRL": 3.0891271529377544,
        "SIG": 3.6527983022435517,
        "BAK": 3.5731412216384366
    },
```

For more information:
- check this [readme](docs/README_labeling.md) on the labeling process
- check this [readme](docs/README_filtering.md) on the filtering processes
- check this [readme](docs/README_improvements.md) on future improvements

## Installation

### Pre-requisites

- poetry
```shell
pip install poetry
```

### Setting up python environment

Run the [setup.sh](setup.sh) scrip which is in charge of:
- creating an environment and install dependencies
- since some packages cannot be installed directly with poetry use the requirements.txt file within the poetry environemnt for these extra packages
- clone external repo DNSMOS

```shell
#!/bin/bash

poetry config virtualenvs.in-project true
poetry install
poetry shell
pip install -r requirements.txt
git clone git@github.com:microsoft/DNS-Challenge.git
```