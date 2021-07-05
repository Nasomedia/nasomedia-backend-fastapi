#! /usr/bin/env bash

# Run Poetry Install 
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
# Add poetry bin to PATH 
echo "export PATH=\$PATH:\$HOME/.poetry/bin" >> $HOME/.bashrc
source ~/.bashrc

# Set poetry config to no virtualenvs
poetry config virtualenvs.create true

# install dependencies
poetry install

# Let the DB start
PYTHONPATH=/nasomedia-backend-workspace/ python ./app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
PYTHONPATH=/nasomedia-backend-workspace/ python ./app/initial_data.py
