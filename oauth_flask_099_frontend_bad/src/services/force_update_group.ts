import { Dictionary } from '../types';

// FoceUpdateGroup is used to manually command components on the front end to 
// update. For example: when data is retrieved from an API, the data on the 
// backend will update, but since we're not using a mobx-like state handler, 
// the frontend has no way of knowing it needs to refresh. 
//
// To use force update, you need a fake line in your component such as
// const [, forceUpdate] = React.useReducer(x => x + 1, 0);
export class ForceUpdateGroup {
	groups: Dictionary<Function[]> = {};

	// initialGroups parameter is required because it is possible for objects 
	// that don't live in the DOM such as websocket to call forceUpdateGroup 
	// before the DOM is rendered
	constructor(initialGroups: string[] = []) {
		for (let i = 0; i < initialGroups.length; i++) {
			let groupName = initialGroups[i];
			this.groups[groupName] = [];
		}
	}

	subscribe(uuid: string, updateFunction: Function) {
		console.log("subscribing forceUpdate function for: " + uuid);
		if (uuid in this.groups) {
			this.groups[uuid].push(updateFunction);
		} else {
			this.groups[uuid] = [];
			this.groups[uuid].push(updateFunction);
		}
	}

	unsubscribe(uuid: string, updateFunction: Function) {
		console.log("unsubscribing forceUpdate function for: " + uuid);
		const index = this.groups[uuid].indexOf(updateFunction);
		if (index > -1) {
			this.groups[uuid].splice(index, 1);
		}
	}

	forceUpdates(uuid: string) {
		console.log("forcing update for group " + uuid);
		for (let i = 0; i < this.groups[uuid].length; i++) {
			this.groups[uuid][i]();
		}
	}
}
