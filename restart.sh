#! /bin/bash

python3 -m venv env
. env/bin/activate
pip install --upgrade pip setuptools pkg-resources
pip install -r requirements.txt
