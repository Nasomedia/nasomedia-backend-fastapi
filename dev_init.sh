#! /usr/bin/env bash

# Run Poetry Install 
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
# Add poetry bin to PATH 
cat "export PATH=$PATH:$HOME/.poetry/bin" >> $HOME/.bashrc
# Set poetry config to no virtualenvs
poetry config virtualenvs.create false

# install dependencies
poetry install

# Let the DB start
python /app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/initial_data.py
