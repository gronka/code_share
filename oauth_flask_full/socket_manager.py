from flask_socketio import join_room
import jwt
import requests
import uuid

from conf import conf, Semit
from app import socketio

# SocketClientManager is to linkt a client_uuid (quuid) with the websocket sid
# so that http routes can lookup websocket clients and emit messages to
# them. It also allows us to store some state about each client, such as if
# the client is already SSO authenticated.
# An alternative solution would be to simply pass data in the session. However,
# this leads to two possibilities:
#
#   1. we require the user to sign in on each new tab
#   2. we store a lookup of the user's credentials in the session
#
# Option 1 is not a seamless experience.
# Option 2 is a security flaw, since it would be very simple for a user to
# spoof their session credential, guessing and checking against the server
# until they got it right. A solution here would be to introduce encryption -
# but then we would be rolling our own security, which is no good.
#
# By using JWTs and storing data in a separate datastore, we gain the benefit
# of encryption without overloading the purpose of the session variable.

def encode_sjwt(data):
    return jwt.encode(data, conf['sjwt_secret'], algorithm='HS256')


def decode_sjwt(data):
    if data == '':
        return {}
    return jwt.decode(data, conf['sjwt_secret'], algorithm='HS256')


class AuthStatus:
    SIGNEDIN = 'SIGNEDIN'
    SIGNEDOUT = 'SIGNEDOUT'


class SocketClientManager:
    def __init__(self):
        self.quuid_to_client = {}
        self.sid_to_client = {}

    def on_client_connect_handler(self, client_sid, client_sjwt):
        decoded_sjwt = decode_sjwt(client_sjwt)

        client = None
        if 'quuid' in decoded_sjwt:
            # client recovered from sjwt; server restart wipes lookup
            client = self.by_quuid(decoded_sjwt['quuid'])
        if client is None:
            client = SocketClient(client_sid, self)

        self.add_client(client)
        client.join_room(client.quuid)
        return client

    def add_client(self, client):
        self.quuid_to_client[client.quuid] = client
        self.sid_to_client[client.sid] = client

    def remove_client(self, client):
        del self.quuid_to_client[client.quuid]
        del self.sid_to_client[client.sid]
        client.signout_emit()
        client.signout()

    def by_quuid(self, quuid):
        return self.quuid_to_client.get(quuid)

    def by_sid(self, sid):
        return self.sid_to_client.get(sid)


class SocketClient:
    def __init__(self, sid, scman):
        self.auth_status = AuthStatus.SIGNEDOUT
        self.scman = scman
        # openid (string): User's unique open id
        self.openid = ''
        self.sso_access_token = ''
        self.sid = sid if sid else ''
        self.quuid = str(uuid.uuid4())

        self.sjwt = self.make_sjwt()

    def get_openid_info(self):
        resp = requests.get(
            conf['openid_url'],
            headers={'Authorization': f'Bearer {self.sso_access_token}'})
        try:
            jso = resp.json()
            if 'sub' in jso:
                self.openid = jso['sub']
                self.auth_status = AuthStatus.SIGNEDIN
            else:
                self.signout()
        except json.decoder.JSONDecodeError:
            self.signout()

    def is_signed_in():
        return self.auth_status == AuthStatus.SIGNEDIN

    def signout(self):
        self.openid = ''
        self.auth_status = AuthStatus.SIGNEDOUT
        self.private_emit(Semit.client_info_needs_update)

    def make_sjwt(self):
        encoded_sjwt = encode_sjwt({'quuid': self.quuid})
        return encoded_sjwt

    def is_sjwt_stale(self):
        # TODO: return true if sjwt is expired
        pass

    def join_room(self, room):
        join_room(room, self.sid)

    # private_emit uses the quuid, so it will reach all sockets a user owns
    def private_emit(self, event_name, data=None):
        socketio.emit(event_name, data, room=self.quuid)

    # private_emit_sid will only go to a single socket that a user owns
    def private_emit_sid(self, event_name, data=None):
        socketio.emit(event_name, data, room=self.sid)

    def signout(self):
        self.jwt = ''
        self.openid = ''
        self.sso_access_token = ''
        self.auth_status = AuthStatus.SIGNEDOUT

    def signout_emit(self):
        self.private_emit(Semit.your_client_info,
                          {'sjwt': '',
                           'openid': '',
                           'auth_status': 'SIGNEDOUT'})

    def send_client_info(self):
        if self.is_sjwt_stale() and self.is_signed_in():
            self.scman.remove_client(self)
        else:
            self.private_emit(Semit.your_client_info,
                        {'sjwt': self.sjwt,
                         'openid': self.openid,
                         'auth_status': self.auth_status})
