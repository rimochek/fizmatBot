from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.db.clubsManager import getClubs

class ClubsInlinePages(CallbackData, prefix="pages"):
    page: int
    club: str

class AdminClubsInlinePages(CallbackData, prefix="admin"):
     page: int
     club: str

def getInlines(lg):
        clubs = getClubs(lg)
        inlines = []
        pages = len(clubs)//10
        if len(clubs)%10 != 0:
             pages = pages+1
        for i in range(0, pages):
             buttons = [[]]
             for j in clubs[10*i:10*(i+1)]:
                buttons.append([InlineKeyboardButton(text=j.name, callback_data=ClubsInlinePages(page=i, club=j.callName).pack())])
             buttons.append([
                InlineKeyboardButton(text="⬅️", callback_data=ClubsInlinePages(page=i, club="backPage").pack()),
                InlineKeyboardButton(text=f"{i+1}/{pages}", callback_data=ClubsInlinePages(page=99, club="pagesInfo").pack()),
                InlineKeyboardButton(text="➡️", callback_data=ClubsInlinePages(page=i, club="nextPage").pack())
             ])
             inlines.append(InlineKeyboardMarkup(inline_keyboard=buttons))
        return inlines

def getInlinesAdmin(lg):
        clubs = getClubs(lg)
        inlines = []
        pages = len(clubs)//10
        if len(clubs)%10 != 0:
             pages = pages+1
        for i in range(0, pages):
             buttons = [[]]
             for j in clubs[10*i:10*(i+1)]:
                buttons.append([InlineKeyboardButton(text=j.name, callback_data=AdminClubsInlinePages(page=i, club=j.callName).pack())])
             buttons.append([
                InlineKeyboardButton(text="⬅️", callback_data=AdminClubsInlinePages(page=i, club="backPage").pack()),
                InlineKeyboardButton(text=f"{i+1}/{pages}", callback_data=AdminClubsInlinePages(page=99, club="pagesInfo").pack()),
                InlineKeyboardButton(text="➡️", callback_data=AdminClubsInlinePages(page=i, club="nextPage").pack())
             ])
             inlines.append(InlineKeyboardMarkup(inline_keyboard=buttons))
        return inlines