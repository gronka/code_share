import React from 'react';
import { king } from './globals';

function App() {
	const [, forceUpdate] = React.useReducer(x => x + 1, 0);

	// Force re-rendering when socket disconnects and reconnects
	React.useEffect(() => {
		king.sock.forceUpdateGroup.subscribe('socketChange', forceUpdate);
		return function cleanup() {
			king.sock.forceUpdateGroup.unsubscribe('socketChange', forceUpdate);
		};
	}, []);

	// Force re-rendering when auth status changes
	React.useEffect(() => {
		king.authService.forceUpdateGroup.subscribe('authChange', forceUpdate);
		return function cleanup() {
			king.authService.forceUpdateGroup.unsubscribe('authChange', forceUpdate);
		};
	}, []);

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

			{king.authService.isSignedIn 
				? <p>You are signed in as {king.authService.openid}!</p>
				: <p>Signed out</p>
			}

			{king.sock.client.disconnected
			  ? <p>Socket disconnected!</p>
				: <p>Connection established</p>
			}
    </div>
  );
}

export default App;
