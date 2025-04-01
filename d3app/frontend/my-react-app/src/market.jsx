import React, { useState, useEffect } from "react";
import { ethers } from "ethers";
import contractABI from "../../../backend/artifacts/contracts/market.sol/NFTMarket.json"; // Import your contract's ABI

const contractAddress = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0"; // Add your contract's address here
const tokenAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

let signer = null;
let provider;

if (window.ethereum == null) {
  console.log("MetaMask not installed; using read-only defaults");
  provider = ethers.getDefaultProvider();
} else {
  provider = new ethers.BrowserProvider(window.ethereum);
  signer = await provider.getSigner();
}

const contract = new ethers.Contract(contractAddress, contractABI.abi, signer);

const Market = () => {
  const [nftContract, setNftContract] = useState("");
  const [tokenId, setTokenId] = useState("");
  const [price, setPrice] = useState("");
  const [message, setMessage] = useState("");
  const [retrievedNumber, setRetrievedNumber] = useState("");

  const listNFT = async () => {
    try {
      const tx = await contract.listNFT(
        nftContract,
        tokenId,
        ethers.parseEther(price)
      );
      await tx.wait();
      setMessage(`NFT with token ID ${tokenId} listed successfully!`);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
      console.error("Error listing NFT:", error);
    }
  };

  const buyNFT = async () => {
    try {
      const tx = await contract.buyNFT(tokenAddress, tokenId);
      await tx.wait();
      setMessage(`NFT with token ID ${tokenId} bought successfully!`);
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div>
      <h1>NFT Marketplace</h1>
      <div>
        <h2>List NFT</h2>
        <input
          type="text"
          placeholder="NFT Contract Address"
          value={nftContract}
          onChange={(e) => setNftContract(e.target.value)}
        />
        <input
          type="text"
          placeholder="Token ID"
          value={tokenId}
          onChange={(e) => setTokenId(e.target.value)}
        />
        <input
          type="text"
          placeholder="Price in ETH"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />
        <button onClick={listNFT}>List NFT</button>
      </div>
      <div>
        <h2>retrieve number</h2>
        <button onClick={retrieveNumber}>retrieve</button>
        <p>number: {retrievedNumber}</p>
      </div>
      <div>
        <h2>Buy NFT</h2>
        <input
          type="text"
          placeholder="Token ID"
          value={tokenId}
          onChange={(e) => setTokenId(e.target.value)}
        />
        <button onClick={buyNFT}>Buy NFT</button>
      </div>
      <p>{message}</p>
    </div>
  );
};

export default Market;
