from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class UserDetailResponse(BaseModel):
    """
    Model for the response data that includes essential user details, ensuring sensitive data like passwords are excluded.
    """

    username: str
    roles: List[str]
    creationDate: datetime


async def getUser(userId: int) -> UserDetailResponse:
    """
    Retrieves the details of a specific user by their unique identifier. This is protected
    and only accessible by administrators. It uses groq for querying the user data. The
    expected response includes details like username, roles, and creation date but excludes
    sensitive information such as the password.

    Args:
        userId (int): The unique identifier of the user, utilized to retrieve specific user details.

    Returns:
        UserDetailResponse: Model for the response data that includes essential user details,
        ensuring sensitive data like passwords are excluded.

    Example:
        user_detail = await getUser(1)
        print(user_detail)
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId},
        include={"role": True, "requests": {"select": {"createdAt": True}}},
    )
    if not user:
        raise ValueError("User not found.")
    username = user.email
    roles = [user.role.name]
    creationDate = (
        min((request.createdAt for request in user.requests))
        if user.requests
        else datetime.now()
    )
    return UserDetailResponse(username=username, roles=roles, creationDate=creationDate)
