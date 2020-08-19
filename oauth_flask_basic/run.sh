#!/bin/sh

export FLASK_APP=app.py
export OAUTHLIB_INSECURE_TRANSPORT=1
flask run
