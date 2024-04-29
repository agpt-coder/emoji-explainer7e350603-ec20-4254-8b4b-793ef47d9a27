import prisma
import prisma.models
from pydantic import BaseModel


class EmojiExplanationResponse(BaseModel):
    """
    Response model representing the emoji explanation retrieved from the database, formatted for the user.
    """

    emoji: str
    explanation: str


async def fetchExplanation(id: str) -> EmojiExplanationResponse:
    """
    This endpoint allows users to retrieve a previously explained emoji using a unique identifier (id) provided at the time of the initial explanation response. This is useful for referencing past interpretations without resubmitting the same emoji. The endpoint expects an ID in the path, interacts with the data storage to fetch the corresponding explanation, and returns it formatted via the API Gateway.

    Args:
    id (str): Unique identifier for the emoji explanation, used to retrieve the record from the database.

    Returns:
    EmojiExplanationResponse: Response model representing the emoji explanation retrieved from the database, formatted for the user.
    """
    emoji_explanation = await prisma.models.EmojiExplanation.prisma().find_unique(
        where={"id": int(id)}
    )
    if emoji_explanation is None:
        raise ValueError("No explanation found with the provided ID.")
    return EmojiExplanationResponse(
        emoji=emoji_explanation.emoji, explanation=emoji_explanation.explanation
    )
