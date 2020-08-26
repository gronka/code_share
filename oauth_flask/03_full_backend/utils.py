from flask import url_for
from conf import conf


# NOTE: I only added this step of changing 127.0.0.1 to localhost since my
# testing endpoints were registed to localhost
def build_redirect_uri():
    redirect_uri = url_for(f"authorize_sso", _external=True)
    return redirect_uri.replace("127.0.0.1", "localhost")


def build_sso_uri(sid):
    redirect_uri = url_for(f"signin_sso", sid=sid, _external=True)
    return redirect_uri.replace("127.0.0.1", "localhost")
