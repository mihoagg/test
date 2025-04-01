// SPDX-License-Identifier: MIT
pragma solidity 0.8.29;

import {ERC721URIStorage, ERC721} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NFTMarket is Ownable {
    uint256 favoriteNumber = 124121;

    struct Listing {
        address seller;
        uint256 price;
    }

    // Mapping from NFT contract address and token ID to listing details
    mapping(address => mapping(uint256 => Listing)) public listings;

    event NFTListed(
        address indexed nftContract,
        uint256 indexed tokenId,
        address seller,
        uint256 price
    );
    event NFTSold(
        address indexed nftContract,
        uint256 indexed tokenId,
        address buyer,
        uint256 price
    );

    constructor() Ownable(msg.sender) {}

    // Function to list an NFT for sale
    function listNFT(
        address nftContract,
        uint256 tokenId,
        uint256 price
    ) external {
        ERC721 nft = ERC721(nftContract);
        require(
            nft.ownerOf(tokenId) == msg.sender,
            "You are not the owner of this NFT"
        );
        listings[nftContract][tokenId] = Listing(msg.sender, price);
        emit NFTListed(nftContract, tokenId, msg.sender, price);
    }

    // Function to buy an NFT
    function buyNFT(address nftContract, uint256 tokenId) external payable {
        Listing memory listing = listings[nftContract][tokenId];
        require(listing.price > 0, "NFT not listed for sale");
        require(msg.value >= listing.price, "Insufficient payment");

        // Transfer payment to the seller
        payable(listing.seller).transfer(listing.price);

        // Transfer NFT to the buyer
        ERC721(nftContract).transferFrom(listing.seller, msg.sender, tokenId);

        // Remove the listing
        delete listings[nftContract][tokenId];

        emit NFTSold(nftContract, tokenId, msg.sender, listing.price);
    }

    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }
}
