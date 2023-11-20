import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from utils.db.eventsManager import Events, addNewEvent, deleteEvent, getEvents
from data.languagePreset import languages as lang
from data.languagePreset import general
from states.states import AdminMenuStates, EventsStates
from keyboards.admin import menu, redactEvents
from keyboards.user.inline import eventsPages
from loader import db, bot

router = Router()

@router.message(AdminMenuStates.event, F.text.in_(redactEvents.newEvent))
async def add_new_club(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["writeEventName"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(EventsStates.enterEventName)

@router.message(EventsStates.enterEventName)
async def add_club_name(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["writeEventDescription"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(name = message.text)
    await state.set_state(EventsStates.enterEventDescription)

@router.message(EventsStates.enterEventDescription)
async def add_club_description(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["writeEventPlace"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(description = message.text)
    await state.set_state(EventsStates.enterEventPlace)

@router.message(EventsStates.enterEventPlace)
async def add_club_image(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["writeEventDate"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(place = message.text)
    await state.set_state(EventsStates.enterEventDate)

@router.message(EventsStates.enterEventDate)
async def add_club_image(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["sendLinkToEvent"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(date = message.text)
    await state.set_state(EventsStates.enterEventLink)

@router.message(EventsStates.enterEventLink)
async def enter_resident_name(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["sendEventImage"],
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(link = message.text)
    await state.set_state(EventsStates.enterEventIMG)

@router.message(EventsStates.enterEventIMG, F.photo)
async def enter_resident_number(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["eventAdded"],
        reply_markup=ReplyKeyboardRemove()
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
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AdminMenuStates.event)

    #Download file
    await state.update_data(img = None)

    addNewEvent(await state.get_data())



@router.message(AdminMenuStates.event, F.text.in_(redactEvents.deleteEvent))
async def change_club(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=lang[lg]["chooseEventToDelete"],
        reply_markup=eventsPages.getInlinesAdmin(lg)[0]
    )

@router.callback_query(eventsPages.AdminEventsInlinePages.filter())
async def choosing_to_delete(query: CallbackQuery, callback_data: eventsPages.AdminEventsInlinePages):
    eventToDelete = Events()
    for i in getEvents(db.get_user_language(query.message.chat.id)):
        print(i)
        if callback_data.event == i.callName:
            print("got you")
            eventToDelete = i
    deleteEvent(eventToDelete.name)
    await bot.send_message(
        chat_id=query.message.chat.id,
        text = "Deleted"
    )

@router.message(AdminMenuStates.event, F.text.in_(redactEvents.back))
async def back(message: Message, state: FSMContext):
    lg = db.get_user_language(message.from_user.id)
    await message.answer(
        text=general["adminMenu"],
        reply_markup=menu.send_markup(lg)
    )
    await state.set_state(AdminMenuStates.menu)