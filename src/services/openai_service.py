import asyncio
from openai import AsyncOpenAI
from typing import BinaryIO

from src.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def voice_to_text(voice_file: BinaryIO) -> str:
    try:
        transcription = await client.audio.transcriptions.create(
            model="whisper-1",
            file=("voice.ogg", voice_file.read())
        )
        return transcription.text
    except Exception as e:
        print(f"Ошибка при транскрибации: {e}")
        return "Произошла ошибка при обработке вашего голоса."

async def get_assistant_response(text: str) -> str:
    try:
        response = await client.responses.create(
            model="gpt-4o",
            instructions="Ты — полезный и дружелюбный ИИ-помощник.",
            input=text,
        )

        return response.output_text
    except Exception as e:
        print(f"Ошибка при работе с Chat Completions API: {e}")
        return "Извините, произошла ошибка при генерации ответа."

async def text_to_voice(text: str) -> bytes:
    try:
        response = await client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text
        )
        return response.read()
    except Exception as e:
        print(f"Ошибка при озвучивании текста: {e}")
        return b"" 