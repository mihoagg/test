import React, { useState, useEffect } from "react";
import Web3 from "web3";
import MyContractABI from "../../../backend/artifacts/contracts/nft.sol/MyNFT.json";

const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3"; // Replace with your contract address

function App() {
  const [mintData, setMintData] = useState({ to: "", metadataURI: "" });
  const [transferData, setTransferData] = useState({
    from_address: "",
    to_address: "",
    token_id: "",
  });
  const [approveData, setApproveData] = useState({
    to_address: "",
    token_id: "",
  });
  const [response, setResponse] = useState(null);
  const [account, setAccount] = useState(null);
  const [web3, setWeb3] = useState(null);
  const [myContract, setMyContract] = useState(null);
  const [nftList, setNftList] = useState([]); // State for NFT list

  useEffect(() => {
    if (window.ethereum) {
      const web3Instance = new Web3(window.ethereum);
      setWeb3(web3Instance);
      const contractInstance = new web3Instance.eth.Contract(
        MyContractABI.abi,
        contractAddress
      );
      setMyContract(contractInstance);
    } else {
      console.error("MetaMask not detected");
    }
  }, []);

  const connectMetaMask = async () => {
    if (web3) {
      try {
        await window.ethereum.request({ method: "eth_requestAccounts" });
        const accounts = await web3.eth.getAccounts();
        setAccount(accounts[0]);
        fetchNFTs(accounts[0]); // Fetch NFTs after connecting
      } catch (error) {
        console.error("Error connecting to MetaMask:", error);
      }
    }
  };

  const fetchNFTs = async (account) => {
    try {
      const balance = await myContract.methods.balanceOf(account).call();
      const nfts = [];
      for (let i = 0; i < balance; i++) {
        const tokenId = await myContract.methods
          .tokenOfOwnerByIndex(account, i)
          .call();
        const tokenURI = await myContract.methods.tokenURI(tokenId).call();
        nfts.push({ tokenId, tokenURI });
      }
      setNftList(nfts);
    } catch (error) {
      console.error("Error fetching NFTs:", error);
    }
  };

  const handleChange = (e, setData) => {
    const { name, value } = e.target;
    setData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e, endpoint, data) => {
    e.preventDefault();
    try {
      if (!window.ethereum) {
        throw new Error("MetaMask is not installed");
      }

      await window.ethereum.request({ method: "eth_requestAccounts" });

      const accounts = await window.ethereum.request({
        method: "eth_accounts",
      });
      const account = accounts[0];

      let tx;
      if (endpoint === "mint") {
        if (!data.to || !Web3.utils.isAddress(data.to)) {
          throw new Error("Invalid 'to' address");
        }
        tx = myContract.methods.mint(data.to, data.metadataURI);
      } else if (endpoint === "transfer") {
        if (!data.from_address || !Web3.utils.isAddress(data.from_address)) {
          throw new Error("Invalid 'from' address");
        }
        if (!data.to_address || !Web3.utils.isAddress(data.to_address)) {
          throw new Error("Invalid 'to' address");
        }
        tx = myContract.methods.transferFrom(
          data.from_address,
          data.to_address,
          data.token_id
        );
      } else if (endpoint === "approve") {
        if (!data.to_address || !Web3.utils.isAddress(data.to_address)) {
          throw new Error("Invalid 'to' address");
        }
        tx = myContract.methods.approve(data.to_address, data.token_id);
      }

      const transactionParameters = {
        from: account,
        to: contractAddress,
        gasPrice: "0x9184e72a000",
        value: "0x0",
        data: tx.encodeABI(),
      };

      const txHash = await window.ethereum.request({
        method: "eth_sendTransaction",
        params: [transactionParameters],
      });
      console.log("Transaction sent with hash:", txHash);
    } catch (error) {
      setResponse(error.message);
    }
  };

  return (
    <div className="App">
      <h1>NFT Operations</h1>

      {!account ? (
        <button onClick={connectMetaMask}>Connect MetaMask</button>
      ) : (
        <div>
          <p>Connected Account: {account}</p>

          <h2>Mint NFT</h2>
          <form onSubmit={(e) => handleSubmit(e, "mint", mintData)}>
            <input
              type="text"
              name="to"
              placeholder="To Address"
              value={mintData.to}
              onChange={(e) => handleChange(e, setMintData)}
            />
            <input
              type="text"
              name="metadataURI"
              placeholder="Metadata URI"
              value={mintData.metadataURI}
              onChange={(e) => handleChange(e, setMintData)}
            />
            <button type="submit">Mint</button>
          </form>

          <h2>Transfer NFT</h2>
          <form onSubmit={(e) => handleSubmit(e, "transfer", transferData)}>
            <input
              type="text"
              name="from_address"
              placeholder="From Address"
              value={transferData.from_address}
              onChange={(e) => handleChange(e, setTransferData)}
            />
            <input
              type="text"
              name="to_address"
              placeholder="To Address"
              value={transferData.to_address}
              onChange={(e) => handleChange(e, setTransferData)}
            />
            <input
              type="number"
              name="token_id"
              placeholder="Token ID"
              value={transferData.token_id}
              onChange={(e) => handleChange(e, setTransferData)}
            />
            <button type="submit">Transfer</button>
          </form>

          <h2>Approve NFT</h2>
          <form onSubmit={(e) => handleSubmit(e, "approve", approveData)}>
            <input
              type="text"
              name="to_address"
              placeholder="To Address"
              value={approveData.to_address}
              onChange={(e) => handleChange(e, setApproveData)}
            />
            <input
              type="number"
              name="token_id"
              placeholder="Token ID"
              value={approveData.token_id}
              onChange={(e) => handleChange(e, setApproveData)}
            />
            <button type="submit">Approve</button>
          </form>

          <h2>Your NFTs</h2>
          <ul>
            {nftList.map((nft) => (
              <li key={nft.tokenId}>
                <p>Token ID: {nft.tokenId}</p>
                <p>Metadata URI: {nft.tokenURI}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {response && (
        <div>
          <h3>Response:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
