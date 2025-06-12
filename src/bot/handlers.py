import io
from aiogram import Router, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import CommandStart

from src.services import openai_service

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Привет, {message.from_user.full_name}! 👋\nОтправь мне голосовое сообщение, и я отвечу.")

@router.message(F.voice)
async def voice_message_handler(message: Message) -> None:

    await message.answer("Преобразую в текст🧐")

    voice_file_id = message.voice.file_id
    file_info = await message.bot.get_file(voice_file_id)
    file_path = file_info.file_path

    voice_bytes_io = await message.bot.download_file(file_path)

    user_text = await openai_service.voice_to_text(voice_bytes_io)

    if not user_text or "ошибка" in user_text:
        await message.answer("Не удалось распознать текст. Попробуйте еще раз.")
        return

    await message.answer(f"Вы сказали: «{user_text}»\n\nГенерирую ответ...")

    ai_response_text = await openai_service.get_assistant_response(user_text)

    ai_response_voice = await openai_service.text_to_voice(ai_response_text)

    if not ai_response_voice:
        await message.answer("Не удалось сгенерировать голосовой ответ. Вот текстовая версия:\n\n" + ai_response_text)
        return

    voice_to_send = BufferedInputFile(ai_response_voice, filename="response.ogg")
    await message.answer_voice(voice_to_send)

@router.message()
async def other_messages_handler(message: Message):

    await message.answer("Я умею работать только с голосовыми сообщениями. Пожалуйста, отправь мне войс.")