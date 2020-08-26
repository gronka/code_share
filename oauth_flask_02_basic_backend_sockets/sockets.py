from flask import request

from app import socketio
from utils import build_sso_uri
from state import scman


@socketio.on('connect')
def socket_connect():
    # when the client receives this event it will call get_my_client_info
    socketio.emit('connection_established', room=request.sid)
    print(f'client connected with sid {request.sid}' )


@socketio.on('get_my_client_info')
def get_my_client_info(client_sjwt):
    scman.on_client_connect_handler(request.sid, client_sjwt)
    client = scman.by_sid(request.sid)
    client.send_client_info()


@socketio.on('sso_signin')
def socket_sso_signin():
    print('signing in')
    client = scman.by_sid(request.sid)
    client.private_emit('open_sso_signin_window', {'ssoUrl': build_sso_uri(request.sid)})


@socketio.on('print_debug')
def socket_print_debug(message):
    print('======= PRINT DEBUG =========')
    print(f'request_has_sid: {request.sid}')
    client = scman.by_sid(request.sid)
    print('client info:')
    print(f'sid: {client.sid}')
    print(f'quuid: {client.quuid}')
    print(f'openId: {client.openId}')
    print('====end print debug. client says "{message}"')

