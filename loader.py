from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config
from utils.db.storage import DatabaseManager
from utils.suggestedSongsEditor import SongEditor

scheduler = AsyncIOScheduler()
storage = MemoryStorage()
db = DatabaseManager("data/usersinfo.db")
dp = Dispatcher(storage=storage)
suggestedSongEditor = SongEditor("data/songs.txt")
bot = Bot(token=config.TOKEN)
admins = (config.ADMINS).split()
listOfCommands = [BotCommand(command="/start", description="Рестарт бота")]
messageLettersLimit = 3900