#!/bin/sh

# sockets don't use flask run
#export FLASK_APP=main.py
#flask run

# TODO: disable this when https is set up
export OAUTHLIB_INSECURE_TRANSPORT=1
python main.py
