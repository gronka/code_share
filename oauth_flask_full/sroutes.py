from flask import request, session

from app import socketio
from conf import conf, Semit
from utils import build_sso_uri
from state import scman


@socketio.on('connect')
def socket_connect():
    # when the client receives this event it will call get_my_client_info
    socketio.emit(Semit.connection_established, room=request.sid)
    print(f'client connected with sid {request.sid}' )


@socketio.on('recover_or_new_session')
def recover_or_new_session(client_sjwt):
    client = scman.on_client_connect_handler(request.sid, client_sjwt)
    client.send_client_info()
    print('recover or new session info sent')
    print(client.quuid)
    print(client.auth_status)


@socketio.on('get_my_client_info')
def get_my_client_info():
    client = scman.by_sid(request.sid)
    client.send_client_info()
    print('client info sent')
    print(client.quuid)
    print(client.auth_status)


@socketio.on('sso_signin')
def socket_sso_signin():
    client = scman.by_sid(request.sid)
    client.private_emit(Semit.open_window, {'url': build_sso_uri(request.sid)})


@socketio.on('sso_signout')
def socket_sso_signout():
    client = scman.by_sid(request.sid)
    scman.remove_client(client)
    client.private_emit(Semit.open_window, {'url': conf['logout_url']})


@socketio.on('print_debug')
def socket_print_debug(message):
    print('======= PRINT DEBUG =========')
    print(f'request_has_sid: {request.sid}')
    client = scman.by_sid(request.sid)
    print('client info printed below')
    print(f'sid: {client.sid}')
    print(f'quuid: {client.quuid}')
    print(f'openid: {client.openid}')
    print(f'====end print debug. client says "{message}"')

