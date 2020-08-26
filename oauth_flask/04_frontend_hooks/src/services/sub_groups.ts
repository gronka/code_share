import { Dictionary } from '../types';


// SubGroups are for subscribing to events. Subscribers provide a name of the
// event they want to subscribe to, and provide a unique key to identify
// themselves.
export class SubGroups {
	groups: Dictionary<Dictionary<Function>> = {};

	constructor() {
		this.groups = {};
	}

	// Subscriptions are made using the subscription name and a key. They key 
	// references the component which wants to receive updates. It must be unique.
	subscribe(subName: string, key: string, updateFunction: Function) {
		console.log("sub hook function for: " + subName+":"+key);
		if (subName in this.groups) {
			this.groups[subName][key] = updateFunction;
		} else {
			this.groups[subName] = {};
			this.groups[subName][key] = updateFunction;
		}
	}

	unsubscribe(subName: string, key: string) {
		console.log("unsub hook function for: " + subName+":"+key);
		delete this.groups[subName][key];
	}

	broadcastUpdate(subName: string, newValue: any) {
		console.log("updating hooks for group " + subName);
		// NOTE: sometimes a broadcast can be sent before a component finishes
		// rendering
		if (subName in this.groups) {
			for (const [, subscriber] of Object.entries(this.groups[subName])) {
				subscriber(newValue);
			}
		}
	}
}
