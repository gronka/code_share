conf = {
    "client_id": "thisIdMatchesTheSsoBackend",
    "client_secret": "thisPasswordMatchesTheSsoBackend",
    "authorization_url": "https://oauth-site.com/v1/authorization.oauth2",
    "access_token_url": "https://oauth-site.com/v1/token.oauth2",
    "openid_url": "https://oauth-site.com/v1/userinfo.openid",
    "logout_url": "https://oauth-site.com/autho/logout.html",
    "sjwt_secret": "yOuCaNnEvErCrAcKtHiS",
}

class Semit:
    client_info_needs_update = 'client_info_needs_update'
    connection_established = 'connection_established'
    open_window = 'open_window'
    sso_signin_successful = 'sso_signin_successful'
    your_client_info = 'your_client_info'

