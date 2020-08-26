Part 03 and 04 should work together once you make the needed configuration 
changes.

The basic process of SSO is:
1. navigate to our backends sso sign in kickoff point (/signin/sso/<sid>)
2. this route prepares SSO signin information and redirects the user to that
SSO url
3. after signin, SSO redirects back to our backend server to the URL which we
register with the SSO server. I registered /authorize/sso for my tests

I'm using jwts to basically store the user session, but I did not implement any
jwt health checks.
