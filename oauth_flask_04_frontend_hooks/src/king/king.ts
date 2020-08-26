import { Configuration } from '../conf';
import { AuthService } from '../services/auth';
import { Sock } from '../services/sock';

// king: rules and coordinates
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
