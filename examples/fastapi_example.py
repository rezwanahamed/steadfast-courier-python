# Example: FastAPI Integration

```python
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from steadfast_courier import SteadfastCourier, SteadfastException

load_dotenv()

app = FastAPI(
    title="Courier API",
    description="SteadFast Courier API Integration with FastAPI"
)

# Initialize client
client = SteadfastCourier(
    api_key=os.getenv('STEADFAST_API_KEY'),
    secret_key=os.getenv('STEADFAST_SECRET_KEY')
)

# Pydantic models
class OrderRequest(BaseModel):
    invoice: str = Field(..., example="ORD-2024-00001")
    recipient_name: str = Field(..., example="John Doe")
    recipient_phone: str = Field(..., example="01712345678")
    recipient_address: str = Field(..., example="House 44, Gulshan, Dhaka")
    cod_amount: float = Field(..., gt=0, example=1000.0)
    note: Optional[str] = None
    recipient_email: Optional[str] = None
    delivery_type: Optional[int] = None

class BulkOrderRequest(BaseModel):
    orders: list[OrderRequest]

# Routes
@app.get("/")
async def root():
    return {"message": "Courier API is running"}

@app.post("/orders/")
async def create_order(order: OrderRequest):
    """Create a new order"""
    try:
        response = client.order().place_order(order.dict())
        return {"success": True, "data": response}
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/orders/bulk/")
async def create_bulk_orders(request: BulkOrderRequest):
    """Create multiple orders"""
    try:
        if len(request.orders) > 500:
            raise ValueError("Maximum 500 orders allowed")
        
        orders_data = [order.dict() for order in request.orders]
        response = client.order().place_bulk_orders(orders_data)
        return {"success": True, "data": response}
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders/status/{tracking_code}")
async def get_order_status(tracking_code: str):
    """Get order status by tracking code"""
    try:
        response = client.status().get_status_by_tracking_code(tracking_code)
        return {"success": True, "data": response}
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/balance/")
async def get_balance():
    """Get account balance"""
    try:
        response = client.balance().get_current_balance()
        return {"success": True, "balance": response}
    except SteadfastException as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Usage

```bash
# Install dependencies
pip install fastapi uvicorn steadfast-courier python-dotenv

# Run server
python example_fastapi.py

# Test endpoints
curl -X POST http://localhost:8000/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "invoice": "ORD-2024-00001",
    "recipient_name": "John Doe",
    "recipient_phone": "01712345678",
    "recipient_address": "House 44, Gulshan, Dhaka",
    "cod_amount": 1000.0
  }'
```

## Access Swagger UI

Visit: http://localhost:8000/docs
