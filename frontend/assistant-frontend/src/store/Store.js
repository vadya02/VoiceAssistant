// store.ts
import { makeAutoObservable } from "mobx";

class AppStore {
  count= 0;
  response = ''
  isAuthenticated = false
  constructor() {
    makeAutoObservable(this);
  }

  increment() {
    this.count++;
  }

  decrement() {
    this.count--;
  }


  setIsAuthenticated (value) {
    this.isAuthenticated = value
  }
  setResponse (value) {
    this.response = value
  }
}

const store = new AppStore();
export default store;
