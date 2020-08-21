let protocol = "http://"
let url = "127.0.0.1"
let port = ":9090"
let apiVersion = "/v1"
let cxApi = protocol + url + port + apiVersion

export interface Configuration {
	env: string,
	apiUrl: string,
	whichApi: string,
	webRequestTimeout: number,
}

export const conf: Configuration = {
	env: "dev",
	apiUrl: cxApi,
	whichApi: "mock",
	webRequestTimeout: 1,
}
