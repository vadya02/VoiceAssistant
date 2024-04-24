// store.ts
import axios from "axios";
import { makeAutoObservable, runInAction } from "mobx";
import { getHistory } from "../api/getHistory";
class AppStore {
	count = 0;
	response = "";
	isAuthenticated = null;
	links = [];
	authToken = localStorage.getItem("authToken");

	constructor() {
		makeAutoObservable(this);
	}

	setLinks(value) {
		this.isAuthenticated = value;
	}

	setIsAuthenticated(value) {
		this.isAuthenticated = value;
	}
	setResponse(value) {
		this.response = value;
	}

	getHistoryAction = async () => {
		try {
      const result = await getHistory()
      runInAction(() => {
        this.links = result
      })
    }
    catch{

    }
	};

  checkAuth = async () => {

    if(this.authToken) {
      // Если есть токен, проверяем его на сервере
      await axios({
        method: "GET",
        url: `${process.env.REACT_APP_URL_BACKEND}auth/users/me/`, // Замените на ваш URL для проверки авторизации
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
