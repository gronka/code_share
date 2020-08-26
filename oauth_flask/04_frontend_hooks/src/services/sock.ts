import io from 'socket.io-client';
import { King } from '../king/king';
import { SubGroups } from './sub_groups';

enum Son {
	clientInfoNeedsUpdate = 'client_info_needs_update',
	connectionEstablished = 'connection_established',
	disconnect = 'disconnect',
	openWindow = 'open_window',
	reconnectAttempt = 'reconnect_attempt',
	ssoSigninSuccessful = 'sso_signin_successful',
	yourClientInfo = 'your_client_info',
}

enum Semit {
	printDebug = 'print_debug',
	getMyClientInfo = 'get_my_client_info',
	recoverOrNewSession = 'recover_or_new_session',
	ssoSignin = 'sso_signin',
	ssoSignout = 'sso_signout',
}


export class Sock {
	client: SocketIOClient.Socket;
	subGroups: SubGroups;
	king: King;
	sjwt: string;

	constructor(king: King) {
		this.subGroups = new SubGroups();
		this.king = king;
		this.sjwt = '';
		console.log('socket constructed');
		// NOTE: Using these transports will avoid triggering CORS if you need that
		//this.client = io('http://localhost:5000', 
										 //{transports: ['websocket', 'polling', 'flashsocket']});
		this.client = io('http://localhost:5000');
										 

		this.client.on(Son.connectionEstablished, () => {
			console.log(Son.connectionEstablished);
			this.recoverOrNewSession();
			this.subGroups.broadcastUpdate('isSocketConnected', true);
		});

		this.client.on(Son.disconnect, (reason: string) => {
			console.log('socket connection lost');
			this.subGroups.broadcastUpdate('isSocketConnected', false);
		});

		this.client.on(Son.yourClientInfo, (data: any) => {
			console.log(data);
			this.sjwt = data['sjwt'];
			this.king.authService.receiveSignin(data['openid'], data['auth_status']);
		});

		this.client.on(Son.clientInfoNeedsUpdate, () => {
			console.log('updating client info');
			this.getMyClientInfo();
		});
		
		this.client.on(Son.openWindow, (data: any) => {
			console.log('opening window to ' + data['url']);
			window.open(data['url']);
		});

		this.client.on(Son.ssoSigninSuccessful, (data: any) => {
			console.log('sign in was successful. getting new client info');
			this.getMyClientInfo();
		});
		
		this.client.on(Son.reconnectAttempt, () => {
			console.log('trying to reconnect');
		});
	}

	get isConnected() {
		return this.client.connected;
	}

	printDebug() {
		console.log('emitting print_debug');
		this.client.emit(Semit.printDebug, 'hey buddy');
	}

	recoverOrNewSession() {
		console.log('emitting recover or new session');
		this.client.emit(Semit.recoverOrNewSession, this.sjwt);
	}

	getMyClientInfo() {
		console.log('emitting getting client info');
		this.client.emit(Semit.getMyClientInfo);
	}

	ssoSignin() {
		console.log('emitting signin');
		this.client.emit(Semit.ssoSignin);  
	}

	ssoSignout() {
		console.log('emitting signout');
		this.client.emit(Semit.ssoSignout);  
	}

	subscribeToIsSocketConnected(key: string, handler: Function) {
		this.subGroups.subscribe('isSocketConnected', key, handler);
	}

	unsubscribeToIsSocketConnected(key: string) {
		this.subGroups.unsubscribe('isSocketConnected', key);
	}
}
