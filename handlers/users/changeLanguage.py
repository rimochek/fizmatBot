from aiogram import Router, F
from aiogram.types import Message
from loader import db

from data.languagePreset import languages as lang
from data.languagePreset import general
from keyboards.user.default import menu, chooseLanguage

router = Router()

@router.message(F.text.in_(menu.changeLanguage))
async def send_clubs(message: Message):
    lg = db.get_user_language(message.chat.id)

    await message.answer(
            text=f"{lang[lg]['chooseLanguage']}:",
            reply_markup=chooseLanguage.send_markup(lg)
    )

@router.message(F.text.in_(chooseLanguage.languages))
async def change_language(message: Message):
    if message.text == chooseLanguage.languages[0]:
        db.set_user_language(message.chat.id, "ru")
        await message.reply(
            text=lang["ru"]["ruSelected"],
            reply_markup=chooseLanguage.send_markup("ru")
            )
    elif message.text == chooseLanguage.languages[1]:
        db.set_user_language(message.chat.id, "kz")
        await message.reply(
            text=lang["kz"]["kzSelected"],
            reply_markup=chooseLanguage.send_markup("kz")
            )

@router.message(F.text.in_(chooseLanguage.back))
async def back_to_menu(message: Message):
    lg = db.get_user_language(message.chat.id)

    await message.answer(
        text=general["menu"],
        reply_markup=menu.send_menu(lg)
    )