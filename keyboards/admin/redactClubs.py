from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

newClub = ["Добавить новый клуб", "Жаңа клуб қосыңыз"]
changeClub = ["Изменить клуб", "Клубты өзгерту"]
deleteClub = ["Удалить существующий клуб", "Бар клубты жою"]
back = ['Назад', 'Артқа']

menuRU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=newClub[0]),
        ],
        [
            KeyboardButton(text=changeClub[0]),
        ],
        [
            KeyboardButton(text=deleteClub[0]),
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
            KeyboardButton(text=newClub[1]),
        ],
        [
            KeyboardButton(text=changeClub[1]),
        ],
        [
            KeyboardButton(text=deleteClub[1]),
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