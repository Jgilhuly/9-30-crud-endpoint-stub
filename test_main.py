"""Unit tests for FastAPI application endpoints."""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import Mock

from main import app
from models import ProductCreate, ProductUpdate, UserCreate, UserUpdate
from database import InMemoryDatabase, db


class TestFixtures:
    """Test data fixtures."""

    @staticmethod
    def product_create_data():
        return {
            "name": "Test Product",
            "description": "A test product description",
            "price": 29.99,
            "category": "Test Category",
            "tags": ["test", "product"],
            "in_stock": True
        }

    @staticmethod
    def product_update_data():
        return {
            "name": "Updated Product",
            "price": 39.99,
            "in_stock": False
        }

    @staticmethod
    def user_create_data():
        return {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }

    @staticmethod
    def user_update_data():
        return {
            "name": "Updated User",
            "email": "updated@example.com"
        }


@pytest.fixture
def client():
    """Create a test client with fresh database for each test."""
    # Create a fresh database instance for each test
    fresh_db = InMemoryDatabase()
    
    # Replace the global db instance with our test instance
    import main
    original_db = main.db
    main.db = fresh_db
    
    # Create test client
    test_client = TestClient(app)
    
    yield test_client
    
    # Restore original db instance
    main.db = original_db


class TestRootEndpoints:
    """Tests for basic application endpoints."""

    def test_read_root(self, client):
        """Test root endpoint returns welcome message."""
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Product & User CRUD API"}

    def test_health_check(self, client):
        """Test health check endpoint."""
        # Act
        response = client.get("/health")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestProductEndpoints:
    """Tests for product CRUD endpoints."""

    def test_get_all_products_empty(self, client):
        """Test getting all products when database is initially empty (no sample data)."""
        # Arrange - client fixture provides fresh db with sample data
        
        # Act
        response = client.get("/products")
        
        # Assert
        assert response.status_code == 200
        products = response.json()
        assert isinstance(products, list)
        assert len(products) == 3  # Sample data count

    def test_create_product(self, client):
        """Test creating a new product."""
        # Arrange
        product_data = TestFixtures.product_create_data()
        
        # Act
        response = client.post("/products", json=product_data)
        
        # Assert
        assert response.status_code == 200
        created_product = response.json()
        assert created_product["name"] == product_data["name"]
        assert created_product["description"] == product_data["description"]
        assert created_product["price"] == product_data["price"]
        assert created_product["category"] == product_data["category"]
        assert created_product["tags"] == product_data["tags"]
        assert created_product["in_stock"] == product_data["in_stock"]
        assert "id" in created_product
        assert "created_at" in created_product

    def test_get_product_by_id(self, client):
        """Test getting a specific product by ID."""
        # Arrange - create a product first
        product_data = TestFixtures.product_create_data()
        create_response = client.post("/products", json=product_data)
        created_product = create_response.json()
        product_id = created_product["id"]
        
        # Act
        response = client.get(f"/products/{product_id}")
        
        # Assert
        assert response.status_code == 200
        retrieved_product = response.json()
        assert retrieved_product["id"] == product_id
        assert retrieved_product["name"] == product_data["name"]

    def test_get_product_not_found(self, client):
        """Test getting a non-existent product returns 404."""
        # Arrange - use non-existent product ID
        non_existent_id = 99999
        
        # Act
        response = client.get(f"/products/{non_existent_id}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_update_product(self, client):
        """Test updating an existing product."""
        # Arrange - create a product first
        product_data = TestFixtures.product_create_data()
        create_response = client.post("/products", json=product_data)
        created_product = create_response.json()
        product_id = created_product["id"]
        
        update_data = TestFixtures.product_update_data()
        
        # Act
        response = client.put(f"/products/{product_id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        updated_product = response.json()
        assert updated_product["id"] == product_id
        assert updated_product["name"] == update_data["name"]
        assert updated_product["price"] == update_data["price"]
        assert updated_product["in_stock"] == update_data["in_stock"]
        # Fields not in update should remain unchanged
        assert updated_product["description"] == product_data["description"]
        assert updated_product["category"] == product_data["category"]

    def test_update_product_not_found(self, client):
        """Test updating a non-existent product returns 404."""
        # Arrange
        non_existent_id = 99999
        update_data = TestFixtures.product_update_data()
        
        # Act
        response = client.put(f"/products/{non_existent_id}", json=update_data)
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_delete_product(self, client):
        """Test deleting an existing product."""
        # Arrange - create a product first
        product_data = TestFixtures.product_create_data()
        create_response = client.post("/products", json=product_data)
        created_product = create_response.json()
        product_id = created_product["id"]
        
        # Act
        response = client.delete(f"/products/{product_id}")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "Product deleted successfully"
        
        # Verify product is actually deleted
        get_response = client.get(f"/products/{product_id}")
        assert get_response.status_code == 404

    def test_delete_product_not_found(self, client):
        """Test deleting a non-existent product returns 404."""
        # Arrange
        non_existent_id = 99999
        
        # Act
        response = client.delete(f"/products/{non_existent_id}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"


class TestUserEndpoints:
    """Tests for user CRUD endpoints."""

    def test_get_all_users(self, client):
        """Test getting all users."""
        # Act
        response = client.get("/users")
        
        # Assert
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) == 3  # Sample data count

    def test_create_user(self, client):
        """Test creating a new user."""
        # Arrange
        user_data = TestFixtures.user_create_data()
        
        # Act
        response = client.post("/users", json=user_data)
        
        # Assert
        assert response.status_code == 200
        created_user = response.json()
        assert created_user["name"] == user_data["name"]
        assert created_user["email"] == user_data["email"]
        assert created_user["password"] == user_data["password"]
        assert "id" in created_user
        assert "created_at" in created_user

    def test_get_user_by_id(self, client):
        """Test getting a specific user by ID."""
        # Arrange - create a user first
        user_data = TestFixtures.user_create_data()
        create_response = client.post("/users", json=user_data)
        created_user = create_response.json()
        user_id = created_user["id"]
        
        # Act
        response = client.get(f"/users/{user_id}")
        
        # Assert
        assert response.status_code == 200
        retrieved_user = response.json()
        assert retrieved_user["id"] == user_id
        assert retrieved_user["name"] == user_data["name"]
        assert retrieved_user["email"] == user_data["email"]

    def test_get_user_not_found(self, client):
        """Test getting a non-existent user returns 404."""
        # Arrange
        non_existent_id = 99999
        
        # Act
        response = client.get(f"/users/{non_existent_id}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_update_user(self, client):
        """Test updating an existing user."""
        # Arrange - create a user first
        user_data = TestFixtures.user_create_data()
        create_response = client.post("/users", json=user_data)
        created_user = create_response.json()
        user_id = created_user["id"]
        
        update_data = TestFixtures.user_update_data()
        
        # Act
        response = client.put(f"/users/{user_id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["id"] == user_id
        assert updated_user["name"] == update_data["name"]
        assert updated_user["email"] == update_data["email"]
        # Fields not in update should remain unchanged
        assert updated_user["password"] == user_data["password"]

    def test_update_user_not_found(self, client):
        """Test updating a non-existent user returns 404."""
        # Arrange
        non_existent_id = 99999
        update_data = TestFixtures.user_update_data()
        
        # Act
        response = client.put(f"/users/{non_existent_id}", json=update_data)
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_user(self, client):
        """Test deleting an existing user."""
        # Arrange - create a user first
        user_data = TestFixtures.user_create_data()
        create_response = client.post("/users", json=user_data)
        created_user = create_response.json()
        user_id = created_user["id"]
        
        # Act
        response = client.delete(f"/users/{user_id}")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"
        
        # Verify user is actually deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, client):
        """Test deleting a non-existent user returns 404."""
        # Arrange
        non_existent_id = 99999
        
        # Act
        response = client.delete(f"/users/{non_existent_id}")
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


class TestDataValidation:
    """Tests for input validation and edge cases."""

    def test_create_product_missing_required_fields(self, client):
        """Test creating product with missing required fields."""
        # Arrange - incomplete product data
        incomplete_data = {
            "name": "Test Product"
            # Missing description, price, category
        }
        
        # Act
        response = client.post("/products", json=incomplete_data)
        
        # Assert
        assert response.status_code == 422  # Validation error

    def test_create_product_invalid_price(self, client):
        """Test creating product with invalid price type."""
        # Arrange
        invalid_data = TestFixtures.product_create_data()
        invalid_data["price"] = "invalid_price"  # Should be float
        
        # Act
        response = client.post("/products", json=invalid_data)
        
        # Assert
        assert response.status_code == 422

    def test_create_user_invalid_email_format(self, client):
        """Test creating user with invalid email format."""
        # Arrange - Note: Pydantic's BaseModel doesn't validate email format by default
        # This test documents the current behavior - email validation would need EmailStr type
        invalid_data = TestFixtures.user_create_data()
        invalid_data["email"] = "not-an-email"
        
        # Act
        response = client.post("/users", json=invalid_data)
        
        # Assert - Currently this passes because we don't have email validation
        # If email validation is added later, this should return 422
        assert response.status_code == 200

    def test_partial_update_product(self, client):
        """Test updating only some fields of a product."""
        # Arrange - create a product first
        product_data = TestFixtures.product_create_data()
        create_response = client.post("/products", json=product_data)
        created_product = create_response.json()
        product_id = created_product["id"]
        
        # Only update name
        partial_update = {"name": "Partially Updated Name"}
        
        # Act
        response = client.put(f"/products/{product_id}", json=partial_update)
        
        # Assert
        assert response.status_code == 200
        updated_product = response.json()
        assert updated_product["name"] == "Partially Updated Name"
        # Other fields should remain unchanged
        assert updated_product["description"] == product_data["description"]
        assert updated_product["price"] == product_data["price"]
        assert updated_product["category"] == product_data["category"]


class TestDatabaseIsolation:
    """Tests to ensure database isolation between tests."""

    def test_database_isolation_products(self, client):
        """Test that each test gets a fresh database instance."""
        # Arrange & Act - create a product
        product_data = TestFixtures.product_create_data()
        response = client.post("/products", json=product_data)
        created_product = response.json()
        
        # Assert - this product should be in addition to sample data
        all_products_response = client.get("/products")
        all_products = all_products_response.json()
        
        # Should have 3 sample products + 1 created = 4 total
        assert len(all_products) == 4
        assert any(p["name"] == product_data["name"] for p in all_products)

    def test_database_isolation_users(self, client):
        """Test that user operations work with fresh database."""
        # Arrange & Act - create a user
        user_data = TestFixtures.user_create_data()
        response = client.post("/users", json=user_data)
        created_user = response.json()
        
        # Assert - this user should be in addition to sample data
        all_users_response = client.get("/users")
        all_users = all_users_response.json()
        
        # Should have 3 sample users + 1 created = 4 total
        assert len(all_users) == 4
        assert any(u["name"] == user_data["name"] for u in all_users)