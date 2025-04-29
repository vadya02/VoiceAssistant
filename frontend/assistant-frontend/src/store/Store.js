// store.ts
import axios from "axios";
import { makeAutoObservable } from "mobx";
class AppStore {
	count = 0;
	response = "";
  filtersResponse = "";
	isAuthenticated = null;
	links = [];
	authToken = localStorage.getItem("authToken");
  checkResult = false;
	constructor() {
		makeAutoObservable(this);
	}

	setLinks(value) {
		this.links = value;
	}

	setIsAuthenticated(value) {
		this.isAuthenticated = value;
	}
  setCheckResult(value) {
		this.checkResult = value;
	}
	setResponse(value) {
		this.response = value;
	}
  setFiltersResponse(value) {
		this.filtersResponse = value;
	}

	getHistoryAction = async () => {
		await axios
    .get(`${process.env.REACT_APP_URL_BACKEND}get_history_of_requests/`, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Token ${localStorage.getItem("authToken")}`,
      },
    })
    .then((response) => {
      // this.setLinks(JSON.parse(response.data) )
      this.links = response.data
      console.log('links: ' + store.links)
      console.log('история запросов: ' + JSON.parse(response.data))
      // return response.data
    })
    .catch((error) => {
      // return error
    });
	};

  checkAuth = async () => {

    if(this.authToken) {
      await axios({
        method: "GET",
        url: `${process.env.REACT_APP_URL_BACKEND}auth/users/me/`, 
        headers: {
          Authorization: `Token ${this.authToken}`,
        },
      })
        .then(() => {
          this.setIsAuthenticated(true);
          console.log('login successfull');
        })
        .catch((error) => {
          localStorage.removeItem("authToken");
          console.log("Ошибка проверки авторизации:", error);
          this.setIsAuthenticated(false);
        });
    }
  }

	
}

const store = new AppStore();
export default store;
