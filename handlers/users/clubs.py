from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from loader import db

from data.languagePreset import languages as lang
from utils.db.clubsManager import getClubInfo
from keyboards.user.default import menu
from keyboards.user.inline.clubsPages import getInlines, getInlinesAdmin, ClubsInlinePages, AdminClubsInlinePages
from loader import bot

router = Router()

@router.message(F.text.in_(menu.clubs))
async def send_clubs(message: Message):
    lg = db.get_user_language(message.chat.id)

    await message.answer(
            text=f"{lang[lg]['clubs']}:",
            reply_markup=getInlines(lg)[0]
    )

@router.callback_query(ClubsInlinePages.filter(F.club == "nextPage"))
async def next_page(query: CallbackQuery, callback_data: ClubsInlinePages):
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

@router.callback_query(ClubsInlinePages.filter(F.club == "backPage"))
async def back_page(query: CallbackQuery, callback_data: ClubsInlinePages):
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
   
@router.callback_query(AdminClubsInlinePages.filter(F.club == "nextPage"))
async def next_page(query: CallbackQuery, callback_data: AdminClubsInlinePages):
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

@router.callback_query(AdminClubsInlinePages.filter(F.club == "backPage"))
async def back_page(query: CallbackQuery, callback_data: AdminClubsInlinePages):
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

@router.callback_query(ClubsInlinePages.filter())
async def club_info(query: CallbackQuery, callback_data: ClubsInlinePages):
    info = getClubInfo(db.get_user_language(query.message.chat.id), callback_data.club)

    await bot.send_photo(
        chat_id=query.message.chat.id,
        photo=info[2],
        caption=info[0],
        reply_markup=info[1],
        parse_mode="markdown"
    )


maxPages = len(getInlines("kz"))