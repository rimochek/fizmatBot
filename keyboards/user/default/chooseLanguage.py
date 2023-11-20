from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

languages = ['Русский', 'Қазақша']
back = ['🔙Назад', '🔙Артқа']

menuRU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=languages[0]),
            KeyboardButton(text=languages[1])
        ],
        [
            KeyboardButton(text=back[0]),
        ]
    ],
    resize_keyboard=True
)

menuKZ = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=languages[0]),
            KeyboardButton(text=languages[1])
        ],
        [
            KeyboardButton(text=back[1]),
        ]
    ],
    resize_keyboard=True
)

startLanguage = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=languages[0]),
            KeyboardButton(text=languages[1])
        ]
    ],
    resize_keyboard=True
)

def send_markup(language):
    if language == "ru":
        return menuRU
    else:
        return menuKZ