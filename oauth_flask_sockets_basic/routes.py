from authlib.integrations.requests_client import OAuth2Session
from flask import redirect, request, session
import requests

from app import app
from conf import conf
from utils import build_redirect_uri
from state import scman


@app.route('/signin/sso/<sid>')
def signin_sso(sid):
    client = OAuth2Session(
        conf['client_id'],
        redirect_uri=build_redirect_uri(),
        scope=['email', 'openid', 'profile'])

    uri, state = client.create_authorization_url(conf['authorization_url'])
    session['oauth_state'] = state
    session['sid'] = sid
    return redirect(uri)


@app.route('/authorize/sso')
def authorize_sso():
    client = OAuth2Session(
        conf['client_id'],
        redirect_uri=build_redirect_uri(),
        state=session['oauth_state'])

    token_dict = client.fetch_token(
        conf['access_token_url'],
        client_secret=conf['client_secret'],
        authorization_response=request.url)
    print(token_dict)

    client = scman.by_sid(session['sid'])
    client.sso_access_token = token_dict['access_token']
    # when the client receives this event it will call get_my_client_info
    client.private_emit('sso_signin_successful')

    # oauth_state is a CSRF token and sid will eventually be stale; remove them
    # so they aren't accidentally used in the future
    del session['oauth_state']
    del session['sid']

    return 'You are signed in - closing window.<script>window.close()</script>'


@app.route('/')
def hello_world():
    return 'Hello, World!'
