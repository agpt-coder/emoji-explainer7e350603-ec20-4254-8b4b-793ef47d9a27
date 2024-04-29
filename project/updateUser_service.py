from enum import Enum
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enum defining user roles.
    """

    ADMIN: str
    USER: str


class User(BaseModel):
    """
    A pydantic model of User table reflecting the changes.
    """

    id: int
    email: str
    role: Role


class UpdateUserDetailsResponse(BaseModel):
    """
    This model provides a confirmation that a user's details have been updated successfully.
    """

    message: str
    updated_user: User


async def updateUser(
    userId: int, email: Optional[str], role: Optional[Role]
) -> UpdateUserDetailsResponse:
    """
    Allows modifications to an existing user's details (excluding password). Admins can use this endpoint to update user roles or other details. It requires sending a JSON payload with the updated information, and uses prisma to validate and update the record in the database.

    Args:
    userId (int): The unique identifier for the user whose details are to be updated.
    email (Optional[str]): The updated email address of the user.
    role (Optional[Role]): The new role of the user which can be adjusted by admins.

    Returns:
    UpdateUserDetailsResponse: This model provides a confirmation that a user's details have been updated successfully.
    """
    update_data = {}
    if email is not None:
        update_data["email"] = email
    if role is not None:
        update_data["role"] = role
    if update_data:
        updated_user = await prisma.models.User.prisma().update(
            where={"id": userId}, data=update_data
        )
        return UpdateUserDetailsResponse(
            message="User details updated successfully.", updated_user=updated_user
        )
    else:
        existing_user = await prisma.models.User.prisma().find_unique(
            where={"id": userId}
        )
        return UpdateUserDetailsResponse(
            message="No updates applied.", updated_user=existing_user
        )
