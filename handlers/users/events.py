from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from utils.db.eventsManager import getEvents, getEventInfo
from keyboards.user.default import menu
from keyboards.user.inline.eventsPages import getInlines, getInlinesAdmin, EventsInlinePages, AdminEventsInlinePages
from data.languagePreset import languages as lang
from loader import db, bot

router = Router()

@router.message(F.text.in_(menu.events))
async def send_events(message: Message):
    lg = db.get_user_language(message.chat.id)
    if len(getEvents(lg)) == 0:
        await message.answer(
            text=lang[lg]["noEvents"]
        )
    else:
        await message.answer(
            text=f"{lang[lg]['events']}:",
            reply_markup=getInlines(lg)[0]
        )

@router.callback_query(EventsInlinePages.filter(F.club == "nextPage"))
async def next_page(query: CallbackQuery, callback_data: EventsInlinePages):
     page = callback_data.page + 1
    
     if page > maxPages-1:
        page = 0
     elif page < 0:
        page = maxPages-1

     
     await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=getInlines(db.get_user_language(query.message.chat.id))[page]
     )

@router.callback_query(EventsInlinePages.filter(F.club == "backPage"))
async def back_page(query: CallbackQuery, callback_data: EventsInlinePages):
     page = callback_data.page - 1
     if page > maxPages-1:
        page = 0
     elif page < 0:
        page = maxPages-1
     await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=getInlines(db.get_user_language(query.message.chat.id))[page]
     )
   
@router.callback_query(AdminEventsInlinePages.filter(F.club == "nextPage"))
async def next_page(query: CallbackQuery, callback_data: AdminEventsInlinePages):
     page = callback_data.page + 1
    
     if page > maxPages-1:
        page = 0
     elif page < 0:
        page = maxPages-1

     
     await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=getInlinesAdmin(db.get_user_language(query.message.chat.id))[page]
     )

@router.callback_query(AdminEventsInlinePages.filter(F.club == "backPage"))
async def back_page(query: CallbackQuery, callback_data: AdminEventsInlinePages):
     page = callback_data.page - 1
     if page > maxPages-1:
        page = 0
     elif page < 0:
        page = maxPages-1
     await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=getInlinesAdmin(db.get_user_language(query.message.chat.id))[page]
     )

@router.callback_query(EventsInlinePages.filter())
async def club_info(query: CallbackQuery, callback_data: EventsInlinePages):
    info = getEventInfo(db.get_user_language(query.message.chat.id), callback_data.event)

    if info[1] != None or info[1] != "":
      await bot.send_photo(
         chat_id=query.message.chat.id,
         photo=info[2],
         caption=info[0],
         reply_markup=info[1],
         parse_mode="markdown"
      )
    else:
      await bot.send_photo(
         chat_id=query.message.chat.id,
         photo=info[2],
         caption=info[0],
         parse_mode="markdown"
      )


maxPages = len(getInlines("kz"))