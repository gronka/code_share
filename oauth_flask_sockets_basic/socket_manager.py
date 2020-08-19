import jwt
import uuid

from conf import conf
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


class SocketClientManager:
    def __init__(self):
        self.quuid_to_client = {}
        self.sid_to_client = {}

    def on_client_connect_handler(self, client_sid, client_sjwt):
        decoded_sjwt = decode_sjwt(client_sjwt)

        client = None
        if 'quuid' in decoded_sjwt:
            # client recovered from sjwt
            client = self.by_quuid(decoded_sjwt['quuid'])
        if client is None:
            client = SocketClient(client_sid)

        self.add_client(client)

    def add_client(self, client):
        self.quuid_to_client[client.quuid] = client
        self.sid_to_client[client.sid] = client

    def remove_client(self, client):
        del self.quuid_to_client[client.quuid]
        del self.sid_to_client[client.sid]

    def by_quuid(self, quuid):
        return self.quuid_to_client.get(quuid)

    def by_sid(self, sid):
        return self.sid_to_client.get(sid)


class SocketClient:
    def __init__(self, sid, quuid=''):
        # openId (string): User's unique open id
        self.openId = ''
        self.sso_access_token = ''
        self.sid = sid

        if quuid == '':
            self.quuid = str(uuid.uuid4())
        else:
            self.quuid = quuid

    def make_sjwt(self):
        encoded_sjwt = encode_sjwt({'quuid': self.quuid})
        return encoded_sjwt

    def private_emit(self, event_name, data=None):
        socketio.emit(event_name, data, room=self.sid)

    def send_client_info(self):
        self.private_emit('your_client_info',
                          {'sjwt': self.make_sjwt(), 'openId': self.openId})
