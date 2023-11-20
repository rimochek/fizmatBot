from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart

from states.states import StartStates
from data.languagePreset import languages as lang
from data.languagePreset import general
from loader import db
from keyboards.user.default.chooseLanguage import startLanguage, languages
from keyboards.user.default.menu import send_menu

router = Router()

@router.message(CommandStart())
async def welcome(message: types.Message, state: FSMContext):
    if db.add_user(message):
        await message.answer(
            text=general["start"],
            reply_markup=startLanguage
        )
    else:
        await message.answer(
            text=lang[db.get_user_language(message.chat.id)]["secondStart"],
            reply_markup=send_menu(db.get_user_language(message.from_user.id))
        )
    await state.set_state(StartStates.start_choosing_language)

@router.message(StartStates.start_choosing_language, F.text.in_(languages))
async def choose_language(message: types.Message, state: FSMContext):
    if message.text == languages[0]:
        db.set_user_language(message.chat.id, "ru")
        await message.reply(
            text=lang["ru"]["start"],
            reply_markup=send_menu("ru")
            )
    elif message.text == languages[1]:
        db.set_user_language(message.chat.id, "kz")
        await message.reply(
            text=lang["kz"]["start"],
            reply_markup=send_menu("kz")
            )
    await state.clear()