"""FastAPI application for Product CRUD operations."""
from typing import List
import uvicorn

from fastapi import FastAPI, HTTPException

from models import Product, ProductCreate, ProductUpdate, User, UserCreate, UserUpdate, UserResponse
from database import db

app = FastAPI(
    title="Product & User CRUD API",
    description="A simple CRUD API for managing products and users",
    version="1.0.0"
)


def user_to_response(user: User) -> UserResponse:
    """Convert User model to UserResponse model, excluding password."""
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at
    )


@app.get("/")
def read_root():
    """Root endpoint returning welcome message."""
    return {"message": "Welcome to the Product & User CRUD API"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/products", response_model=List[Product])
def get_products():
    """Get all products"""
    return db.get_all_products()

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    """Get a specific product by ID"""
    product = db.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    """Create a new product"""
    # TODO: Add validation logic here
    return db.create_product(product)


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate):
    """Update an existing product"""
    # TODO: Add validation and error handling
    updated_product = db.update_product(product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if db.delete_product(product_id):
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    """Create a new user"""
    # TODO: Add validation logic here
    created_user = db.create_user(user)
    return user_to_response(created_user)

@app.get("/users", response_model=List[UserResponse])
def get_users():
    users = db.get_all_users()
    return [user_to_response(user) for user in users]

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_response(user)

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    updated_user = db.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_to_response(updated_user)

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    success = db.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
