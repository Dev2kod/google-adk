import requests
from google.adk.agents import Agent

BASE_URL = "http://172.16.21.186:5000"

def get_invoices_for_customer(customer_id: str) -> dict:
    """Retrieves all invoices belonging to a customer, by customer ID.

    Args:
        customer_id (str): The customer ID, e.g. "CUST-101".

    Returns:
        dict: A dictionary with 'status' ('success' or 'error').
              If 'success', includes a 'report' key listing all matching invoices.
              If 'error', includes an 'error_message' key.
    """
    try:
        response = requests.get(f"{BASE_URL}/invoices", params={"customer_id": customer_id})
        response.raise_for_status()
        results = response.json()
    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Could not reach billing service: {e}"}

    if not results:
        return {"status": "error", "error_message": f"No invoices found for customer {customer_id}."}

    lines = [
        f"{inv['invoice_id']}: ${inv['amount']}, status: {inv['status']}, due {inv['due_date']}, linked to {inv['order_id']}"
        for inv in results
    ]
    return {"status": "success", "report": "; ".join(lines)}

def check_payment_status(invoice_id: str) -> dict:
    """Checks the payment status of a specific invoice by invoice ID.

    Args:
        invoice_id (str): The invoice ID, e.g. "INV-1".

    Returns:
        dict: A dictionary with 'status' ('success' or 'error') and a 'report' or 'error_message'.
    """
    try:
        response = requests.get(f"{BASE_URL}/invoices/{invoice_id}")
    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Could not reach billing service: {e}"}

    if response.status_code == 404:
        return {"status": "error", "error_message": f"No invoice found with ID {invoice_id}."}
    response.raise_for_status()

    invoice = response.json()
    return {"status": "success", "report": f"Payment status for {invoice_id}: {invoice['status']}."}

def create_ticket(issue: str) -> dict:
    """Creates a support ticket for an unresolved technical issue.

    Args:
        issue (str): A short description of the technical issue.

    Returns:
        dict: A dictionary with 'status' ('success' or 'error') and a 'report' or 'error_message'.
    """
    try:
        response = requests.post(f"{BASE_URL}/tickets", json={"issue": issue})
        response.raise_for_status()
    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Could not reach technical service: {e}"}

    ticket = response.json()
    return {"status": "success", "report": f"Created {ticket['ticket_id']} for issue: \"{issue}\". Our team will follow up."}


root_agent = Agent(
    name="billing_agent",
    model="gemini-3.5-flash",
    description="Handles billing questions: invoice lookups by customer, and payment status by invoice.",
    instruction=(
        "You are the Billing Agent. Use get_invoices_for_customer to list a customer's invoices, "
        "and check_payment_status to check a specific invoice's payment status. If the user only gives "
        "a customer ID and asks about payment status, first call get_invoices_for_customer to find their "
        "invoice IDs, then check status on the relevant one. Only handle billing-related requests."
    ),
    tools=[get_invoices_for_customer, check_payment_status],
)