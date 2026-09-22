from pydantic import BaseModel
from typing import Optional

# --- Orders ---
class OrderCreate(BaseModel):
    customer_id: str
    amount: float
    days_since_purchase: int

class OrderUpdate(BaseModel):
    customer_id: Optional[str] = None
    amount: Optional[float] = None
    days_since_purchase: Optional[int] = None

class Order(OrderCreate):
    order_id: str


# --- Invoices ---
class InvoiceCreate(BaseModel):
    customer_id: str
    order_id: str
    amount: float
    status: str
    due_date: str

class InvoiceUpdate(BaseModel):
    customer_id: Optional[str] = None
    order_id: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    due_date: Optional[str] = None

class Invoice(InvoiceCreate):
    invoice_id: str


# --- Service Status ---
class ServiceStatusUpdate(BaseModel):
    status: str

class ServiceStatus(BaseModel):
    service_name: str
    status: str

    # --- Tickets ---
class TicketCreate(BaseModel):
    issue: str

class Ticket(TicketCreate):
    ticket_id: str
    status: str = "open"