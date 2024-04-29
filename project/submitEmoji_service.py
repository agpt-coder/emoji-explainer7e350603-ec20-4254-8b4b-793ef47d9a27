import httpx
import prisma
import prisma.models
from pydantic import BaseModel


class EmojiInterpretResponse(BaseModel):
    """
    Detailed description or interpretation of the submitted emoji, including historical and cultural relevance where applicable.
    """

    emoji: str
    explanation: str


async def submitEmoji(emoji: str) -> EmojiInterpretResponse:
    """
    This route allows a user to submit an emoji, and it returns the explanation of the emoji using the Emoji Interpreter service. The request should include the emoji as payload and expect a detailed description as a response. This process involves validating the user's input, converting the emoji data using the Emoji Interpreter, and ensuring the data format adhered to what is expected by both GROQ for querying and llama3 for processing.

    Args:
    emoji (str): Unicode representation of the emoji to be interpreted.

    Returns:
    EmojiInterpretResponse: Detailed description or interpretation of the submitted emoji, including historical and cultural relevance where applicable.
    """
    interpretation_result = await call_emoji_interpretation_service(emoji)
    existing_explanation = await prisma.models.EmojiExplanation.prisma().find_unique(
        where={"emoji": emoji}
    )
    if existing_explanation is None:
        if interpretation_result is not None:
            await prisma.models.EmojiExplanation.prisma().create(
                data={"emoji": emoji, "explanation": interpretation_result}
            )
        else:
            raise ValueError(f"Failed to get an interpretation for emoji {emoji}.")
    return EmojiInterpretResponse(emoji=emoji, explanation=interpretation_result)


async def call_emoji_interpretation_service(emoji: str) -> str:
    """
    Simulates an asynchronous HTTP request to a real external Emoji Interpretation API.

    Args:
    emoji (str): The emoji to interpret.

    Returns:
    str: A hypothetical detailed explanation of the provided emoji.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.emojiinterpreter.example.com/interpret", json={"emoji": emoji}
        )
        response.raise_for_status()
    interpreted_data = response.json().get("explanation", None)
    if interpreted_data:
        return interpreted_data
    else:
        raise ValueError("No interpretation was returned from the service.")
