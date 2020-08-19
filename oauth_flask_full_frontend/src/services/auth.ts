import { King } from '../king/king';
import { ForceUpdateGroup } from './force_update_group';
import { Dictionary } from '../types';


const AuthStatus: Dictionary<string> = {
	'SIGNEDIN': 'SIGNEDIN',
	'SIGNEDOUT': 'SIGNEDOUT',
};


export class AuthService {
	openid: string = '';
	forceUpdateGroup: ForceUpdateGroup;
	king: King;
	status: string;

	constructor(king: King) {
		this.forceUpdateGroup = new ForceUpdateGroup(['authChange']);
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
		this.forceUpdateGroup.forceUpdates('authChange');
	}

	initiateSsoSignout() {
		console.log('initiating sign out');
		this.king.sock.ssoSignout();
		this.forceUpdateGroup.forceUpdates('authChange');
	}
}
