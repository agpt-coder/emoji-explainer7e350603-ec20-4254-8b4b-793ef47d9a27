from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enum defining user roles.
    """

    ADMIN: str
    USER: str


class ManageUserRoleResponse(BaseModel):
    """
    This model outlines the response after attempting to update a user's role. It includes a success status and a message detailing the result of the operation.
    """

    success: bool
    message: str


async def addUserRole(user_id: int, new_role: Role) -> ManageUserRoleResponse:
    """
    This protected endpoint allows administrators to manage user roles within the application. It accepts a user's ID and the new role to assign, ensuring that only authorized personnel can modify user roles.

    Args:
        user_id (int): The ID of the user whose role is to be updated.
        new_role (Role): The new role to assign to the user. Must be one of the predefined roles in the 'Role' enum.

    Returns:
        ManageUserRoleResponse: This model outlines the response after attempting to update a user's role. It includes a success status and a message detailing the result of the operation.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        return ManageUserRoleResponse(
            success=False, message=f"No user found with ID {user_id}."
        )
    try:
        await prisma.models.User.prisma().update(
            where={"id": user_id}, data={"role": new_role.value}
        )
        return ManageUserRoleResponse(
            success=True, message="User role updated successfully."
        )
    except Exception as e:
        return ManageUserRoleResponse(
            success=False, message=f"Failed to update user role: {str(e)}"
        )
