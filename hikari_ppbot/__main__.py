from datetime import time
import os

import aiosqlite
import hikari
import lightbulb
from lightbulb.events import CommandErrorEvent
from pytz import timezone, utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


with open("./secrets/token") as f:
    token = f.read().strip()

bot = lightbulb.Bot(token=token, prefix="!", intents=hikari.Intents.ALL)
bot.load_extensions_from("./hikari_ppbot/extentions")

bot.scheduler = AsyncIOScheduler()
bot.scheduler.configure(timezone=utc)



@bot.listen(hikari.StartingEvent)
async def on_starting(event):
    bot.db = await aiosqlite.connect("data/database.sqlite3")
    with open("data/build.sql") as f:
        await bot.db.executescript(f.read())
    bot.scheduler.add_job(bot.db.commit, CronTrigger(second=0))


@bot.listen(hikari.StoppingEvent)
async def on_stopping(event):
    await bot.db.commit()
    await bot.db.close()
    bot.scheduler.shutdown()


@bot.listen(hikari.StartedEvent)
async def on_started(event):
    bot.scheduler.start()
    print("ready :)")


@bot.listen(lightbulb.CommandErrorEvent)
async def commadn_error_failure(event):
    if isinstance(event.exception, lightbulb.errors.ConverterFailure):
        return await event.context.respond("Converter failure ERROR")
    
    raise event.exception
    
if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()
    bot.run()