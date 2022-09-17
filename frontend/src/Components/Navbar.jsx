import { ReactComponent as Logo } from "../Images/navlogo.svg";
import axios from "axios";
import { Link } from "react-router-dom";
import { useEffect } from "react";

export default function Navbar({
  connectWallet,
  logoutOfWeb3Modal,
  isConnected,
}) {
  const connectTwitter = async () => {
    axios.get("https://givewithporuka.pythonanywhere.com/auth").then((res) => {
      console.log(res);
      window.open(res.data.url);
    });
  };

  useEffect(() => {
    var url = new URL(window.location.href);
    var id = url.searchParams.get("id");
    var username = url.searchParams.get("username");
    var img = url.searchParams.get("img");
    console.log("id:", id);
    console.log("username:", username);
    console.log("img:", img);
  }, []);

  return (
    <>
      <header className="">
        <nav
          className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
          aria-label="Top"
        >
          <div className="w-full py-4 flex items-center justify-between">
            <Link to="/">
              <div className="flex items-center text-black font-phosphate text-3xl">
                <Logo height={50} width={50} />
                <div className="ml-3 text-3xl">Poruka</div>
              </div>
            </Link>
            {isConnected ? (
              <button
                type="button"
                className="inline-flex items-center rounded-full border border-gray-600 px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                onClick={() => logoutOfWeb3Modal()}
              >
                logout
              </button>
            ) : (
              <>
                <button
                  type="button"
                  className="inline-flex items-center rounded-full border border-gray-600 px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                  onClick={() => connectWallet()}
                >
                  Connect wallet
                </button>
                <button
                  type="button"
                  className="inline-flex items-center rounded-full border border-gray-600 px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                  onClick={() => connectTwitter()}
                >
                  Connect Twitter
                </button>
              </>
            )}
          </div>
        </nav>
      </header>
    </>
  );
}
