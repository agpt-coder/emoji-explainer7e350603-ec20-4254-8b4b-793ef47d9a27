import prisma
import prisma.models
from pydantic import BaseModel


class HealthCheckRequest(BaseModel):
    """
    Request model for the API Gateway Health Check. This model does not require any input fields since it's a generic check.
    """

    pass


class HealthCheckResponse(BaseModel):
    """
    Provides a status update on the health of the API Gateway. Used by system administrators for maintaining and monitoring API availability.
    """

    status: str
    message: str


async def getApiHealth(request: HealthCheckRequest) -> HealthCheckResponse:
    """
    This route is used to monitor the health and status of the API Gateway. The response will include a status indicating whether the API is up and running correctly. This endpoint is crucial for ongoing maintenance and monitoring of the service to ensure high availability and operational performance.

    Args:
        request (HealthCheckRequest): Request model for the API Gateway Health Check. This model does not require any input fields since it's a generic check.

    Returns:
        HealthCheckResponse: Provides a status update on the health of the API Gateway. Used by system administrators for maintaining and monitoring API availability.

    Example:
        request = HealthCheckRequest()
        response = getApiHealth(request)
        print(response)
        > HealthCheckResponse(status="UP", message="API Gateway is running and accepting requests.")
    """
    try:
        emoji_requests = await prisma.models.EmojiRequest.prisma().count()
        if emoji_requests >= 0:
            return HealthCheckResponse(
                status="UP", message="API Gateway is running and accepting requests."
            )
        else:
            return HealthCheckResponse(
                status="UNKNOWN", message="Unable to determine the status."
            )
    except Exception as e:
        return HealthCheckResponse(status="DOWN", message=str(e))
