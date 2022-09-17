import axios from "axios";

export default async function getTwitterId(handle) {
  return axios
    .get(
      "https://givewithporuka.pythonanywhere.com/v1/getTwitterIDs?names=" +
        handle
    )
    .then((res) => {
      return res.data.result;
    });
}
