#!/usr/bin/env bash

export PATH=env/bin:$PATH

black run.py
isort run.py
