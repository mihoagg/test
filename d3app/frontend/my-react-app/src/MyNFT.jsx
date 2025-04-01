import React, { useState } from "react";
import { ethers } from "ethers";
import contractABI from "../../../backend/artifacts/contracts/nft.sol/MyNFT.json";

const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3";

const MyNFT = () => {
  const [account, setAccount] = useState(null);
  const [accounts, setAccounts] = useState([]);
  const [recipient, setRecipient] = useState("");
  const [tokenId, setTokenId] = useState("");
  const [metadataURI, setMetadataURI] = useState("");
  const [price, setPrice] = useState("");
  const [message, setMessage] = useState("");
  const [nftContract, setNftContract] = useState(null);
  const [marketAddress, setMarketAddress] = useState("");

  const connectWallet = async () => {
    if (window.ethereum) {
      try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        const accounts = await provider.send("eth_requestAccounts", []);
        setAccounts(accounts);
        if (accounts.length > 0) {
          setAccount(accounts[0]);
        }
        const contract = new ethers.Contract(
          contractAddress,
          contractABI.abi,
          signer
        );
        setNftContract(contract);
      } catch (error) {
        console.error("Error connecting to MetaMask:", error);
      }
    } else {
      alert("MetaMask is not installed. Please install it to use this app.");
    }
  };

  const handleAccountChange = (event) => {
    setAccount(event.target.value);
  };

  const mintNFT = async () => {
    if (!nftContract) {
      console.error("Contract is not initialized");
      return;
    }
    try {
      const tx = await nftContract.mint(account, metadataURI);
      await tx.wait();
    } catch (error) {
      console.error("Error minting NFT:", error);
    }
  };

  const payToMintNFT = async () => {
    if (!nftContract) {
      console.error("Contract is not initialized");
      return;
    }
    try {
      const tx = await nftContract.payToMint(account, metadataURI, {
        value: ethers.parseEther("0.05"),
      });
      await tx.wait();
    } catch (error) {
      console.error("Error minting NFT:", error);
    }
  };

  const transferNFT = async () => {
    if (!nftContract) {
      console.error("Contract is not initialized");
      return;
    }
    try {
      const tx = await nftContract.transferFrom(account, recipient, tokenId);
      await tx.wait();
    } catch (error) {
      console.error("Error transferring NFT:", error);
    }
  };

  const approveNFT = async () => {
    if (!nftContract) {
      console.error("Contract is not initialized");
      return;
    }
    try {
      const tx = await nftContract.approve(recipient, tokenId);
      await tx.wait();
    } catch (error) {
      console.error("Error approving NFT:", error);
    }
  };

  const approveForAll = async () => {
    if (!nftContract) {
      console.error("Contract is not initialized");
      return;
    }
    try {
      const tx = await nftContract.setApprovalForAll(
        marketAddress,
        Boolean(true)
      );
      await tx.wait();
    } catch (error) {
      console.error("Error approving NFT:", error);
    }
  };

  const burnNft = async () => {
    if (!nftContract) {
      console.error("Contract is not initialized");
      return;
    }
    try {
      const tx = await nftContract.burn(tokenId);
      await tx.wait();
    } catch (error) {
      console.error("Error Burning NFT:", error);
    }
  };

  return (
    <div>
      <h1>MyNFT DApp</h1>
      {account ? (
        <div>
          <p>Connected account: {account}</p>
          <div>
            <label htmlFor="account-select">Select Account:</label>
            <select
              id="account-select"
              value={account}
              onChange={handleAccountChange}
            >
              {accounts.map((acc) => (
                <option key={acc} value={acc}>
                  {acc}
                </option>
              ))}
            </select>
          </div>
          <div>
            <h2>Mint NFT</h2>
            <input
              type="text"
              placeholder="Metadata URI"
              value={metadataURI}
              onChange={(e) => setMetadataURI(e.target.value)}
            />
            <button onClick={mintNFT}>Mint</button>
            <button onClick={payToMintNFT}>Pay to Mint</button>
          </div>
          <div>
            <h2>Transfer NFT</h2>
            <input
              type="text"
              placeholder="Recipient Address"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
            />
            <input
              type="text"
              placeholder="Token ID"
              value={tokenId}
              onChange={(e) => setTokenId(e.target.value)}
            />
            <button onClick={transferNFT}>Transfer</button>
          </div>
          <div>
            <h2>Approve NFT</h2>
            <input
              type="text"
              placeholder="Recipient Address"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
            />
            <input
              type="text"
              placeholder="Token ID"
              value={tokenId}
              onChange={(e) => setTokenId(e.target.value)}
            />
            <button onClick={approveNFT}>Approve</button>
            <h2>Approve For All</h2>
            <input
              type="text"
              placeholder="market address"
              value={marketAddress}
              onChange={(e) => setMarketAddress(e.target.value)}
            />
            <button onClick={approveForAll}>Approve For All</button>
            <h2>List NFT</h2>
          </div>
          <div>
            <h2>Burn NFT</h2>
            <input
              type="text"
              placeholder="Token ID"
              value={tokenId}
              onChange={(e) => setTokenId(e.target.value)}
            />
            <button onClick={burnNft}>Burn</button>
          </div>
        </div>
      ) : (
        <button onClick={connectWallet}>Connect MetaMask</button>
      )}
    </div>
  );
};

export default MyNFT;
