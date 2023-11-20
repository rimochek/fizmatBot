from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

newEvent = ["Добавить новый ивент", "Жаңа ивент қосыңыз"]
changeEvent = ["Изменить ивент", "Ивент өзгерту"]
deleteEvent = ["Удалить существующий ивент", "Бар ивент жою"]
back = ['Назад', 'Артқа']

menuRU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=newEvent[0]),
        ],
        [
            KeyboardButton(text=changeEvent[0]),
        ],
        [
            KeyboardButton(text=deleteEvent[0]),
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
            KeyboardButton(text=newEvent[1]),
        ],
        [
            KeyboardButton(text=changeEvent[1]),
        ],
        [
            KeyboardButton(text=deleteEvent[1]),
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