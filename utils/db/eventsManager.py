import sqlite3 as sqlite
import logging

from datetime import date

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.input_file import FSInputFile
from data.languagePreset import languages as lang
from loader import scheduler

conn = sqlite.connect("data/extracurricular.sqlite")
cur = conn.cursor()

class Events:
    callName = ""
    name = "default"
    description = ""
    place = ""
    date = ""
    link = ""
    image = "root\fizmatbot\photos\events"

def getEvents(lg):
    eventslg = "eventsKZ"
    if lg == "kz":
        eventslg = "eventsKZ"
    elif lg == "ru":
        eventslg = "eventsRU"

    names = [name[0] for name in cur.execute(f"SELECT name FROM {eventslg}")]
    descriptions = [description[0] for description in cur.execute(f"SELECT description FROM {eventslg}")]
    places = [place[0] for place in cur.execute(f"SELECT place FROM {eventslg}")]
    dates = [date[0] for date in cur.execute(f"SELECT date FROM {eventslg}")]
    links = [link[0] for link in cur.execute(f"SELECT link FROM {eventslg}")]
    images = [image[0] for image in cur.execute(f"SELECT image FROM {eventslg}")]

    events = []

    for i in range(0, len(names)):
        event = Events()
        event.callName = f"event{lg}{i}"
        event.name = names[i]
        if descriptions[i] == None or descriptions[i] == "":
            event.description = None
        else:
            event.description = descriptions[i]
        event.place = places[i]
        event.date = dates[i]
        if links[i] == None or links[i] == "":
            event.link = None
        else:
            event.link = links[i]
        if images[i] == None or images[i] == "":
            event.image = "data/media/nspmLogo.png"
        else:
            event.image = "data/media/events/" + str(images[i])

        events.append(event)
    
    return events

def getEventInfo(lg, callName):
    events = getEvents(lg)
    text = ""
    markup = []
    inlineKeyboard = None

    for i in events:
        if i.callName == callName:
            text = f"<b>{i.name}</b>"
            if i.description != None:
                text = text + f"\n\n<b>{lang[lg]['description']}</b>\n{i.description}"
            if i.date != None:
                text = text + f"\n\n<b>{lang[lg]['date']}</b>\n{i.date}"
            if i.place != None:
                text = text + f"\n\n<b>{lang[lg]['place']}</b>\n{i.place}"
            if i.link != None:
                markup.append([InlineKeyboardButton(text="Instagram", url=i.link)])
                inlineKeyboard = InlineKeyboardMarkup(inline_keyboard=markup)
            return [text, inlineKeyboard, FSInputFile(i.image)]
    return None

def getEventInfoByName(lg, name):
    events = getEvents(lg)
    text = ""
    markup = []
    inlineKeyboard = None

    for i in events:
        if i.name == name:
            text = f"<b>{i.name}</b>"
            if i.description != None:
                text = text + f"\n\n<b>{lang[lg]['description']}</b>\n{i.description}"
            if i.date != None:
                text = text + f"\n\n<b>{lang[lg]['date']}</b>\n{i.date}"
            if i.place != None:
                text = text + f"\n\nb>{lang[lg]['place']}</b>\n{i.place}"
            if i.link != None:
                markup = markup.append([InlineKeyboardButton(text="Link", url=i.link)])
                inlineKeyboard = InlineKeyboardMarkup(inline_keyboard=markup)
            return [text, inlineKeyboard, FSInputFile(i.image)]
    return None

def addNewEvent(data: dict):
    values = [data.get("name"), data.get("description"), data.get("place"), data.get("date"), data.get("link"), data.get("img")]
    cur.execute("INSERT INTO eventsKZ VALUES(?, ?, ?, ?, ?, ?)", values)
    cur.execute("INSERT INTO eventsRU VALUES(?, ?, ?, ?, ?, ?)", values)
    conn.commit()
    logging.info(f"Добавил новый ивент: {values[0]}")
    if values[3]:
        date_ = values[3].split(".")
        scheduler.add_job(deleteEvent, "date", run_date=date(int(date_[2]), int(date_[1]), int(date_[0])), args=(values[0]))

def deleteEvent(name):
    cur.execute("DELETE FROM eventsKZ WHERE name = ?", (name,))
    cur.execute("DELETE FROM eventsRU WHERE name = ?", (name,))
    conn.commit()
    logging.info(f"Удалил существующий ивент: {name}")