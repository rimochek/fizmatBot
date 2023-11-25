from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

redactClubs = ["Редактировать клубы", "Клубтарды өңдеу"]
redactEvents = ["Редактировать ивенты", "Оқиғаларды өңдеу"]
makeAnnounce = ["Cделать обьявление", "Хабарландыру жасаңыз"]
getSuggestedSongs = ["Получить предложенные треки", "Ұсынылған тректерді алыңыз"]
back = ['В обычное меню', 'Кәдімгі мәзірге']

menuRU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=redactClubs[0]),
        ],
        [
            KeyboardButton(text=redactEvents[0]),
        ],
        [
            KeyboardButton(text=makeAnnounce[0]),
        ],
        [
            KeyboardButton(text=getSuggestedSongs[0]),
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
            KeyboardButton(text=redactClubs[1]),
        ],
        [
            KeyboardButton(text=redactEvents[1]),
        ],
        [
            KeyboardButton(text=makeAnnounce[1]),
        ],
        [
            KeyboardButton(text=getSuggestedSongs[1]),
        ],
        [
            KeyboardButton(text=back[1]),
        ],
    ],
    resize_keyboard=True
)

def send_markup(language):
    if language == "ru":
        return menuRU
    else:
        return menuKZ