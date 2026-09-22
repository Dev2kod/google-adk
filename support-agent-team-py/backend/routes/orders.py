from fastapi import APIRouter, HTTPException
from data_store import orders
from models import Order, OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("", response_model=list[Order])
def list_orders():
    return [{"order_id": oid, **data} for oid, data in orders.items()]

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: str):
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found.")
    return {"order_id": order_id, **order}

@router.post("", response_model=Order)
def create_order(order: OrderCreate):
    new_id = f"ORDER-{len(orders) + 1}"
    orders[new_id] = order.dict()
    return {"order_id": new_id, **order.dict()}

@router.put("/{order_id}", response_model=Order)
def update_order(order_id: str, update: OrderUpdate):
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found.")
    updates = {k: v for k, v in update.dict().items() if v is not None}
    order.update(updates)
    return {"order_id": order_id, **order}

@router.delete("/{order_id}")
def delete_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found.")
    del orders[order_id]
    return {"status": "success", "message": f"Order {order_id} deleted."}