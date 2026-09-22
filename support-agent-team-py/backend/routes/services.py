from fastapi import APIRouter, HTTPException
from data_store import service_status
from models import ServiceStatus, ServiceStatusUpdate

router = APIRouter(prefix="/services", tags=["services"])

@router.get("", response_model=list[ServiceStatus])
def list_services():
    return [{"service_name": name, "status": status} for name, status in service_status.items()]

@router.get("/{service_name}", response_model=ServiceStatus)
def get_service(service_name: str):
    status = service_status.get(service_name.lower())
    if not status:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found.")
    return {"service_name": service_name.lower(), "status": status}

@router.post("", response_model=ServiceStatus)
def create_service(service: ServiceStatus):
    name = service.service_name.lower()
    if name in service_status:
        raise HTTPException(status_code=400, detail=f"Service '{name}' already exists.")
    service_status[name] = service.status
    return {"service_name": name, "status": service.status}

@router.put("/{service_name}", response_model=ServiceStatus)
def update_service(service_name: str, update: ServiceStatusUpdate):
    name = service_name.lower()
    if name not in service_status:
        raise HTTPException(status_code=404, detail=f"Service '{name}' not found.")
    service_status[name] = update.status
    return {"service_name": name, "status": update.status}

@router.delete("/{service_name}")
def delete_service(service_name: str):
    name = service_name.lower()
    if name not in service_status:
        raise HTTPException(status_code=404, detail=f"Service '{name}' not found.")
    del service_status[name]
    return {"status": "success", "message": f"Service '{name}' deleted."}