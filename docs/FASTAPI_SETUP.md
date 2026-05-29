# FastAPI Integration Guide

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Basic Setup](#basic-setup)
4. [Endpoints](#endpoints)
5. [Dependency Injection](#dependency-injection)
6. [Pydantic Models](#pydantic-models)
7. [Error Handling](#error-handling)

## Installation

### Step 1: Install Dependencies

```bash
pip install fastapi uvicorn steadfast-courier python-dotenv pydantic
```

### Step 2: Create FastAPI Project

```bash
mkdir courier_api
cd courier_api
touch main.py
```

## Configuration

### .env File

Create a `.env` file in your project root:

```env
STEADFAST_API_KEY=your-api-key
STEADFAST_SECRET_KEY=your-secret-key
STEADFAST_BASE_URL=https://portal.packzy.com/api/v1
STEADFAST_TIMEOUT=30
```

Or copy the provided template:

```bash
cp .env.example .env
```

### config.py (Optional)

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    steadfast_api_key: str = os.getenv('STEADFAST_API_KEY', '')
    steadfast_secret_key: str = os.getenv('STEADFAST_SECRET_KEY', '')
    steadfast_base_url: str = os.getenv('STEADFAST_BASE_URL', 'https://portal.packzy.com/api/v1')
    steadfast_timeout: int = int(os.getenv('STEADFAST_TIMEOUT', 30))

    class Config:
        env_file = ".env"

settings = Settings()
```

## Basic Setup

### main.py (Option 1: Simple - Recommended)

```python
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from steadfast_courier import SteadfastCourier, SteadfastException
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Courier Management API",
    description="SteadFast Courier API Integration",
    version="1.0.0"
)

# Initialize client from environment variables
def get_steadfast_client():
    return SteadfastCourier.from_env()
```

### main.py (Option 2: With Config)

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from steadfast_courier import SteadfastCourier, SteadfastException
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Courier Management API",
    description="SteadFast Courier API Integration",
    version="1.0.0"
)

# Initialize client globally
steadfast_client = SteadfastCourier(
    api_key=settings.steadfast_api_key,
    secret_key=settings.steadfast_secret_key,
    base_url=settings.steadfast_base_url,
    timeout=settings.steadfast_timeout,
)

# Pydantic Models
class OrderRequest(BaseModel):
    invoice: str = Field(..., example="ORD-2024-00001")
    recipient_name: str = Field(..., example="John Doe")
    recipient_phone: str = Field(..., example="01712345678")
    recipient_address: str = Field(..., example="House 44, Gulshan, Dhaka")
    cod_amount: float = Field(..., gt=0, example=1000.0)
    note: Optional[str] = Field(None, example="Handle with care")
    recipient_email: Optional[str] = Field(None, example="john@example.com")
    delivery_type: Optional[int] = Field(None, example=0)

class BulkOrderRequest(BaseModel):
    orders: list[OrderRequest]

class StatusResponse(BaseModel):
    success: bool
    data: dict = {}
    error: Optional[str] = None

# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Order Endpoints
@app.post("/orders/create", response_model=StatusResponse)
async def create_order(order: OrderRequest):
    """
    Create a new order with SteadFast Courier

    - **invoice**: Unique order identifier
    - **recipient_name**: Customer full name
    - **recipient_phone**: 11-digit phone number
    - **recipient_address**: Delivery address
    - **cod_amount**: Cash on delivery amount
    """
    try:
        response = steadfast_client.order().place_order(order.dict())
        return StatusResponse(success=True, data=response)

    except SteadfastException as e:
        logger.error(f"SteadFast Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/orders/bulk-create", response_model=StatusResponse)
async def create_bulk_orders(request: BulkOrderRequest):
    """
    Create multiple orders in a single request (max 500)
    """
    try:
        if len(request.orders) > 500:
            raise ValueError("Maximum 500 orders allowed per request")

        orders_data = [order.dict() for order in request.orders]
        response = steadfast_client.order().place_bulk_orders(orders_data)
        return StatusResponse(success=True, data=response)

    except SteadfastException as e:
        logger.error(f"SteadFast Error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Status Tracking Endpoints
@app.get("/orders/status/consignment/{consignment_id}")
async def get_status_by_consignment_id(consignment_id: int):
    """Get order status by consignment ID"""
    try:
        response = steadfast_client.status().get_status_by_consignment_id(consignment_id)
        return StatusResponse(success=True, data=response)
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders/status/invoice/{invoice}")
async def get_status_by_invoice(invoice: str):
    """Get order status by invoice number"""
    try:
        response = steadfast_client.status().get_status_by_invoice(invoice)
        return StatusResponse(success=True, data=response)
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders/status/tracking/{tracking_code}")
async def get_status_by_tracking_code(tracking_code: str):
    """Get order status by tracking code"""
    try:
        response = steadfast_client.status().get_status_by_tracking_code(tracking_code)
        return StatusResponse(success=True, data=response)
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Account Endpoints
@app.get("/account/balance")
async def get_balance():
    """Get current account balance"""
    try:
        response = steadfast_client.balance().get_current_balance()
        return StatusResponse(success=True, data=response)
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Payment Endpoints
@app.get("/payments")
async def get_payments():
    """Get all payments"""
    try:
        response = steadfast_client.payment().get_payments()
        return StatusResponse(success=True, data=response)
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/payments/{payment_id}")
async def get_payment(payment_id: int):
    """Get specific payment"""
    try:
        response = steadfast_client.payment().get_payment(payment_id)
        return StatusResponse(success=True, data=response)
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Run the API

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload

# Run on specific port
uvicorn main:app --host 0.0.0.0 --port 8000
```

Access the API:

- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Dependency Injection

### services.py

```python
from steadfast_courier import SteadfastCourier
from config import settings
import logging

logger = logging.getLogger(__name__)

class CourierService:
    """Service layer for Courier operations"""

    def __init__(self):
        self.client = SteadfastCourier(
            api_key=settings.steadfast_api_key,
            secret_key=settings.steadfast_secret_key,
            base_url=settings.steadfast_base_url,
            timeout=settings.steadfast_timeout,
        )

    def create_order(self, order_data: dict):
        """Create order"""
        try:
            logger.info(f"Creating order: {order_data['invoice']}")
            response = self.client.order().place_order(order_data)
            logger.info(f"Order created: {response['consignment']['consignment_id']}")
            return response
        except Exception as e:
            logger.error(f"Order creation failed: {str(e)}")
            raise

    def get_order_status(self, tracking_code: str):
        """Get order status"""
        try:
            return self.client.status().get_status_by_tracking_code(tracking_code)
        except Exception as e:
            logger.error(f"Status check failed: {str(e)}")
            raise

def get_courier_service() -> CourierService:
    """Dependency for FastAPI"""
    return CourierService()
```

### Using Dependency Injection

```python
from fastapi import Depends
from services import CourierService, get_courier_service

@app.post("/orders/create")
async def create_order(
    order: OrderRequest,
    service: CourierService = Depends(get_courier_service)
):
    """Create order using dependency injection"""
    try:
        response = service.create_order(order.dict())
        return StatusResponse(success=True, data=response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Pydantic Models

### models.py

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

class DeliveryType(int, Enum):
    HOME_DELIVERY = 0
    HUB_PICKUP = 1

class OrderRequest(BaseModel):
    invoice: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example="ORD-2024-00001",
        description="Unique order identifier"
    )
    recipient_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example="John Doe"
    )
    recipient_phone: str = Field(
        ...,
        min_length=11,
        max_length=11,
        example="01712345678"
    )
    recipient_address: str = Field(
        ...,
        min_length=5,
        max_length=250,
        example="House 44, Gulshan, Dhaka"
    )
    cod_amount: float = Field(
        ...,
        gt=0,
        example=1000.0
    )
    note: Optional[str] = Field(None, max_length=500)
    recipient_email: Optional[str] = Field(None, example="john@example.com")
    alternative_phone: Optional[str] = Field(None, min_length=11, max_length=11)
    delivery_type: Optional[DeliveryType] = Field(None)

    @validator('invoice')
    def validate_invoice(cls, v):
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Invoice must be alphanumeric with hyphens/underscores')
        return v

    @validator('recipient_phone')
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError('Phone must contain only digits')
        return v

    class Config:
        schema_extra = {
            "example": {
                "invoice": "ORD-2024-00001",
                "recipient_name": "John Doe",
                "recipient_phone": "01712345678",
                "recipient_address": "House 44, Gulshan, Dhaka",
                "cod_amount": 1000.0,
                "note": "Handle with care"
            }
        }

class OrderResponse(BaseModel):
    consignment_id: int
    invoice: str
    tracking_code: str
    status: str
    created_at: str

class StatusResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
```

## Error Handling

### exception_handlers.py

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from steadfast_courier import SteadfastException
import logging

logger = logging.getLogger(__name__)

def setup_exception_handlers(app: FastAPI):
    """Setup exception handlers for FastAPI"""

    @app.exception_handler(SteadfastException)
    async def steadfast_exception_handler(request: Request, exc: SteadfastException):
        logger.error(f"SteadFast API Error: {str(exc)} (Code: {exc.code})")
        return JSONResponse(
            status_code=exc.code or 400,
            content={
                "success": False,
                "error": str(exc),
                "code": exc.code,
                "details": exc.get_errors()
            }
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        logger.error(f"Validation Error: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": str(exc),
                "type": "validation_error"
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected Error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "detail": str(exc) if not isinstance(exc, Exception) else None
            }
        )
```

### Use in main.py

```python
from exception_handlers import setup_exception_handlers

app = FastAPI()
setup_exception_handlers(app)
```

## requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
steadfast-courier==1.0.0
python-dotenv==1.0.0
```

## See Also

- [Complete Usage Guide](USAGE.md)
- [Django Integration](DJANGO_SETUP.md)
- [Flask Integration](FLASK_SETUP.md)
