import requests
from google.adk.agents import Agent

BASE_URL = "http://172.16.21.186:5000"

def check_service_status(service: str) -> dict:
    """Checks the current operational status of a named service/feature.

    Args:
        service (str): The service name, e.g. "login", "payments", "notifications".

    Returns:
        dict: A dictionary with 'status' ('success' or 'error') and a 'report' or 'error_message'.
    """
    try:
        response = requests.get(f"{BASE_URL}/services/{service}")
    except requests.RequestException as e:
        return {"status": "error", "error_message": f"Could not reach technical service: {e}"}

    if response.status_code == 404:
        return {"status": "error", "error_message": f"Unknown service: {service}."}
    response.raise_for_status()

    data = response.json()
    return {"status": "success", "report": f"{data['service_name']} is currently: {data['status']}."}

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
    return {"status": "success", "report": f'Created {ticket["ticket_id"]} for issue: "{issue}". Our team will follow up.'}

root_agent = Agent(
    name="technical_agent",
    model="gemini-3.5-flash",
    description="Handles technical issues: service outages, bugs, and creating support tickets.",
    instruction=(
        "You are the Technical Agent. Use check_service_status to diagnose issues and create_ticket "
        "to log unresolved problems. Only handle technical requests."
    ),
    tools=[check_service_status, create_ticket],
)