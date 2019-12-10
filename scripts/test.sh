#!/usr/bin/env bash

set -e

PATH=env/bin:${PATH}

black --check run.py
flake8 run.py
isort -c run.py
mypy run.py
