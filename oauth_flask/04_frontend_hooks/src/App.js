import React from 'react';
import { king } from './globals';
import { useIsSignedIn, useIsSocketConnected } from './services/hooks';


function App() {
	const isSocketConnected = useIsSocketConnected('homepage');
	const isSignedIn = useIsSignedIn('homepage');

	function socketPrintDebug() {
		king.sock.printDebug();
	}

	function ssoSignin() {
		king.authService.initiateSsoSignin();
	}

	function ssoSignout() {
		king.authService.initiateSsoSignout();
	}

	function forceGetClientInfo() {
		king.sock.getMyClientInfo();
	}

  return (
    <div className="App">
			<br />
			<button onClick={socketPrintDebug}>socket print debug</button>
			<br />
			<br />
			<button onClick={ssoSignin}>Sign in</button>
			<br />
			<br />
			<button onClick={ssoSignout}>Sign out</button>
			<br />
			<br />
			<button onClick={forceGetClientInfo}>force get client info</button>

			{isSignedIn 
				? <p>You are signed in as {king.authService.openid}!</p>
				: <p>Signed out</p>
			}

			{isSocketConnected
				? <p>Connection established</p>
			  : <p>Socket disconnected!</p>
			}
    </div>
  );
}

export default App;
