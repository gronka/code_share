import { Configuration } from '../conf';
import { AuthService } from '../services/auth';
import { Sock } from '../services/sock';

// King controls and coordinates incidents in the kingdom. He gives 
// commands to Viceroys (usually services)
export class King {
	authService: AuthService;
	conf: Configuration;
	sock: Sock;

	constructor(conf: Configuration) {
		this.conf = conf;
		this.authService = new AuthService(this);
		this.sock = new Sock(this);
	}
}
