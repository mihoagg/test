import React, { useState, useEffect } from "react";
import { ethers } from "ethers";

const WalletConnect = () => {
  const [account, setAccount] = useState(null);

  useEffect(() => {
    if (window.ethereum) {
      window.ethereum.on("accountsChanged", handleAccountsChanged);
    }
    return () => {
      if (window.ethereum) {
        window.ethereum.removeListener(
          "accountsChanged",
          handleAccountsChanged
        );
      }
    };
  }, []);

  const handleAccountsChanged = (accounts) => {
    if (accounts.length === 0) {
      console.log("Please connect to MetaMask.");
    } else {
      setAccount(accounts[0]);
    }
  };

  const connectWallet = async () => {
    if (window.ethereum) {
      try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        await provider.send("eth_requestAccounts", []);
        const signer = provider.getSigner();
        const address = await signer.getAddress();
        setAccount(address);
      } catch (error) {
        console.error("Error connecting to MetaMask:", error);
      }
    } else {
      alert("MetaMask is not installed. Please install it to use this app.");
    }
  };

  return (
    <div>
      <h1>Wallet Connection Test</h1>
      {account ? (
        <p>Connected account: {account}</p>
      ) : (
        <button onClick={connectWallet}>Connect MetaMask</button>
      )}
    </div>
  );
};

export default WalletConnect;
