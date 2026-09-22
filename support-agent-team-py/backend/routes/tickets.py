from fastapi import APIRouter, HTTPException
from data_store import tickets
from models import Ticket, TicketCreate

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("", response_model=list[Ticket])
def list_tickets():
    return [{"ticket_id": tid, **data} for tid, data in tickets.items()]

@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: str):
    ticket = tickets.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found.")
    return {"ticket_id": ticket_id, **ticket}

@router.post("", response_model=Ticket)
def create_ticket(ticket: TicketCreate):
    new_id = f"TICKET-{1000 + len(tickets)}"
    tickets[new_id] = {"issue": ticket.issue, "status": "open"}
    return {"ticket_id": new_id, **tickets[new_id]}

@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket_status(ticket_id: str, status: str):
    ticket = tickets.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found.")
    ticket["status"] = status
    return {"ticket_id": ticket_id, **ticket}

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: str):
    if ticket_id not in tickets:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found.")
    del tickets[ticket_id]
    return {"status": "success", "message": f"Ticket {ticket_id} deleted."}