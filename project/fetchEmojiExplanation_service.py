from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class GetEmojiExplanationResponse(BaseModel):
    """
    This response model provides the emoji along with its explanation as stored in the system, serving the purpose of quick access for users.
    """

    emoji: str
    explanation: Optional[str] = None


async def fetchEmojiExplanation(emoji_id: str) -> GetEmojiExplanationResponse:
    """
    Retrieves the explanation of an emoji by its unique identifier from the prisma.models.EmojiExplanation table.
    If the emoji is found, it returns the emoji and its explanation; if not found, it returns the emoji with a None explanation.

    Args:
        emoji_id (str): The unique identifier of the emoji for which the explanation is requested. This should match the ID used in the prisma.models.EmojiExplanation model.

    Returns:
        GetEmojiExplanationResponse: This response model provides the emoji along with its explanation as stored in the system, serving the purpose of quick access for users.

    Example:
        fetchEmojiExplanation("1")
        > GetEmojiExplanationResponse(emoji='😀', explanation='A smiley face, often used to express happiness')

    Raises:
        ValueError: If the emoji_id is not found.
    """
    emoji_record = await prisma.models.EmojiExplanation.prisma().find_unique(
        where={"id": int(emoji_id)}
    )
    if not emoji_record:
        raise ValueError(f"No explanation found for emoji with id {emoji_id}")
    return GetEmojiExplanationResponse(
        emoji=emoji_record.emoji, explanation=emoji_record.explanation
    )
