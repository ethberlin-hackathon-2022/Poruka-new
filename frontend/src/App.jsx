import "./App.css";
import Landing from "./Views/Landing";
import { Routes, Route } from "react-router-dom";
import React from "react";
import { useState, useEffect } from "react";
import { ethers } from "ethers";
import Web3Modal from "web3modal";
import WalletConnectProvider from "@walletconnect/web3-provider";
import { useNavigate } from "react-router-dom";
import Lend from "./Views/Lend";
import Connect from "./Views/Connect";
import Navbar from "./Components/Navbar";
import isTwitterResolved from "./helpers/isTwitterResolved";
import getTwitterId from "./helpers/getTwitterId";
import { Network } from './utils/config';

const INFURA_ID = "f17f31ea210e43ca91b886804c49a9b8";


function App() {
  const [address, setAddress] = useState(null);
  const [signer, setSigner] = useState(null);
  const [injectedProvider, setInjectedProvider] = useState();
  const [connectedNetwork, setConnectedNetwork] = useState();
  const [web3Modal, setWeb3Modal] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isTwitterConnected, setIsTwitterConnected] = useState(false);
  const [twitterId, setTwitterId] = useState(0);
  const navigate = useNavigate();
  const [allFollowers, setAllFollowers] = useState([]);

  const addListeners = (provider) => {
    provider.on("chainChanged", (chainId) => {
      console.log(`chain changed to ${chainId}! updating providers`);
      setInjectedProvider(new ethers.providers.Web3Provider(provider));
    });

    provider.on("accountsChanged", () => {
      console.log("account changed!");
      setInjectedProvider(new ethers.providers.Web3Provider(provider));
      localStorage.removeItem("user_id");
      window.location.reload();
    });

    // Subscribe to session disconnection
    provider.on("disconnect", (code, reason) => {
      console.log(code, reason);
      logoutOfWeb3Modal();
      localStorage.removeItem("supa_token");
      localStorage.removeItem("user_id");
      setIsConnected(false);
    });
  };

  useEffect(() => {
    // initiate web3modal
    const providerOptions = {
      walletconnect: {
        package: WalletConnectProvider,
        options: {
          bridge: "https://polygon.bridge.walletconnect.org",
          infuraId: INFURA_ID,
          rpc: {
            1: `https://${Network}.infura.io/v3/${INFURA_ID}`,
            100: "https://dai.poa.network", // xDai
          },
        },
      },
    };

    const newWeb3Modal = new Web3Modal({
      cacheProvider: true, // very important
      network: Network,
      providerOptions,
    });

    setWeb3Modal(newWeb3Modal);
  }, []);

  async function connectWallet() {
    const web3provider = await web3Modal.connect();

    addListeners(web3provider);

    const provider = new ethers.providers.Web3Provider(web3provider);
    setInjectedProvider(provider);

    const signer = await provider.getSigner();
    setSigner(signer);

    const network = await provider.getNetwork();
    setConnectedNetwork(network.name);
    const address = await signer.getAddress();
    setAddress(address);
    const isTwitter = await isTwitterResolved(address);
    if (isTwitter !== "") {
      setIsTwitterConnected(true);
      const handle = isTwitter;
      const id = getTwitterId(handle);
      setTwitterId(id);
    }
    setIsConnected(true);
  }

  const logoutOfWeb3Modal = async () => {
    await web3Modal.clearCachedProvider();
    if (
      injectedProvider &&
      injectedProvider.provider &&
      typeof injectedProvider.provider.disconnect === "function"
    ) {
      await injectedProvider.provider.disconnect();
    }
    setTimeout(() => {
      window.location.reload();
    }, 1);
  };

  useEffect(() => {
    // connect automatically and without a popup if user is already connected
    if (web3Modal && web3Modal.cachedProvider) {
      connectWallet();
    }
  }, [web3Modal]);


  return (
    <>
      <Navbar
        connectWallet={connectWallet}
        logoutOfWeb3Modal={logoutOfWeb3Modal}
        isConnected={isConnected}
      />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route
          path="lend"
          element={
            <Lend
              allFollowers={allFollowers}
              twitterId={twitterId}
              setAllFollowers={setAllFollowers}
              injectedProvider={injectedProvider}
              signer={signer}
              userAddress={address}
            />
          }
        />
        <Route
          path="connect"
          element={
            <Connect
              connectWallet={connectWallet}
              isConnected={isConnected}
              isTwitterConnected={isTwitterConnected}
              setIsTwitterConnected={setIsTwitterConnected}
              twitterId={twitterId}
              setTwitterId={setTwitterId}
              allFollowers={allFollowers}
              setAllFollowers={setAllFollowers}
              injectedProvider={injectedProvider}
              signer={signer}
              userAddress={address}
            />
          }
        />
      </Routes>
    </>
  );
}

export default App;
