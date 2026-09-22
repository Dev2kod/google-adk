import requests
from google.adk.agents import Agent

BASE_URL = "http://172.16.21.186:5000"

def check_refund_eligibility(order_id: str) -> dict:
    """Checks whether an order is eligible for a refund (within 30 days of purchase).

    Args:
        order_id (str): The order ID, e.g. "ORDER-1".

    Returns:
        dict: A dictionary with 'status' ('success' or 'error') and a 'report' or 'error_message'.
    """
    try:
        response = requests.get(f"{BASE_URL}/orders/{order_id}")
    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Could not reach refunds service: {e}"}

    if response.status_code == 404:
        return {"status": "error", "error_message": f"No order found with ID {order_id}."}
    response.raise_for_status()

    order = response.json()
    eligible = order["days_since_purchase"] <= 30
    return {
        "status": "success",
        "report": (
            f"{order_id} (customer {order['customer_id']}, {order['days_since_purchase']} days old): "
            f"{'eligible' if eligible else 'not eligible'} for refund."
        ),
    }

def process_refund(order_id: str) -> dict:
    """Processes a refund for an eligible order.

    Args:
        order_id (str): The order ID to refund.

    Returns:
        dict: A dictionary with 'status' ('success' or 'error') and a 'report' or 'error_message'.
    """
    try:
        response = requests.get(f"{BASE_URL}/orders/{order_id}")
    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Could not reach refunds service: {e}"}

    if response.status_code == 404:
        return {"status": "error", "error_message": f"No order found with ID {order_id}."}
    response.raise_for_status()

    order = response.json()
    if order["days_since_purchase"] > 30:
        return {"status": "error", "error_message": f"{order_id} is past the 30-day refund window."}

    return {
        "status": "success",
        "report": f"Refund of ${order['amount']} processed for {order_id} (customer {order['customer_id']}).",
    }

root_agent = Agent(
    name="refunds_agent",
    model="gemini-3.5-flash",
    description="Handles refund requests: eligibility checks and processing refunds for orders.",
    instruction=(
        "You are the Refunds Agent. Use check_refund_eligibility before process_refund. "
        "Only handle refund-related requests."
    ),
    tools=[check_refund_eligibility, process_refund],
)