
import axios from "axios";

export const getHistory = async () => {
  await axios
    .get(`${process.env.REACT_APP_URL_BACKEND}get_history_of_requests/`, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Token ${localStorage.getItem("authToken")}`,
      },
    })
    .then((response) => {
      return response.data
    })
    .catch((error) => {
      return error
    });
};