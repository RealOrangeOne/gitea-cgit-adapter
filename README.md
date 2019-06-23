# gitea-cgit-adapter

Export public gitea repos in a way cgit understands

## Installation

1. `python -m venv env`
2. `env/bin/pip install -e .`
3. `env/bin/python run.py <gitea app.ini> <cgitrepos>

A systemd service is provided for convenience
