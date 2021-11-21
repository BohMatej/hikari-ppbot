import os
import hikari
import lightbulb
from lightbulb.events import CommandErrorEvent

with open("./secrets/token") as f:
    token = f.read().strip()

bot = lightbulb.Bot(token=token, prefix="!", intents=hikari.Intents.ALL)
bot.load_extensions_from("./hikari_ppbot/extentions")


@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print("ready :)")


@bot.listen(lightbulb.CommandErrorEvent)
async def commadn_error_failure(event):
    if isinstance(event.exception, lightbulb.errors.ConverterFailure):
        await event.context.respond("Converter failure ERROR")

    
if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()
    bot.run()