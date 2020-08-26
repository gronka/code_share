#!/bin/sh

#export FLASK_APP=main.py
#flask run

export SESSION_COOKIE_SECURE=True
# TODO: disable this in production
export OAUTHLIB_INSECURE_TRANSPORT=1
python main.py
