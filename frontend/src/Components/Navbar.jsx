import { ReactComponent as Logo } from "../Images/navlogo.svg";
import axios from "axios";
import { redirect } from "react-router-dom";

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

  return (
    <>
      <header className="">
        <nav
          className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
          aria-label="Top"
        >
          <div className="w-full py-4 flex items-center justify-between">
            <div className="flex items-center text-black font-phosphate text-3xl">
              <Logo height={50} width={50} />
              <div className="ml-3 text-3xl">Poruka</div>
            </div>
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
