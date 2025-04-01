import React, { useState, useEffect } from "react";
import { ethers } from "ethers";
import contractABI from "../../../backend/artifacts/contracts/nft.sol/MyNFT.json";

const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

const Account = () => {
  const [address, setAddress] = useState("");
  const [balance, setBalance] = useState(null);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  let provider;

  if (window.ethereum == null) {
    console.log("MetaMask not installed; using read-only defaults");
    provider = ethers.getDefaultProvider();
  } else {
    provider = new ethers.BrowserProvider(window.ethereum);
  }

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const accounts = await provider.listAccounts();
        if (accounts.length > 0) {
          setAddress(accounts[0]);
          setIsConnected(true);
        }
      } catch (err) {
        console.error(err);
      }
    };
    checkConnection();
  }, []);

  const connectAccount = async () => {
    try {
      await provider.send("eth_requestAccounts", []);
      const signer = provider.getSigner();
      const account = await signer.getAddress();
      setAddress(account);
      setIsConnected(true);
      setError(null);
    } catch (err) {
      setError("Error connecting to MetaMask");
    }
  };

  const changeAccount = async () => {
    try {
      await provider.send("wallet_requestPermissions", [{ eth_accounts: {} }]);
      const accounts = await provider.listAccounts();
      if (accounts.length > 0) {
        setAddress(accounts[0]);
        setIsConnected(true);
        setError(null);
      }
    } catch (err) {
      setError("Error changing account");
    }
  };

  const getBalance = async () => {
    try {
      if (!ethers.utils.isAddress(address)) {
        setError("Invalid Ethereum address");
        setBalance(null);
        return;
      }
      setError(null);
      const balance = await provider.getBalance(address);
      setBalance(ethers.formatEther(balance));
    } catch (err) {
      setError("Error fetching balance");
      setBalance(null);
    }
  };

  return (
    <div>
      <h1>Ethereum Balance Checker</h1>
      {!isConnected ? (
        <button onClick={connectAccount}>Connect Account</button>
      ) : (
        <>
          <button onClick={changeAccount}>Change Account</button>
          <button onClick={getBalance}>Check Balance</button>
        </>
      )}
      {balance && <p>Balance: {balance} ETH</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};

export default Account;
