import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.addUserRole_service
import project.authenticateUser_service
import project.createUser_service
import project.deleteUser_service
import project.deleteUserRole_service
import project.fetchEmojiExplanation_service
import project.fetchExplanation_service
import project.fetchRecentEmojis_service
import project.getApiHealth_service
import project.getUser_service
import project.submitEmoji_service
import project.systemHealthCheck_service
import project.updateUser_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="emoji-explainer",
    lifespan=lifespan,
    description="create a single api that takes in an emoji and explains it's meaning. Use groq and llama3 in particular",
)


@app.get(
    "/emojis/recent",
    response_model=project.fetchRecentEmojis_service.RecentEmojisResponse,
)
async def api_get_fetchRecentEmojis(
    request: project.fetchRecentEmojis_service.GetRecentEmojisRequest,
) -> project.fetchRecentEmojis_service.RecentEmojisResponse | Response:
    """
    This route provides a list of recently interpreted emojis to users. It helps in keeping track of what emojis have been popular or frequently interpreted. This endpoint utilizes a combination of querying recent data entries using GROQ and ensuring that the response is formatted appropriately for user-level consumption.
    """
    try:
        res = await project.fetchRecentEmojis_service.fetchRecentEmojis(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/emoji/explanation/{emoji_id}",
    response_model=project.fetchEmojiExplanation_service.GetEmojiExplanationResponse,
)
async def api_get_fetchEmojiExplanation(
    emoji_id: str,
) -> project.fetchEmojiExplanation_service.GetEmojiExplanationResponse | Response:
    """
    This endpoint retrieves the explanation of an emoji by its unique identifier. It’s useful for reviewing past submissions or when explanations are cached for quicker access. The endpoint responds with the emoji and its previously interpreted explanation, promoting efficient data retrieval and user interaction.
    """
    try:
        res = await project.fetchEmojiExplanation_service.fetchEmojiExplanation(
            emoji_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users/{userId}", response_model=project.getUser_service.UserDetailResponse)
async def api_get_getUser(
    userId: int,
) -> project.getUser_service.UserDetailResponse | Response:
    """
    Retrieves the details of a specific user by their unique identifier. This is protected and only accessible by administrators. It uses groq for querying the user data. The expected response includes details like username, roles, and creation date but excludes sensitive information such as the password.
    """
    try:
        res = await project.getUser_service.getUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/emoji/interpret",
    response_model=project.submitEmoji_service.EmojiInterpretResponse,
)
async def api_post_submitEmoji(
    emoji: str,
) -> project.submitEmoji_service.EmojiInterpretResponse | Response:
    """
    This route allows a user to submit an emoji, and it returns the explanation of the emoji using the Emoji Interpreter service. The request should include the emoji as payload and expect a detailed description as a response. This process involves validating the user's input, converting the emoji data using the Emoji Interpreter, and ensuring the data format adheres to what is expected by both GROQ for querying and llama3 for processing.
    """
    try:
        res = await project.submitEmoji_service.submitEmoji(emoji)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/system/status",
    response_model=project.systemHealthCheck_service.SystemStatusResponse,
)
async def api_get_systemHealthCheck(
    request: project.systemHealthCheck_service.SystemStatusRequest,
) -> project.systemHealthCheck_service.SystemStatusResponse | Response:
    """
    This endpoint is used by admins to check the operational status of the emoji-explainer application. It provides a detailed report on system health, uptime, and any issues detected in the different modules including the Response Manager and Emoji Interpreter. This aids in maintenance and quick troubleshooting.
    """
    try:
        res = await project.systemHealthCheck_service.systemHealthCheck(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/admin/user-role/{user_id}",
    response_model=project.deleteUserRole_service.RemoveUserRoleResponse,
)
async def api_delete_deleteUserRole(
    user_id: int,
) -> project.deleteUserRole_service.RemoveUserRoleResponse | Response:
    """
    Admins can utilize this endpoint to remove a user's role, effectively managing access control and system security. The endpoint requires a user's unique identifier and removes the associated role, updating the system's authorization database accordingly.
    """
    try:
        res = await project.deleteUserRole_service.deleteUserRole(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/emoji/explanation/{id}",
    response_model=project.fetchExplanation_service.EmojiExplanationResponse,
)
async def api_get_fetchExplanation(
    id: str,
) -> project.fetchExplanation_service.EmojiExplanationResponse | Response:
    """
    This endpoint allows users to retrieve a previously explained emoji using a unique identifier (id) provided at the time of the initial explanation response. This is useful for referencing past interpretations without resubmitting the same emoji. The endpoint expects an ID in the path, interacts with the data storage to fetch the corresponding explanation, and returns it formatted via the API Gateway.
    """
    try:
        res = await project.fetchExplanation_service.fetchExplanation(id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/admin/user-role",
    response_model=project.addUserRole_service.ManageUserRoleResponse,
)
async def api_post_addUserRole(
    user_id: int, new_role: project.addUserRole_service.Role
) -> project.addUserRole_service.ManageUserRoleResponse | Response:
    """
    This protected endpoint allows administrators to manage user roles within the application. It accepts a JSON body containing the user's ID and the new role to assign. This route is crucial for maintaining the integrity and order of access control in the system, ensuring that only authorized personnel can modify user roles.
    """
    try:
        res = await project.addUserRole_service.addUserRole(user_id, new_role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: int, approverId: int
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Permits administrators to remove a user from the system. It uses groq to ensure the request is valid and the specified user exists before removing their records from the database.
    """
    try:
        res = await project.deleteUser_service.deleteUser(userId, approverId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}",
    response_model=project.updateUser_service.UpdateUserDetailsResponse,
)
async def api_put_updateUser(
    userId: int, email: Optional[str], role: Optional[project.updateUser_service.Role]
) -> project.updateUser_service.UpdateUserDetailsResponse | Response:
    """
    Allows modifications to an existing user's details (excluding password). Admins can use this endpoint to update user roles or other details. It requires sending a JSON payload with the updated information, and uses groq to validate and update the record in the database.
    """
    try:
        res = await project.updateUser_service.updateUser(userId, email, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/authenticate",
    response_model=project.authenticateUser_service.UserAuthenticationResponse,
)
async def api_post_authenticateUser(
    username: str, password: str
) -> project.authenticateUser_service.UserAuthenticationResponse | Response:
    """
    This endpoint validates user login credentials against the stored records. If the credentials are correct, it issues a JWT (JSON Web Token) which should be used for subsequent requests that require authentication. This process involves using llama3 for password comparison and, if authentication is successful, groq is used to generate and return the token.
    """
    try:
        res = await project.authenticateUser_service.authenticateUser(
            username, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/health", response_model=project.getApiHealth_service.HealthCheckResponse)
async def api_get_getApiHealth(
    request: project.getApiHealth_service.HealthCheckRequest,
) -> project.getApiHealth_service.HealthCheckResponse | Response:
    """
    This route is used to monitor the health and status of the API Gateway. The response will include a status indicating whether the API is up and running correctly. This endpoint is crucial for ongoing maintenance and monitoring of the service to ensure high availability and operational performance.
    """
    try:
        res = await project.getApiHealth_service.getApiHealth(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    username: str, password: str, role: project.createUser_service.Role
) -> project.createUser_service.CreateUserResponse | Response:
    """
    This route allows an admin to create a new user. It receives a JSON payload with user information such as username and password and roles. It uses groq to handle the input validation and llama3 for secure password management. Upon successful creation, it returns the new user's details excluding the password.
    """
    try:
        res = await project.createUser_service.createUser(username, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
