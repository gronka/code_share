from authlib.integrations.requests_client import OAuth2Session
from flask import redirect, request, session
import json

from app import app
from conf import conf, Semit
from utils import build_redirect_uri
from state import scman


@app.route('/signin/sso/<sid>')
def signin_sso(sid):
    # Scope determines what data your access_token has access to. Use the
    # smallest scope possible. More options: ['email', 'openid', 'profile']
    client = OAuth2Session(
        conf['client_id'],
        redirect_uri=build_redirect_uri(),
        scope=['openid'])

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

    # token_dict returns the access token used for future requests, a refresh
    # token, client_id which is a JWT
    token_dict = client.fetch_token(
        conf['access_token_url'],
        client_secret=conf['client_secret'],
        authorization_response=request.url)

    sclient = scman.by_sid(session['sid'])
    sclient.sso_access_token = token_dict['access_token']
    sclient.get_openid_info()
    # emitting this event to the client  will initiate get_my_client_info
    sclient.private_emit(Semit.sso_signin_successful)

    # oauth_state is a CSRF token and sid will eventually be stale; remove them
    # so they aren't accidentally used in the future
    del session['oauth_state']
    del session['sid']

    return 'You are signed in - this window will close automatically. \
        <script>setTimeout(function () { window.close();}, 2000);</script>'


@app.route('/')
def hello_world():
    return 'Hello, World!'
