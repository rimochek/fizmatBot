import asyncio
import logging

from loader import bot, dp, db, listOfCommands, suggestedSongEditor, scheduler

from handlers.users import start, clubs, events, changeLanguage, about, suggestTrack
from handlers.admins import adminMenu, redactClubs, redactEvents, makeAnnounce

async def main():
    logging.basicConfig(
        level=logging.INFO, filename="data/logs.log",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    #scheduler tasks
    scheduler.add_job(suggestedSongEditor.deleteAllData, trigger="interval", days=7, args=())
    scheduler.start()

    await bot.set_my_commands(listOfCommands)

    dp.include_routers(
        start.router, clubs.router, events.router, changeLanguage.router, about.router, suggestTrack.router,
        adminMenu.router, redactClubs.router, redactEvents.router, makeAnnounce.router
    )

    db.create_tables()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())