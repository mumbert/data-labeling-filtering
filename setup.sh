#!/bin/bash

poetry config virtualenvs.in-project true
poetry install
poetry shell
pip install -r requirements.txt
git clone git@github.com:microsoft/DNS-Challenge.git
