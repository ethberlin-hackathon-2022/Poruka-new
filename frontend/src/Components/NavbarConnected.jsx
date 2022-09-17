import { ReactComponent as Logo } from "../Images/navlogo.svg";
import { Link } from "react-router-dom";
import { useEffect } from "react";

export default function NavbarConnected({
  connectWallet,
  logoutOfWeb3Modal,
  isConnected,
}) {
  useEffect(() => {
    var url = new URL(window.location.href);
    var id = url.searchParams.get("id");
    var username = url.searchParams.get("username");
    var img = url.searchParams.get("img");
    console.log("id:", id);
    console.log("username:", username);
    console.log("img:", img);
    window.localStorage.setItem("twitter_id", id);
    window.localStorage.setItem("twitter_name", username);
    window.localStorage.setItem("twitter_photo", img);
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
          </div>
        </nav>
      </header>
    </>
  );
}
