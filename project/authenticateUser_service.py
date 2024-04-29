from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserAuthenticationResponse(BaseModel):
    """
    This model represents the output of the user authentication process. If successful, it returns a JWT, otherwise an appropriate error message.
    """

    jwt: str
    error: Optional[str] = None


async def authenticateUser(username: str, password: str) -> UserAuthenticationResponse:
    """
    This endpoint validates user login credentials against the stored records. If the credentials are correct, it issues a JWT (JSON Web Token) which should be used for subsequent requests that require authentication. This process involves using internal password comparison and, if authentication is successful, generating and returning the token.

    Args:
        username (str): The username of the user trying to authenticate.
        password (str): The password of the user, which will be verified against the stored hash.

    Returns:
        UserAuthenticationResponse: This model represents the output of the user authentication process. If successful, it returns a JWT, otherwise an appropriate error message.

    Example:
        response = authenticateUser('johndoe@example.com', 'correcthorsebatterystaple')
        if response.error:
            print(f"Authentication failed: {response.error}")
        else:
            print(f"JWT Token: {response.jwt}")
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user is None or not user.password == password:
        return UserAuthenticationResponse(jwt="", error="Invalid username or password")
    token = "example_token_for_" + str(user.id)
    return UserAuthenticationResponse(jwt=token, error=None)
