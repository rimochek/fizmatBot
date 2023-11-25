from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.user.default import menu
from keyboards.admin import skipBack
from data.languagePreset import languages as lang
from data.languagePreset import general
from states.states import SuggestSongStates, MenuStates
from loader import db, suggestedSongEditor

router = Router()

@router.message(F.text.in_(menu.suggestSong))
async def suggestSong(message: Message, state: FSMContext):
    lg = db.get_user_language(message.chat.id)
    await message.answer(
        text=lang[lg]["suggestSong"],
        reply_markup=skipBack.send_back(lg)
    )
    await state.set_state(SuggestSongStates.writingSong)

@router.message(SuggestSongStates.writingSong)
async def getSuggestedSong(message: Message, state: FSMContext):
    lg = db.get_user_language(message.chat.id)
    if message.text in skipBack.back:
        await message.answer(
            text=general["menu"],
            reply_markup=menu.send_menu(lg)
        )
    else:
        await message.answer(
            text=lang[lg]["songAdded"],
            reply_markup=menu.send_menu(lg)
        )
        suggestedSongEditor.addSong(message.text)
    await state.set_state(MenuStates.menu)