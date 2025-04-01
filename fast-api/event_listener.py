from web3 import Web3
import mysql.connector
import asyncio
import json

# Connect to MySQL database
db_config = {
"host": "localhost",
"user": "root",
"password": "hoang2004",
"database": "30049_database"
}

with open("C:/Users/Admin/Desktop/code/30049/d3app/backend/artifacts/contracts/market.sol/NFTMarket.json") as f:
    contract_json = json.load(f)
contract_abi = contract_json["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/"))
market_contract_address = w3.to_checksum_address("0x5FbDB2315678afecb367f032d93F642f64180aa3")
contract = w3.eth.contract(address=market_contract_address, abi=contract_abi)
your_account_address = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
your_private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"


# Event listener function
def handle_event(event):
    event_name = event.event
    event_args = event.args

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    if event_name == "NFTListed":
            query = "INSERT INTO listings (nft_contract, token_id, seller, price) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (event_args.nftContract, event_args.tokenId, event_args.seller, event_args.price))
            
            
    elif event_name == "NFTSold":
            query = "DELETE FROM listings WHERE nft_contract = %s AND token_id = %s"
            cursor.execute(query, (event_args.nftContract, event_args.tokenId))
            queyr = "INSERT INTO sales (nft_contract, token_id, buyer, price) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (event_args.nftContract, event_args.tokenId, event_args.buyer, event_args.price))
    
    connection.commit()
    cursor.close()
    connection.close()       

# Asynchronous loop to listen for events
async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)

# Main function to set up event listeners
def start_event_listener():
    nft_listed_filter = contract.events.NFTListed.create_filter(from_block='latest')
    nft_sold_filter = contract.events.NFTSold.create_filter(from_block='latest')

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(asyncio.gather(
            log_loop(nft_listed_filter, 2),
            log_loop(nft_sold_filter, 2)
        ))
    finally:
        loop.close()