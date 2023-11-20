from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from data.languagePreset import languages as lang
from data.languagePreset import general
from states.states import AdminMenuStates
from keyboards.admin import menu, redactClubs, redactEvents
from keyboards.user.default.menu import send_menu
from loader import db, admins

router = Router()

@router.message(Command("admin"))
async def admin_menu(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if str(message.from_user.id) in admins:
        await message.answer(
            text=general["adminMenu"],
            reply_markup=menu.send_markup(lg))
        
        await state.set_state(AdminMenuStates.menu)
    else:
        await message.answer(lang[lg]["notAdmin"])

@router.message(AdminMenuStates.menu, F.text.in_(menu.redactClubs))
async def redact_clubs(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["clubs"],
        reply_markup=redactClubs.send_markup(lg)
    )
    
    await state.set_state(AdminMenuStates.clubs)

@router.message(AdminMenuStates.menu, F.text.in_(menu.redactEvents))
async def redact_events(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=general["events"],
        reply_markup=redactEvents.send_markup(lg)
    )

    await state.set_state(AdminMenuStates.event)

@router.message(AdminMenuStates.menu, F.text.in_(menu.makeAnnounce))
async def make_announce(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["makeAnnounce"],
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(AdminMenuStates.announce)

@router.message(AdminMenuStates.menu, F.text.in_(menu.back))
async def back(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=general["menu"],
        reply_markup=send_menu(lg)
    )

    await state.clear()