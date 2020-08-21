import { King } from '../king/king';
import { SubGroups } from './sub_groups';
import { Dictionary } from '../types';


const AuthStatus: Dictionary<string> = {
	'SIGNEDIN': 'SIGNEDIN',
	'SIGNEDOUT': 'SIGNEDOUT',
};


export class AuthService {
	openid: string = '';
	subGroups: SubGroups;
	king: King;
	status: string;

	constructor(king: King) {
		this.subGroups = new SubGroups();
		this.king = king;
		this.status = AuthStatus.SIGNEDOUT;
	}

	get isSignedIn() {
		return this.status === AuthStatus.SIGNEDIN;
	}

	initiateSsoSignin() {
		console.log('initiating sign in');
		this.king.sock.ssoSignin();
	}

	receiveSignin(openid: string, authStatus: string) {
		console.log('sign in received with openid ' + openid + 
								' and authStatus ' + authStatus);
		this.openid = openid;
		this.status = AuthStatus[authStatus];
		this.subGroups.broadcastUpdate('isSignedIn', this.isSignedIn);
	}

	initiateSsoSignout() {
		console.log('initiating sign out');
		this.king.sock.ssoSignout();
		// we don't need to broadcast isSignedIn here
	}

	subscribeToIsSignedIn(key: string, handler: Function) {
		this.subGroups.subscribe('isSignedIn', key, handler);
	}

	unsubscribeToIsSignedIn(key: string) {
		this.subGroups.unsubscribe('isSignedIn', key);
	}
}
