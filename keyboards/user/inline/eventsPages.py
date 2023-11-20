from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.db.eventsManager import getEvents

class EventsInlinePages(CallbackData, prefix="pagesEvent"):
    page: int
    event: str

class AdminEventsInlinePages(CallbackData, prefix="adminEvent"):
     page: int
     event: str

def getInlines(lg):
        events = getEvents(lg)
        inlines = []
        pages = len(events)//10
        if len(events)%10 != 0:
             pages = pages+1
        for i in range(0, pages):
             buttons = [[]]
             for j in events[10*i:10*(i+1)]:
                buttons.append([InlineKeyboardButton(text=j.name, callback_data=EventsInlinePages(page=i, event=j.callName).pack())])
             buttons.append([
                InlineKeyboardButton(text="⬅️", callback_data=EventsInlinePages(page=i, event="backPage").pack()),
                InlineKeyboardButton(text=f"{i+1}/{pages}", callback_data=EventsInlinePages(page=99, event="pagesInfo").pack()),
                InlineKeyboardButton(text="➡️", callback_data=EventsInlinePages(page=i, event="nextPage").pack())
             ])
             inlines.append(InlineKeyboardMarkup(inline_keyboard=buttons))
        return inlines

def getInlinesAdmin(lg):
        events = getEvents(lg)
        inlines = []
        pages = len(events)//10
        if len(events)%10 != 0:
             pages = pages+1
        for i in range(0, pages):
             buttons = [[]]
             for j in events[10*i:10*(i+1)]:
                buttons.append([InlineKeyboardButton(text=j.name, callback_data=AdminEventsInlinePages(page=i, event=j.callName).pack())])
             buttons.append([
                InlineKeyboardButton(text="⬅️", callback_data=AdminEventsInlinePages(page=i, event="backPage").pack()),
                InlineKeyboardButton(text=f"{i+1}/{pages}", callback_data=AdminEventsInlinePages(page=99, event="pagesInfo").pack()),
                InlineKeyboardButton(text="➡️", callback_data=AdminEventsInlinePages(page=i, event="nextPage").pack())
             ])
             inlines.append(InlineKeyboardMarkup(inline_keyboard=buttons))
        return inlines