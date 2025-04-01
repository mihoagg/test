#Importing the elements needed.
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from passlib.context import CryptContext
import mysql.connector

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "mydb",
}

# Setting the hashing configuration for the password.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setting up the models
#The NFTListing model, used for process involving NFT retrieval related information.
class NFTListing(BaseModel):
    id: int
    nft_id: str  # Type changed to string
    seller_name: str
    price: float
    status: str
    listed_at: datetime
    name: str
    description: Optional[str]
    category_name: Optional[str]
    image_url: Optional[str]

#The PurchaseRecord model, used for process involving purchase record related information.
class PurchaseRequest(BaseModel):
    nft_id: int
    buyer_id: int
    purchase_price: float

#The UserCreate model, used for process involving user account creation.
class UserCreate(BaseModel):
    name: str
    email: str
    wallet_address: str
    id_number: str
    password: str

#The UserLogin model, used for process involving user log-in action.
class UserLogin(BaseModel):
    email: str
    password: str

#The NFTCreate model, used for process involving NFT creation related information.
class NFTCreate(BaseModel):
    nft_id: Optional[str]  # Type changed to string
    seller_id: int
    price: float
    status: str = "listed"  # Default value
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None

# This function hashes the password and returns an ecrypted string from the password.
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# This function verifies the hashed password for authentication purposes.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# This endpoint is used to register a new user
@app.post("/register")
def register_user(user: UserCreate):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Perform check to see if email already exists.
    cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    # Add the new user into database.
    hashed_password = hash_password(user.password)
    cursor.execute(
        """
        INSERT INTO users (name, email, wallet_address, id_number, password)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user.name, user.email, user.wallet_address, user.id_number, hashed_password)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "User registered successfully"}

# This endpoint is used to log in a user
@app.post("/login")
def login_user(user: UserLogin):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, password FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()
    cursor.close()
    connection.close()

    if not db_user or not verify_password(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful", "user_id": db_user['id']}

# This endpoint is used to retrieve all NFT listings, with optional category and search filters
@app.get("/nft_listings", response_model=List[NFTListing])
def get_nft_listings(category: Optional[int] = None, search: Optional[str] = None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT nft_listings.*, users.name AS seller_name, categories.category_name
        FROM nft_listings
        JOIN users ON nft_listings.seller_id = users.id
        LEFT JOIN categories ON nft_listings.category_id = categories.id
        WHERE 1 = 1
    """
    params = []

    if category:
        query += " AND category_id = %s"
        params.append(category)
    if search:
        query += " AND nft_listings.name LIKE %s"
        params.append(f"%{search}%")

    cursor.execute(query, params)
    nft_listings = cursor.fetchall()
    cursor.close()
    connection.close()

    # Matching the final response with the format of NFTListing model fields
    return nft_listings

# This endpoint is used to retrieve a specific NFT listing by its `id`
@app.get("/nft_listings/{id}", response_model=NFTListing)
def get_nft_listing(id: int):  # Use `id` as an integer
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT nft_listings.*, users.name AS seller_name, categories.category_name
        FROM nft_listings
        JOIN users ON nft_listings.seller_id = users.id
        LEFT JOIN categories ON nft_listings.category_id = categories.id
        WHERE nft_listings.id = %s
    """
    cursor.execute(query, (id,))
    nft_listing = cursor.fetchone()
    cursor.close()
    connection.close()
    if nft_listing is None:
        raise HTTPException(status_code=404, detail="NFT not found")
    return nft_listing

# This endpoint is used to add a new NFT listing
@app.post("/add_nft")
def add_nft(nft: NFTCreate):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # If nft_id is provided, the system could use it; otherwise, generate a new one
    if nft.nft_id:
        nft_id = nft.nft_id
    else:
        nft_id = "NFT" + str(datetime.now().timestamp())  # Example of generating a string ID

    cursor.execute(
        """
        INSERT INTO nft_listings (nft_id, seller_id, price, status, name, description, category_id, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nft_id, nft.seller_id, nft.price, nft.status, nft.name, nft.description, nft.category_id, nft.image_url)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "NFT added successfully"}

# This endpoint is used to retrieve all categories
@app.get("/categories")
def get_categories():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM categories"
    cursor.execute(query)
    categories = cursor.fetchall()
    cursor.close()
    connection.close()
    return categories

# This endpoint is used to retrieve all users with their id and email
@app.get("/users")
def get_users():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Query to select user id and email
    query = "SELECT id, email, name FROM users"
    cursor.execute(query)
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users

# This endpoint is used to get a user's email by their ID
@app.get("/users/{user_id}/email")
def get_user_email(user_id: int):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"email": user["email"]}

# This endpoint is use to handle the back-end requests while the transaction is running
@app.post("/purchase_nft")
async def purchase_nft(request: PurchaseRequest):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    nft_id = request.nft_id
    buyer_id = request.buyer_id
    purchase_price = request.purchase_price

    # Check if the NFT exists
    cursor.execute("SELECT seller_id FROM nft_listings WHERE id = %s AND status = 'listed'", (nft_id,))
    nft_listing = cursor.fetchone()

    if nft_listing is None:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail="NFT not found or not available for sale")

    seller_id = nft_listing['seller_id']

    # Save the purchase to the database
    cursor.execute(
        """
        INSERT INTO purchases (nft_id, buyer_id, purchase_price, purchased_at)
        VALUES (%s, %s, %s, NOW())
        """,
        (nft_id, buyer_id, purchase_price)
    )

    # Update status of NFT to 'sold'
    cursor.execute(
        """
        UPDATE nft_listings
        SET status = 'sold'
        WHERE id = %s
        """,
        (nft_id,)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Purchase successful"}


# The back-end could be initiated with: uvicorn main:app --reload