from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand

from data import config
from utils.db.storage import DatabaseManager

storage = MemoryStorage()
db = DatabaseManager("data/usersinfo.db")
dp = Dispatcher(storage=storage)
bot = Bot(token=config.TOKEN)
admins = (config.ADMINS).split()
listOfCommands = [BotCommand(command="/start", description="Рестарт бота")]