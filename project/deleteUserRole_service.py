import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class RemoveUserRoleResponse(BaseModel):
    """
    Response model indicating the result of the user role removal operation.
    """

    success: bool
    message: str


async def deleteUserRole(user_id: int) -> RemoveUserRoleResponse:
    """
    Admins can utilize this endpoint to remove a user's role, effectively managing access control and system security.
    The endpoint requires a user's unique identifier and removes the associated role, updating the system's authorization database accordingly.

    Args:
    user_id (int): The unique identifier of the user whose role is to be removed.

    Returns:
    RemoveUserRoleResponse: Response model indicating the result of the user role removal operation.
    """
    try:
        user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
        if user is None:
            return RemoveUserRoleResponse(success=False, message="User not found.")
        updated_user = await prisma.models.User.prisma().update(
            where={"id": user_id}, data={"role": prisma.enums.Role.USER}
        )
        return RemoveUserRoleResponse(
            success=True, message="User role updated successfully."
        )
    except Exception as e:
        return RemoveUserRoleResponse(
            success=False, message=f"Failed to update user role: {str(e)}"
        )
