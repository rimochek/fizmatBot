import sqlite3 as sqlite
import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.input_file import FSInputFile
from data.languagePreset import languages as lang

conn = sqlite.connect("data/extracurricular.sqlite")
cur = conn.cursor()

class Clubs:
    callName = ""
    name = "default"
    description = ""
    residentName = "default"
    residentContact = "8-700-888-8888"
    inst = ""
    image = "root\fizmatbot\photos\clubs"

def getClubs(lg):
    clubslg = "clubsKZ"
    if lg == "kz":
        clubslg = "clubsKZ"
    elif lg == "ru":
        clubslg = "clubsRU"

    names = [name[0] for name in cur.execute(f"SELECT name FROM {clubslg}")]
    descriptions = [description[0] for description in cur.execute(f"SELECT description FROM {clubslg}")]
    residentNames = [residentName[0] for residentName in cur.execute(f"SELECT residentName FROM {clubslg}")]
    residentContacts = [residentContact[0] for residentContact in cur.execute(f"SELECT residentContact FROM {clubslg}")]
    insts = [inst[0] for inst in cur.execute(f"SELECT inst FROM {clubslg}")]
    images = [image[0] for image in cur.execute(f"SELECT image FROM {clubslg}")]

    clubs = []

    for i in range(0, len(names)):
        club = Clubs()
        club.callName = f"club{lg}{i}"
        club.name = names[i]
        if descriptions[i] == None or descriptions[i] == "":
            club.description = None
        else:
            club.description = descriptions[i]
        club.residentName = residentNames[i]
        club.residentContact = residentContacts[i]
        if insts[i] == None or insts[i] == "":
            club.inst = None
        else:
            club.inst = insts[i]
        if images[i] == None or images[i] == "":
            club.image = "data/media/nspmLogo.png"
        else:
            club.image = "data/media/clubs/" + str(images[i])

        clubs.append(club)
    
    return clubs

def getClubInfo(lg, callName):
    clubs = getClubs(lg)
    text = ""
    markup = []

    for i in clubs:
        if i.callName == callName:
            text = f"*{i.name}*"
            markup.append([InlineKeyboardButton(text="Whatsapp", url=("https://wa.me/" + "7" + i.residentContact[1:]))])
            if i.description != None:
                text = text + f"\n\n*{lang[lg]['description']}*\n{i.description}"
            text = text + f"\n\n*{lang[lg]['contacts']}*\n{i.residentName} - {i.residentContact}"
            if i.inst != None:
                markup.append([InlineKeyboardButton(text="Instagram", url=i.inst)])
            print(i.image)
            return [text, InlineKeyboardMarkup(inline_keyboard=markup), FSInputFile(i.image)]
    return None                                                                                                                                                                       

def addNewClub(data: dict):
    values = [data.get("name"), data.get("description"), data.get("residentName"), data.get("residentContact"), data.get("instagram"), data.get("img")]
    cur.execute("INSERT INTO clubsKZ VALUES(?, ?, ?, ?, ?, ?)", values)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    cur.execute("INSERT INTO clubsRU VALUES(?, ?, ?, ?, ?, ?)", values)
    conn.commit()
    logging.info(f"Добавил новый клуб: {values[0]}")

def deleteClub(name):
    cur.execute("DELETE FROM clubsKZ WHERE name = ?", (name,))
    cur.execute("DELETE FROM clubsRU WHERE name = ?", (name,))
    conn.commit()
    logging.info(f"Удалил существующий клуб: {name}")