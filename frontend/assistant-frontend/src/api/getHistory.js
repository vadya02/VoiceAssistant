
import axios from "axios";
import store from "../store/Store";
export const getHistory = async () => {
  await axios
    .get(`${process.env.REACT_APP_URL_BACKEND}get_history_of_requests/`, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Token ${localStorage.getItem("authToken")}`,
      },
    })
    .then((response) => {
      store.setLinks(JSON.parse(response.data) )

      console.log('links: ' + store.links)
      console.log('история запросов: ' + JSON.parse(response.data))
      return response.data
    })
    .catch((error) => {
      return error
    });
};