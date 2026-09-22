orders = {
    "ORDER-1": {"customer_id": "CUST-101", "amount": 49.99, "days_since_purchase": 10},
    "ORDER-2": {"customer_id": "CUST-102", "amount": 129.0, "days_since_purchase": 45},
    "ORDER-3": {"customer_id": "CUST-101", "amount": 19.99, "days_since_purchase": 5},
}

invoices = {
    "INV-1": {"customer_id": "CUST-101", "order_id": "ORDER-1", "amount": 49.99, "status": "paid", "due_date": "2026-08-15"},
    "INV-2": {"customer_id": "CUST-101", "order_id": "ORDER-3", "amount": 19.99, "status": "overdue", "due_date": "2026-09-10"},
    "INV-3": {"customer_id": "CUST-102", "order_id": "ORDER-2", "amount": 129.0, "status": "overdue", "due_date": "2026-09-01"},
}

service_status = {
    "login": "operational",
    "payments": "degraded",
    "notifications": "outage",
}

tickets = {}