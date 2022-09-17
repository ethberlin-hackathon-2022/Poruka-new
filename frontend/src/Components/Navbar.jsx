import { ReactComponent as Logo } from "../Images/navlogo.svg";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Navbar({
  connectWallet,
  logoutOfWeb3Modal,
  isConnected,
}) {
  const [isLanding, setIsLanding] = useState(false);

  useEffect(() => {
    var url = window.location.pathname;
    console.log(url);
    if (url === "/") {
      setIsLanding(true);
    } else {
      setIsLanding(false);
    }
  }, [window.location.pathname]);

  const GoToApp = () => {
    return (
      <Link to="/connect">
        <button
          type="button"
          className="inline-flex mt-10 items-center rounded-full border border-gray-600 px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          Go to app
        </button>
      </Link>
    );
  };

  const ConnectWallet = () => {
    return (
      <Link to="/connect">
        <button
          type="button"
          className="inline-flex mt-10 items-center rounded-full border border-gray-600 px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          onClick={() => {
            connectWallet();
          }}
        >
          Connect
        </button>
      </Link>
    );
  };

  const Logout = () => {
    return (
      <Link to="/connect">
        <button
          type="button"
          className="inline-flex mt-10 items-center rounded-full border border-gray-600 px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          onClick={() => {
            logoutOfWeb3Modal();
          }}
        >
          Logout
        </button>
      </Link>
    );
  };

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

            {isLanding ? (
              <GoToApp />
            ) : isConnected ? (
              <Logout />
            ) : (
              <ConnectWallet />
            )}
          </div>
        </nav>
      </header>
    </>
  );
}
