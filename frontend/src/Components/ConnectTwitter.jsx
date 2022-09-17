import { useEffect } from "react";
import axios from "axios";
import { ChatBubbleLeftIcon } from "@heroicons/react/24/outline";

export default function ConnectTwitter({
  twitterId,
  allFollowers,
  setTwitterId,
}) {
  const connectTwitter = async () => {
    axios.get("https://givewithporuka.pythonanywhere.com/auth").then((res) => {
      console.log(res);
      window.open(res.data.url, "_self");
    });
  };

  useEffect(() => {
    var url = new URL(window.location.href);
    var id = url.searchParams.get("id");
    var username = url.searchParams.get("username");
    var img = url.searchParams.get("img");
    setTwitterId(id);
    console.log("id:", id);
    console.log("username:", username);
    console.log("img:", img);
    window.localStorage.setItem("twitter_id", id);
    window.localStorage.setItem("twitter_name", username);
    window.localStorage.setItem("twitter_photo", img);
  }, []);
  return (
    <div className="flex mx-20 mt-20">
      <button
        type="button"
        className="relative block w-full rounded-lg border-2 border-dashed border-gray-300 p-12 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        onClick={() => {
          connectTwitter();
        }}
      >
        <ChatBubbleLeftIcon className="mx-auto h-10 w-10" />
        <span className="mt-2 block text-sm font-medium text-gray-900">
          Connect your Twitter account
        </span>
      </button>
    </div>
  );
}
