from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

clubs = ['🍻 Клубы', '🍻 Клубтар']
events = ['🎲 Ивенты', '🎲 Ивенты']
schedule = ['📅 Расписание', '📅 Кесте']
changeLanguage = ['📜 Поменять язык', '📜 Тілді өзгерту']
about = ['О боте', 'Бот туралы']

scheduleWebApp = WebAppInfo(url="https://fizmatmpd.kz")

menuRU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=clubs[0]),
            KeyboardButton(text=events[0])
        ],
        [
            KeyboardButton(text=schedule[0], web_app=scheduleWebApp),
        ],
        [
            KeyboardButton(text=changeLanguage[0]),
            KeyboardButton(text=about[0])
        ]
    ],
    resize_keyboard=True
)

menuKZ = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=clubs[1]),
            KeyboardButton(text=events[1])
        ],
        [
            KeyboardButton(text=schedule[1], web_app=scheduleWebApp),
        ],
        [
            KeyboardButton(text=changeLanguage[1]),
            KeyboardButton(text=about[1])
        ]
    ],
    resize_keyboard=True
)

def send_menu(language):
    if language == "ru":
        return menuRU
    else:
        return menuKZ