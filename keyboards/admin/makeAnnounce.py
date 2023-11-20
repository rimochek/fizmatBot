from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

yes = ["Да", "Иә"]
no = ["Нет", "Жок"]

menuRU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=yes[0]),
            KeyboardButton(text=no[0]),
        ]
    ],
    resize_keyboard=True
)

menuKZ = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=yes[0]),
            KeyboardButton(text=no[0]),
        ]
    ],
    resize_keyboard=True
)

def send_markup(language):
    if language == "ru":
        return menuRU
    else:
        return menuKZ