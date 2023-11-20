from aiogram import Router, F
from aiogram.types import Message
from loader import db

from data.languagePreset import languages as lang
from keyboards.user.default import menu

router = Router()

@router.message(F.text.in_(menu.about))
async def send_clubs(message: Message):
    lg = db.get_user_language(message.chat.id)

    await message.answer(
            text=lang[lg]['about'],
            parse_mode="HTML"
    )