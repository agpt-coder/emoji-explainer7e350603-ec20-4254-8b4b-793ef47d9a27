from enum import Enum

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class Role(Enum):
    """
    Enum defining user roles.
    """

    ADMIN: str
    USER: str


class CreateUserResponse(BaseModel):
    """
    Outputs user details upon successful creation, excluding the password for security reasons.
    """

    id: int
    username: str
    role: Role


async def createUser(username: str, password: str, role: Role) -> CreateUserResponse:
    """
    This route allows an admin to create a new user. It receives user information such as
    username and password, and the role. Passwords will be securely hashed using bcrypt before
    storage. The user object will be created in the database and a response excluding the password
    will be returned to enhance security.

    Args:
        username (str): The desired username for the new user.
        password (str): The password for the new user. This will be securely hashed.
        role (Role): The role assigned to the new user, either ADMIN or USER.

    Returns:
        CreateUserResponse: Outputs user details upon successful creation, excluding the password for security reasons.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = await prisma.models.User.prisma().create(
        data={
            "email": username,
            "password": hashed_password.decode("utf-8"),
            "role": role.name,
        }
    )
    return CreateUserResponse(id=user.id, username=user.email, role=Role[user.role])
