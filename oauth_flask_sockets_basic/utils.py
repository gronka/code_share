from flask import url_for


def build_redirect_uri():
    redirect_uri = url_for(f"authorize_sso", _external=True)
    return redirect_uri.replace("127.0.0.1", "localhost")


def build_sso_uri(sid):
    redirect_uri = url_for(f"signin_sso", sid=sid, _external=True)
    return redirect_uri.replace("127.0.0.1", "localhost")
