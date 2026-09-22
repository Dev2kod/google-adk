from fastapi import APIRouter, HTTPException, Query
from data_store import invoices
from models import Invoice, InvoiceCreate, InvoiceUpdate

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.get("", response_model=list[Invoice])
def list_invoices(customer_id: str | None = Query(default=None)):
    results = [{"invoice_id": iid, **data} for iid, data in invoices.items()]
    if customer_id:
        results = [inv for inv in results if inv["customer_id"] == customer_id]
    return results

@router.get("/{invoice_id}", response_model=Invoice)
def get_invoice(invoice_id: str):
    invoice = invoices.get(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail=f"Invoice {invoice_id} not found.")
    return {"invoice_id": invoice_id, **invoice}

@router.post("", response_model=Invoice)
def create_invoice(invoice: InvoiceCreate):
    new_id = f"INV-{len(invoices) + 1}"
    invoices[new_id] = invoice.dict()
    return {"invoice_id": new_id, **invoice.dict()}

@router.put("/{invoice_id}", response_model=Invoice)
def update_invoice(invoice_id: str, update: InvoiceUpdate):
    invoice = invoices.get(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail=f"Invoice {invoice_id} not found.")
    updates = {k: v for k, v in update.dict().items() if v is not None}
    invoice.update(updates)
    return {"invoice_id": invoice_id, **invoice}

@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: str):
    if invoice_id not in invoices:
        raise HTTPException(status_code=404, detail=f"Invoice {invoice_id} not found.")
    del invoices[invoice_id]
    return {"status": "success", "message": f"Invoice {invoice_id} deleted."}