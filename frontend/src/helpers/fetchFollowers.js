import axios from "axios";

export default async function fetchFollowers(id) {
  return axios
    .get("https://givewithporuka.pythonanywhere.com/getFollowing?id=" + id)
    .then((res) => {
      console.log("result within the function", res);
      return res.data.result;
    });
}
