import { WalletIcon } from "@heroicons/react/24/outline";
import Lend from "./Lend";
import ConnectTwitter from "../Components/ConnectTwitter";
import fetchFollowers from "../helpers/fetchFollowers";
import { useEffect, useState } from "react";

export default function Connect({
  connectWallet,
  isConnected,
  isTwitterConnected,
  setIsTwitterConnected,
  twitterId,
  setTwitterId,
  setAllFollowers,
  allFollowers,
  injectedProvider,
  signer,
  userAddress
}) {
  return (
    <>
      {isConnected ? (
        isTwitterConnected ? (
          <Lend
            allFollowers={allFollowers}
            setAllFollowers={setAllFollowers}
            twitterId={twitterId}
            injectedProvider={injectedProvider}
            signer={signer}
            userAddress={userAddress}
          />
        ) : (
          <ConnectTwitter
            twitterId={twitterId}
            setTwitterId={setTwitterId}
            isTwitterConnected={isTwitterConnected}
            setIsTwitterConnected={setIsTwitterConnected}
          />
        )
      ) : (
        <div className="flex mx-20 mt-20">
          <button
            type="button"
            className="relative block w-full rounded-lg border-2 border-dashed border-gray-300 p-12 text-center hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            onClick={() => {
              connectWallet();
            }}
          >
            <WalletIcon className="mx-auto h-10 w-10" />
            <span className="mt-2 block text-sm font-medium text-gray-900">
              Connect wallet
            </span>
          </button>
        </div>
      )}
    </>
  );
}
