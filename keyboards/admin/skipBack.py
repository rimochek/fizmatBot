from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

skip = ["Пропустить", "Өткізіп жіберу"]
back = ['Назад', 'Артқа']

menuRU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=skip[0]),
        ],
        [
            KeyboardButton(text=back[0]),
        ],
    ],
    resize_keyboard=True
)

menuKZ = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=skip[1]),
        ],
        [
            KeyboardButton(text=back[1]),
        ],
    ],
    resize_keyboard=True
)

backRU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=back[0])
        ]
    ]
)

backKZ = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=back[1])
        ]
    ]
)

def send_back(language):
    if language == "ru":
        return backRU
    else:
        return backKZ

def send_markup(language):
    if language == "ru":
        return menuRU
    else:
        return menuKZ