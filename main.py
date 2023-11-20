import asyncio
import logging

from loader import bot, dp, db, listOfCommands

from handlers.users import start, clubs, events, changeLanguage, about
from handlers.admins import adminMenu, redactClubs, redactEvents

async def main():
    logging.basicConfig(
        level=logging.INFO, filename="data/logs.log",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    await bot.set_my_commands(listOfCommands)

    dp.include_routers(
        start.router, clubs.router, events.router, changeLanguage.router, about.router,
        adminMenu.router, redactClubs.router, redactEvents.router
    )

    db.create_tables()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())