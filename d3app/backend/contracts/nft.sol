// SPDX-License-Identifier: MIT
pragma solidity 0.8.29;

import {ERC721URIStorage, ERC721} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721URIStorage, Ownable {
    uint256 public nextTokenId;
    mapping(uint256 => string) private _metadataURIs;

    constructor() ERC721("MyNFT", "MNFT") Ownable(msg.sender) {}

    function mint(address to, string memory metadataURI) public onlyOwner {
        uint256 tokenId = nextTokenId;
        _mint(to, tokenId);
        _setMetadataURI(tokenId, metadataURI);
        nextTokenId++;
    }

    function payToMint(address to, string memory metadataURI) public payable {
        require(msg.value >= 0.05 ether, "Insufficient payment");
        uint256 tokenId = nextTokenId;
        _mint(to, tokenId);
        _setMetadataURI(tokenId, metadataURI);
        nextTokenId++;
    }

    function burn(uint256 tokenId) public {
        require(_ownerOf(tokenId) == msg.sender, "Not the owner");
        _burn(tokenId);
    }

    function _setMetadataURI(
        uint256 tokenId,
        string memory metadataURI
    ) internal virtual {
        _metadataURIs[tokenId] = metadataURI;
    }

    function tokenURI(
        uint256 tokenId
    ) public view virtual override returns (string memory) {
        require(
            _ownerOf(tokenId) != address(0),
            "ERC721: URI query for nonexistent token"
        );
        return _metadataURIs[tokenId];
    }

    function getOwner() public view returns (address) {
        return owner();
    }
}
