import React from 'react';
import { king } from '../globals';


export function useIsSocketConnected(key: string) {
	const [isConnected, setIsConnected] = React.useState(false);

	React.useEffect(() => {
		function handleSocketChange(isConnected: boolean) {
				setIsConnected(isConnected);
		}
		king.sock.subscribeToIsSocketConnected(key, handleSocketChange);
		return () => {
			king.sock.unsubscribeToIsSocketConnected(key);
		}
	});

	return isConnected;
}


export function useIsSignedIn(key: string) {
	const [isSignedIn, setIsSignedIn] = React.useState(false);

	React.useEffect(() => {
		function handleAuthChange(isSignedIn: boolean) {
				setIsSignedIn(isSignedIn);
		}
		king.authService.subscribeToIsSignedIn(key, handleAuthChange);
		return () => {
			king.authService.unsubscribeToIsSignedIn(key);
		}
	});

	return isSignedIn;
}
