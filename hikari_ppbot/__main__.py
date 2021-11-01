import os
import hikari
import lightbulb

with open("./secrets/token") as f:
    token = f.read().strip()

bot = lightbulb.Bot(token=token, prefix="!", intents=hikari.Intents.ALL)


@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print("ready :)")

@bot.command(name="ping", help="sdfsdfzfdssdffsd")
async def pingcmd(ctx):
    await ctx.respond("Pong!")

    channel = await ctx.bot.rest.fetch_channel(882583345802907708)
    await channel.send("Pong!")

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()
    bot.run()