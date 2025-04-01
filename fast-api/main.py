from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from web3 import Web3
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/"))

# Load contract ABI and address
with open("C:/Users/Admin/Desktop/code/30049/d3app/backend/artifacts/contracts/nft.sol/MyNFT.json") as f:
    contract_json = json.load(f)
NFT_contract_abi = contract_json["abi"]

# NFT contract address
NFT_contract_address = w3.to_checksum_address("0x5FbDB2315678afecb367f032d93F642f64180aa3")

# Create contract instance
nft = w3.eth.contract(address=NFT_contract_address, abi=NFT_contract_abi)

with open("C:/Users/Admin/Desktop/code/30049/d3app/backend/artifacts/contracts/market.sol/NFTMarket.json") as f:
    contract_json = json.load(f)
Market_contract_abi = contract_json["abi"]

# Market contract address
Market_contract_address = w3.to_checksum_address("0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0")

# Create contract instance
market = w3.eth.contract(address=Market_contract_address, abi=Market_contract_abi)

# Replace 'your_account_address' and 'your_private_key' with your own address and private key
your_account_address = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
your_private_key = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"

account2_address = "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"
account2_private = "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"

db_config = {
"host": "localhost",
"user": "root",
"password": "hoang2004",
"database": "30049_database"
}

# Define allowed origins
origins = [
    "http://localhost:5173",  # React frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MintItem(BaseModel):
    metadataURI: str

class TransferItem(BaseModel):
    from_address: str
    to_address: str
    token_id: int

class ApproveItem(BaseModel):
    to_address: str
    token_id: int

class ApproveItem(BaseModel):
    to_address: str
    token_id: int
    
class nft_metadata(BaseModel):
    nft_id: int
    nft_name: str
    description: str
    image_url: str
    
class SetApprovalForAll(BaseModel):
    operator: str
    approved: bool

class ListNFTItem(BaseModel):
    nft_contract: str
    token_id: int
    price: float

def sign_and_send_transaction(transaction, private_key):
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    tx_receipt_json = {
        'transactionHash': tx_receipt.transactionHash.hex(),
        'transactionIndex': tx_receipt.transactionIndex,
        'blockHash': tx_receipt.blockHash.hex(),
        'blockNumber': tx_receipt.blockNumber,
        'from': tx_receipt['from'],
        'to': tx_receipt['to'],
        'cumulativeGasUsed': tx_receipt.cumulativeGasUsed,
        'gasUsed': tx_receipt.gasUsed,
    }
    
    return tx_receipt_json

@app.post("/mint/", tags=["NFT"])
async def mint_nft(item: MintItem):
    try:
        # Get the current token ID before minting
        current_token_id = nft.functions.nextTokenId().call()
        
        transaction = nft.functions.mint(item.to, item.metadataURI).build_transaction({
            'from': your_account_address,
            'nonce': w3.eth.get_transaction_count(your_account_address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei')
        })

        tx_receipt_json = sign_and_send_transaction(transaction, your_private_key)
        
        return {"message": "Mint success","token_id": current_token_id , "transaction_receipt": tx_receipt_json}
    except Exception as e:
        return {"error": str(e)}

@app.post("/paytomint/", tags=["NFT"])
async def pay_to_mint(item: MintItem):
    try:
        current_token_id = nft.functions.nextTokenId().call()
        transaction = nft.functions.payToMint(your_account_address, item.metadataURI).build_transaction({
            'from': your_account_address,
            'nonce': w3.eth.get_transaction_count(your_account_address),
            'value': w3.to_wei(0.05, 'ether'),
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei')
        })

        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=your_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        tx_receipt_json = {
            'transactionHash': tx_receipt.transactionHash.hex(),
            'transactionIndex': tx_receipt.transactionIndex,
            'blockHash': tx_receipt.blockHash.hex(),
            'blockNumber': tx_receipt.blockNumber,
            'from': tx_receipt['from'],
            'to': tx_receipt['to'],
            'cumulativeGasUsed': tx_receipt.cumulativeGasUsed,
            'gasUsed': tx_receipt.gasUsed,
        }
        
        return {"message": "Pay to mint success", "token_id": current_token_id, "transaction_receipt": tx_receipt_json}
    except Exception as e:
        return {"error": str(e)}

@app.post("/transfer/", tags=["NFT"])
async def transfer_nft(item: TransferItem):
    try:
        transaction = nft.functions.transferFrom(item.from_address, item.to_address, item.token_id).build_transaction({
            'from': your_account_address,
            'nonce': w3.eth.get_transaction_count(your_account_address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei')
        })

        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=your_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        tx_receipt_json = {
            'transactionHash': tx_receipt.transactionHash.hex(),
            'transactionIndex': tx_receipt.transactionIndex,
            'blockHash': tx_receipt.blockHash.hex(),
            'blockNumber': tx_receipt.blockNumber,
            'from': tx_receipt['from'],
            'to': tx_receipt['to'],
            'cumulativeGasUsed': tx_receipt.cumulativeGasUsed,
            'gasUsed': tx_receipt.gasUsed,
        }
        
        return {"message": "Transfer success", "transaction_receipt": tx_receipt_json}
    except Exception as e:
        return {"error": str(e)}

@app.post("/approve/", tags=["NFT"])
async def approve_nft(item: ApproveItem):
    try:
        transaction = nft.functions.approve(item.to_address, item.token_id).build_transaction({
            'from': your_account_address,
            'nonce': w3.eth.get_transaction_count(your_account_address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei')
        })

        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=your_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        tx_receipt_json = {
            'transactionHash': tx_receipt.transactionHash.hex(),
            'transactionIndex': tx_receipt.transactionIndex,
            'blockHash': tx_receipt.blockHash.hex(),
            'blockNumber': tx_receipt.blockNumber,
            'from': tx_receipt['from'],
            'to': tx_receipt['to'],
            'cumulativeGasUsed': tx_receipt.cumulativeGasUsed,
            'gasUsed': tx_receipt.gasUsed,
        }
        
        return {"message": "Approve success", "transaction_receipt": tx_receipt_json}
    except Exception as e:
        return {"error": str(e)}

@app.get("/get_approved/{token_id}", tags=["NFT"])
async def get_approved(token_id: int):
    try:
        approved_address = nft.functions.getApproved(token_id).call()
        return {"approved_address": approved_address}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/getOwner/", tags=["NFT"])
async def getOwner():
    try:
        # Call the getOwner function
        retrieved_value = nft.functions.getOwner().call()
        
        return {"status": "Success", "Owner": retrieved_value}
        
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/owner_of/{token_id}", tags=["NFT"])
async def owner_of(token_id: int):
    try:
        owner_address = nft.functions.ownerOf(token_id).call()
        return {"owner_address": owner_address}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/nfts/", tags=["Database"])
def get_nfts():
    try:
        # Establish a database connection
        connection = mysql.connector.connect(**db_config)

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Define the SQL query to retrieve data (e.g., all students)
        query = "SELECT * FROM nft_metadata"

        # Execute the SQL query
        cursor.execute(query)

        # Fetch all the rows
        result = cursor.fetchall()

        # Convert the result to a list of dictionaries
        nfts = [dict(zip(cursor.column_names, row)) for row in result]

        # Close the cursor and the database connection
        cursor.close()
        connection.close()
        
        return nfts

    except mysql.connector.Error as err:
        return {"error": f"Error: {err}"}
    
@app.get("/nft/{nft_id}", tags=["Database"])
async def getNftId(nft_id: int):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM nft_metadata WHERE id = %s"
    cursor.execute(query, (nft_id,))
    result = cursor.fetchone()
    nft = dict(zip(cursor.column_names, result))
    cursor.close()
    connection.close()
    return nft

@app.post("/setapprovalforall/", tags=["NFT"])
async def set_approval_for_all(item: SetApprovalForAll):
    try:
        transaction = nft.functions.setApprovalForAll(item.operator, item.approved).build_transaction({
            'from': your_account_address,
            'nonce': w3.eth.get_transaction_count(your_account_address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei')
        })

        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=your_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        tx_receipt_json = {
            'transactionHash': tx_receipt.transactionHash.hex(),
            'transactionIndex': tx_receipt.transactionIndex,
            'blockHash': tx_receipt.blockHash.hex(),
            'blockNumber': tx_receipt.blockNumber,
            'from': tx_receipt['from'],
            'to': tx_receipt['to'],
            'cumulativeGasUsed': tx_receipt.cumulativeGasUsed,
            'gasUsed': tx_receipt.gasUsed,
        }
        
        return {"message": "Set approval for all success", "transaction_receipt": tx_receipt_json}
    except Exception as e:
        return {"error": str(e)}

@app.post("/list_nft/", tags=["Market"])
async def list_nft(item: ListNFTItem):
    try:
        transaction = market.functions.listNFT(item.nft_contract, item.token_id, w3.to_wei(item.price, 'ether')).build_transaction({
            'from': your_account_address,
            'nonce': w3.eth.get_transaction_count(your_account_address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei')
        })
        tx_receipt = sign_and_send_transaction(transaction, your_private_key)

        return {"message": "NFT listed successfully", "transaction_receipt": tx_receipt}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/buy_nft/", tags=["Market"])
async def buy_nft(token_id: int):
    try:
        # Retrieve the listing price from the contract
        listing = market.functions.listings("0x5FbDB2315678afecb367f032d93F642f64180aa3", token_id).call()
        price = listing[1]  # The price is the second element in the listing tuple

        transaction = market.functions.buyNFT("0x5FbDB2315678afecb367f032d93F642f64180aa3", token_id).build_transaction({
            'from': your_account_address,
            'value': price,
            'nonce': w3.eth.get_transaction_count(your_account_address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei')
        })
        tx_receipt = sign_and_send_transaction(transaction, your_private_key)
        
        return {"message": "NFT purchased successfully", "transaction_receipt": tx_receipt}
    except Exception as e:
        return {"error": str(e)}

@app.get("/listing/{nft_contract}/{token_id}", tags=["Market"])
async def get_listing(token_id: int):
    try:
        listing = market.functions.listings("0x5FbDB2315678afecb367f032d93F642f64180aa3", token_id).call()
        return {"seller": listing[0], "price": w3.from_wei(listing[1], 'ether')}
    except Exception as e:
        return {"error": str(e)}