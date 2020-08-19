from authlib.integrations.requests_client import OAuth2Session
from flask import redirect, request, session

from app import app
from conf import conf
from utils import build_redirect_uri


@app.route("/signin/sso")
def signin_sso():
    client = OAuth2Session(
        conf["client_id"],
        redirect_uri=build_redirect_uri(),
    )

    uri, state = client.create_authorization_url(
        conf["authorization_url"])
    session["oauth_state"] = state
    return redirect(uri)


@app.route("/authorize/sso")
def authorize_sso():
    client = OAuth2Session(
        conf["client_id"],
        redirect_uri=build_redirect_uri(),
        state=session["oauth_state"],
    )
    del session['oauth_state']  # oauth_state is a CSRF token

    token_dict = client.fetch_token(
        conf["access_token_url"],
        client_secret=conf["client_secret"],
        authorization_response=request.url,
    )

    session['sso_access_token'] = token_dict['access_token']

    return "You are signed in. You may now close this window."


@app.route('/')
def hello_world():
    return 'Hello, World!'
