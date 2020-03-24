#!/usr/bin/env bash

export FLASK_APP=server.py
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000