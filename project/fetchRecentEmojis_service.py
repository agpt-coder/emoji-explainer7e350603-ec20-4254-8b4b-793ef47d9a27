from typing import List, Optional

import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class GetRecentEmojisRequest(BaseModel):
    """
    No specific input fields are required for this request as it fetches recent emojis without any filters or body parameters.
    """

    pass


class EmojiInfo(BaseModel):
    """
    Details of an individual emoji request including the emoji character and its explanation.
    """

    emoji: str
    explanation: Optional[str] = None


class RecentEmojisResponse(BaseModel):
    """
    This model will return a list of recent emoji explanations, showing both the emoji and the associated explanation text.
    """

    emojis: List[EmojiInfo]


async def fetchRecentEmojis(request: GetRecentEmojisRequest) -> RecentEmojisResponse:
    """
    This route provides a list of recently interpreted emojis to users. It helps in keeping track of what emojis have been popular or frequently interpreted. This endpoint utilizes a combination of querying recent data entries using GROQ and ensuring that the response is formatted appropriately for user-level consumption.

    Args:
    request (GetRecentEmojisRequest): No specific input fields are required for this request as it fetches recent emojis without any filters or body parameters.

    Returns:
    RecentEmojisResponse: This model will return a list of recent emoji explanations, showing both the emoji and the associated explanation text.
    """
    recent_emojis = await prisma.models.EmojiRequest.prisma().find_many(
        where={"status": "EXPLAINED"}, order={"createdAt": "desc"}, take=10
    )
    if not recent_emojis:
        raise HTTPException(status_code=404, detail="No recent emojis found.")
    response = RecentEmojisResponse(
        emojis=[
            EmojiInfo(emoji=r.emoji, explanation=r.explanation) for r in recent_emojis
        ]
    )
    return response
