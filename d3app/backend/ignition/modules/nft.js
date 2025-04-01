const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");

module.exports = buildModule("NFTModule", (m) => {
  const myNFT = m.contract("MyNFT");

  m.call(myNFT, "mint", ["0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199", "ipfs://YourMetadataURI"]);

  return { myNFT };
});