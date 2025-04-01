const { buildModule } = require("@nomicfoundation/hardhat-ignition/modules");

module.exports = buildModule("NFTMarketModule", (m) => {
  const myNFT = m.contract("NFTMarket");

  return { myNFT };
});