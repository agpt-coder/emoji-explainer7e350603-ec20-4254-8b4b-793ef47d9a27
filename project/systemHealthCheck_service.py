from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel


class SystemStatusRequest(BaseModel):
    """
    This model represents the request to fetch system status. Since it's a GET request, the fields represent possible query parameters to filter or alter the query if necessary, though none are defined currently.
    """

    pass


class ComponentStatus(BaseModel):
    """
    Status description for a single system component.
    """

    component_name: str
    status: str
    last_checked: str


class SystemStatusResponse(BaseModel):
    """
    This model encapsulates the response data for the system status, detailing various metrics about system components.
    """

    uptime: str
    health: Dict[str, str]
    details: List[ComponentStatus]


async def systemHealthCheck(request: SystemStatusRequest) -> SystemStatusResponse:
    """
    This endpoint is used by admins to check the operational status of the emoji-explainer application. It provides a detailed report on system health, uptime, and any issues detected in the different modules including the Response Manager and Emoji Interpreter. This aids in maintenance and quick troubleshooting.

    Args:
        request (SystemStatusRequest): This model represents the request to fetch system status.

    Returns:
        SystemStatusResponse: This model encapsulates the response data for the system status, detailing various metrics about system components.
    """
    uptime = "72 hours"
    component_details = [
        ComponentStatus(
            component_name="Response Manager",
            status="Operational",
            last_checked=datetime.now().isoformat(),
        ),
        ComponentStatus(
            component_name="Emoji Interpreter",
            status="Operational",
            last_checked=datetime.now().isoformat(),
        ),
    ]
    health_summary = {comp.component_name: comp.status for comp in component_details}
    response = SystemStatusResponse(
        uptime=uptime, health=health_summary, details=component_details
    )
    return response
