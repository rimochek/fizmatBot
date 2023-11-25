import random
import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton

from utils.db.clubsManager import addNewClub, deleteClub, getClubs, Clubs
from data.languagePreset import languages as lang
from data.languagePreset import general
from states.states import AdminMenuStates, ClubsStates
from keyboards.admin import redactClubs, menu, skipBack
from keyboards.user.inline import clubsPages
from loader import db, bot, messageLettersLimit

router = Router()

'''
    NEW POST
'''
@router.message(AdminMenuStates.clubs, F.text.in_(redactClubs.newClub))
async def add_new_club(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["writeClubName"],
        reply_markup=skipBack.send_back(lg)
    )
    await state.set_state(ClubsStates.enterClubName)

@router.message(ClubsStates.enterClubName)
async def add_club_name(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        await message.answer(
            text=lang[lg]["writeClubDescription"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.update_data(name = message.text)
        await state.set_state(ClubsStates.enterClubDescription)

@router.message(ClubsStates.enterClubDescription)
async def add_club_description(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        if len(message.text) > messageLettersLimit:
            await message.answer(
                text=lang[lg]["captionIsTooLong"]
            )
            await message.answer(
                text=lang[lg]["writeClubDescription"],
                reply_markup=skipBack.send_markup(lg)
            )
            await state.set_state(ClubsStates.enterClubDescription)
        else:
            await message.answer(
                text=lang[lg]["sendClubImage"],
                reply_markup=skipBack.send_markup(lg)
            )
            if message.text in skipBack.skip:
                await state.update_data(description = None)
            else:
                await state.update_data(description = message.text)
            await state.set_state(ClubsStates.sendClubImage)

@router.message(ClubsStates.sendClubImage, F.photo)
async def add_club_image(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["writeResidentName"],
        reply_markup=skipBack.send_back(lg)
    )
    await state.set_state(ClubsStates.enterResidentName)

    #Download file
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_name = f"{random.randint(0, 1000000)}.png"
    file_path = f"data/media/clubs/{file_name}"
    await state.update_data(img = file_name)
    await bot.download(file, file_path)

@router.message(ClubsStates.sendClubImage, F.text)
async def add_club_image(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        await message.answer(
            text=lang[lg]["writeResidentName"],
            reply_markup=skipBack.send_back(lg)
        )
        await state.update_data(img = None)
        await state.set_state(ClubsStates.enterResidentName)

@router.message(ClubsStates.enterResidentName)
async def enter_resident_name(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        await message.answer(
            text=lang[lg]["writeResidentNumber"],
            reply_markup=skipBack.send_back(lg)
        )
        await state.update_data(residentName = message.text)
        await state.set_state(ClubsStates.enterResidentNumber)

@router.message(ClubsStates.enterResidentNumber)
async def enter_resident_number(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        await message.answer(
            text=lang[lg]["sendInstagram"],
            reply_markup=skipBack.send_back(lg)
        )
        await state.update_data(residentContact = message.text)
        await state.set_state(ClubsStates.enterInstagram)

@router.message(ClubsStates.enterInstagram)
async def get_instagram(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        await message.answer(
            text=lang[lg]["clubAdded"],
            reply_markup=redactClubs.send_markup(lg),
        )
        await state.update_data(instagram = message.text)
        data = await state.get_data()
        addNewClub(data)
        await state.clear()
        await state.set_state(AdminMenuStates.clubs)



@router.message(AdminMenuStates.clubs, F.text.in_(redactClubs.deleteClub))
async def change_club(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["chooseClubToDelete"],
        reply_markup=clubsPages.getInlinesAdmin(lg)[0]
    )

@router.callback_query(clubsPages.AdminClubsInlinePages.filter())
async def choosing_to_delete(query: CallbackQuery, callback_data: clubsPages.AdminClubsInlinePages, state: FSMContext):
    lg = db.get_user_language(query.message.chat.id)
    clubToDelete = Clubs()
    imageToDelete = None
    for i in getClubs(db.get_user_language(query.message.chat.id)):
        if callback_data.club == i.callName:
            clubToDelete = i
            if i.image != "data/media/nspmLogo.png":
                imageToDelete = i.image
    deleteClub(clubToDelete.name)
    if imageToDelete != None:
        os.remove(imageToDelete)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text = "Deleted",
        reply_markup=menu.send_markup(lg)
    )
    await state.set_state(AdminMenuStates.menu)
    if len(clubsPages.getInlinesAdmin(lg)):
        await bot.edit_message_reply_markup(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=clubsPages.getInlinesAdmin(0)[0]
        )
    else:
        await bot.edit_message_reply_markup(
            chat_id=query.message.message_id,
            message_id=query.message.message_id,
            reply_markup=None
        )

@router.message(AdminMenuStates.clubs, F.text.in_(redactClubs.back))
async def back(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=general["adminMenu"],
        reply_markup=menu.send_markup(lg)
    )
    await state.set_state(AdminMenuStates.menu)


async def back(message: Message, state: FSMContext):
    lg = db.get_user_language(message.chat.id)
    state_ = await state.get_state()
    if state_ == ClubsStates.enterClubName:
        await message.answer(
            text=general["adminMenu"],
            reply_markup=menu.send_markup(lg)
        )
        await state.set_state(AdminMenuStates.menu)
    elif state_ == ClubsStates.enterClubDescription:
        await message.answer(
            text=lang[lg]["writeClubName"],
            reply_markup=skipBack.send_back(lg)
        )
        await state.set_state(ClubsStates.enterClubName)
    elif state_ == ClubsStates.sendClubImage:
        await message.answer(
            text=lang[lg]["writeClubDescription"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.set_state(ClubsStates.enterClubDescription)
    elif state_ == ClubsStates.enterResidentName:
        await message.answer(
            text=lang[lg]["sendClubImage"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.set_state(ClubsStates.sendClubImage)
    elif state_ == ClubsStates.enterResidentNumber:
        await message.answer(
            text=lang[lg]["writeResidentName"],
            reply_markup=skipBack.send_back(lg)
        )
        await state.set_state(ClubsStates.enterResidentName)
    elif state_ == ClubsStates.enterInstagram:
        await message.answer(
            text=lang[lg]["writeResidentNumber"],
            reply_markup=skipBack.send_back(lg)
        )
        await state.set_state(ClubsStates.enterResidentNumber)