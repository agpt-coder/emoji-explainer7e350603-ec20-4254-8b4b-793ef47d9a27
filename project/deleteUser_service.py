import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Describes the outcome of the delete operation, including a success status and any relevant messages.
    """

    status: str
    message: str


async def deleteUser(userId: int, approverId: int) -> DeleteUserResponse:
    """
    Permits administrators to remove a user from the system given the appropriate permissions. The function uses
    Prisma to check the existence and role of the user, as well as the role of the approver, before proceeding
    with deletion.

    Args:
        userId (int): The unique identifier of the user to be deleted from the system.
        approverId (int): The user ID of the requester who must be an admin to authorize deletion.

    Returns:
        DeleteUserResponse: Describes the outcome of the delete operation, including a success status and
                            any relevant messages.

    Example:
        deleteUser(123, 1)
        > DeleteUserResponse(status='success', message='User successfully deleted.')
    """
    approver = await prisma.models.User.prisma().find_unique(where={"id": approverId})
    if not approver or approver.role != prisma.enums.Role.ADMIN:
        return DeleteUserResponse(
            status="error", message="Approver is not authorized or does not exist."
        )
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not user:
        return DeleteUserResponse(status="error", message="User does not exist.")
    if user.role == prisma.enums.Role.ADMIN:
        return DeleteUserResponse(
            status="error", message="Cannot delete an admin user."
        )
    await prisma.models.EmojiRequest.prisma().delete_many(where={"userId": userId})
    await prisma.models.User.prisma().delete(where={"id": userId})
    return DeleteUserResponse(status="success", message="User successfully deleted.")
