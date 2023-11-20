from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.admin.makeAnnounce import send_markup, yes, no
from states.states import AdminMenuStates, AnnounceStates
from data.languagePreset import languages as lang
from data.languagePreset import general
from keyboards.admin import menu

from loader import db, bot

router = Router()

@router.message(AdminMenuStates.announce)
async def write_message(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["yourAnnounce"],
        reply_markup=ReplyKeyboardRemove()
    )
    if message.photo == None:
        await message.answer(
            text=message.text
        )
        await state.update_data(text=message.text)
        await state.update_data(img=None)
    else:
        await message.answer_photo(
            photo=message.photo[0].file_id,
            caption=message.caption
        )
        await state.update_data(text=message.caption)
        await state.update_data(img=message.photo[0])
    await message.answer(
        text=lang[lg]["doYouWantToAnnounce"],
        reply_markup=send_markup(lg)
    )
    await state.set_state(AnnounceStates.waiting_for_confirmation)

@router.message(AnnounceStates.waiting_for_confirmation, F.text.in_(yes))
async def send_to_every(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    users = db.get_all_users()
    data = await state.get_data()

    #sending for every user
    for i in users:
        print(data.get("text"))
        if data.get("img") != None:
            await bot.send_photo(
                chat_id=i[0],
                caption=data.get("text"),
                photo=data.get("img").file_id
            )
        else:
            await bot.send_message(
                chat_id=i[0],
                text=data.get("text")
            )
    await message.answer(
        text=general["adminMenu"],
        reply_markup=menu.send_markup(lg)
    )
    await state.set_state(AdminMenuStates.menu)

@router.message(AnnounceStates.waiting_for_confirmation, F.text.in_(no))
async def send_to_every(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=general["adminMenu"],
        reply_markup=menu.send_markup(lg)
    )
    await state.set_state(AdminMenuStates.menu)