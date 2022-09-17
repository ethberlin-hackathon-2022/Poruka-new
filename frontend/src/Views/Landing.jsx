import { ReactComponent as Hero } from "../Images/hero.svg";
import { Link } from "react-router-dom";
import Navbar from "../Components/Navbar";

export default function Landing({
  connectWallet,
  logoutOfWeb3Modal,
  isConnected,
}) {
  return (
    <>
      <div className="flex mx-20 mt-20 justify-between">
        <div className="flex items-center">
          <div className="">
            <p className="font-extrabold text-7xl">Lend to fam</p>
            <p className="w-3/4 text-3xl mt-10 font-light leading-10">
              Give and get access to financial support by vouching for people
              you know
            </p>
            <Link to="/connect">
              <button
                type="button"
                className="inline-flex mt-10 items-center rounded-full border border-gray-600 px-4 py-2 text-base font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                Go to app
              </button>
            </Link>
          </div>
        </div>
        <div>
          <Hero />
        </div>
      </div>
    </>
  );
}
