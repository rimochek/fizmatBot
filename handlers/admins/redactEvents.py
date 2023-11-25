import random
import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.db.eventsManager import Events, addNewEvent, deleteEvent, getEvents
from data.languagePreset import languages as lang
from data.languagePreset import general
from states.states import AdminMenuStates, EventsStates
from keyboards.admin import menu, redactEvents, skipBack
from keyboards.user.inline import eventsPages
from loader import db, bot, messageLettersLimit, scheduler

router = Router()

@router.message(AdminMenuStates.event, F.text.in_(redactEvents.newEvent))
async def add_new_club(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["writeEventName"],
        reply_markup=skipBack.send_back(lg)
    )
    await state.set_state(EventsStates.enterEventName)

@router.message(EventsStates.enterEventName)
async def add_club_name(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        await message.answer(
            text=lang[lg]["writeEventDescription"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.update_data(name = message.text)
        await state.set_state(EventsStates.enterEventDescription)

@router.message(EventsStates.enterEventDescription)
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
                text=lang[lg]["writeEventDescription"],
                reply_markup=skipBack.send_markup(lg)
            )
            await state.set_state(EventsStates.enterEventDescription)
        else:
            await message.answer(
                text=lang[lg]["writeEventPlace"],
                reply_markup=skipBack.send_markup(lg)
            )
            await state.set_state(EventsStates.enterEventPlace)
        if message.text in skipBack.skip:
            await state.update_data(description = None)
        else:
            await state.update_data(description = message.text)

@router.message(EventsStates.enterEventPlace)
async def add_club_image(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        await message.answer(
            text=lang[lg]["writeEventDate"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.set_state(EventsStates.enterEventDate)
        if message.text in skipBack.skip:
            await state.update_data(place = None)
        else:
            await state.update_data(place = message.text)

@router.message(EventsStates.enterEventDate)
async def add_club_image(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        await message.answer(
            text=lang[lg]["sendLinkToEvent"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.set_state(EventsStates.enterEventLink)
        if message.text in skipBack.skip:
            await state.update_data(date = None)
        else:
            await state.update_data(date = message.text)

@router.message(EventsStates.enterEventLink)
async def enter_resident_name(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if message.text in skipBack.back:
        await back(message, state)
    else:
        await message.answer(
            text=lang[lg]["sendEventImage"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.set_state(EventsStates.enterEventIMG)
        if message.text in skipBack.skip:
            await state.update_data(link = None)
        else:
            await state.update_data(link = message.text)

@router.message(EventsStates.enterEventIMG, F.photo)
async def enter_resident_number(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["eventAdded"],
        reply_markup=redactEvents.send_markup(lg)
    )
    await state.set_state(AdminMenuStates.event)

    #Download file
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_name = f"{random.randint(0, 1000000)}.png"
    file_path = f"data/media/events/{file_name}"
    await state.update_data(img = file_name)
    await bot.download(file, file_path)

    addNewEvent(await state.get_data())

@router.message(EventsStates.enterEventIMG, F.text)
async def enter_resident_number(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["eventAdded"],
        reply_markup=redactEvents.send_markup(lg)
    )
    await state.set_state(AdminMenuStates.event)
    await state.update_data(img = None)

    addNewEvent(await state.get_data())



@router.message(AdminMenuStates.event, F.text.in_(redactEvents.deleteEvent))
async def change_club(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    if len(eventsPages.getInlinesAdmin(lg)):
        await message.answer(
            text=lang[lg]["chooseEventToDelete"],
            reply_markup=eventsPages.getInlinesAdmin(lg)[0]
        )
    else:
        await message.answer(
            text=lang[lg]["noEvents"]
        )

@router.callback_query(eventsPages.AdminEventsInlinePages.filter())
async def choosing_to_delete(query: CallbackQuery, callback_data: eventsPages.AdminEventsInlinePages):
    lg = db.get_user_language(query.message.chat.id)
    eventToDelete = Events()
    imageToDelete = None
    for i in getEvents(db.get_user_language(query.message.chat.id)):
        if callback_data.event == i.callName:
            eventToDelete = i
            if i.image != "data/media/nspmLogo.png":
                imageToDelete = i.image
    deleteEvent(eventToDelete.name)
    if imageToDelete != None:
        os.remove({imageToDelete})
    await bot.send_message(
        chat_id=query.message.chat.id,
        text = "Deleted"
    )
    if len(eventsPages.getInlinesAdmin(lg)):
        await bot.edit_message_reply_markup(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=eventsPages.getInlinesAdmin(lg)[0]
        )
    else:
        await bot.edit_message_reply_markup(
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=None
        )

@router.message(AdminMenuStates.event, F.text.in_(redactEvents.back))
async def backToMenu(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=general["adminMenu"],
        reply_markup=menu.send_markup(lg)
    )
    await state.set_state(AdminMenuStates.menu)



async def back(message: Message, state: FSMContext):
    lg = db.get_user_language(message.chat.id)
    state_ = await state.get_state()
    if state_ == EventsStates.enterEventName:
        await message.answer(
            text=general["adminMenu"],
            reply_markup=menu.send_markup(lg)
        )
        await state.set_state(AdminMenuStates.menu)
    elif state_ == EventsStates.enterEventDescription:
        await message.answer(
            text=lang[lg]["writeEventName"],
            reply_markup=skipBack.send_back(lg)
        )
        await state.set_state(EventsStates.enterEventName)
    elif state_ == EventsStates.enterEventPlace:
        await message.answer(
            text=lang[lg]["writeEventDescription"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.set_state(EventsStates.enterEventDescription)
    elif state_ == EventsStates.enterEventDate:
        await message.answer(
            text=lang[lg]["writeEventPlace"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.set_state(EventsStates.enterEventPlace)
    elif state_ == EventsStates.enterEventLink:
        await message.answer(
            text=lang[lg]["writeEventDate"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.set_state(EventsStates.enterEventDate)
    elif state_ == EventsStates.enterEventIMG:
        await message.answer(
            text=lang[lg]["sendLinkToEvent"],
            reply_markup=skipBack.send_markup(lg)
        )
        await state.set_state(EventsStates.enterEventLink)