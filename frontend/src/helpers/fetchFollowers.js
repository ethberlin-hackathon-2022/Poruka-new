import axios from "axios";

export default async function fetchFollowers(id) {
  axios
    .get("https://givewithporuka.pythonanywhere.com/getFollowing?id=" + id)
    .then((res) => {
      return res.data.result;
    });
}
