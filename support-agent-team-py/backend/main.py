from fastapi import FastAPI
from routes import orders, invoices, services, tickets

app = FastAPI(title="Support Agent Team Backend")

app.include_router(orders.router)
app.include_router(invoices.router)
app.include_router(services.router)
app.include_router(tickets.router)
@app.get("/")
def root():
    return {"status": "ok", "message": "Support agent team backend is running."}