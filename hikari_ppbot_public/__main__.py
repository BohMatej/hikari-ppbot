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
bot.remove_command("help")
@bot.command()
async def help(ctx: lightbulb.Context):
    embed1 = (
        hikari.Embed(
            title = "Maculamatej's hwbot - Help and information",
            description = "A lightweight bot for organizing assignments for Discord servers. Created by Matej Macula.",
        )
    ) 
    embed2 = (
        hikari.Embed(
            title = "Setting server channels - `!setchannel`",
            description = "**`!setchannel [weekday], [channelID]`**",
        )
        .add_field("`[weekday]`", "A weeekday - meaning `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, or `sunday`.")
        .add_field("`[ChannelID]`", "The ID of the text channel, or `default`.")
        .add_field("-", "**-**")
        .add_field("Getting the text channel ID", "Right click a text channel and select Copy ID. Make sure that Developer Mode is turned on under User Settings - Advanced.")
        .add_field("The `default` keyword", "Setting a weekday to `default` resets the text channel, and new assignments for that weekday will appear where the `assign` command was called.")
    ) 
    embed3 = (
        hikari.Embed(
            title = "Setting reaction emojis - `!setemoji`",
            description = "**`!setemoji [purpose], [EmojiID], [EmojiName]`**",
        )
        .add_field("`[purpose]`", "What purpose the emoji has: `complete` or `incomplete`.")
        .add_field("`[EmojiID]`", "The ID of the emoji, or `default`.")
        .add_field("`[EmojiName]` (optional)", "The name of the emoji - the string of letters between the ':' symbols when typing out an emoji. Leave out if `EmojiID` is `default`")
        .add_field("-", "**-**")
        .add_field("Getting the emoji ID", "Right click the emoji and select Copy Link. Paste the link anywhere "
        "- the ID will appear in the URL as a string of digits: 'https://cdn.discordapp.com/emojis/**[EmojiID]**.webp'.")
        .add_field("The `default` keyword", "Setting an emoji to `default` reverts the emoji to ✅ for complete and ❌ for incomplete.")
        .add_field("Note:", "At the moment, the bot **only supports custom emoji** to replace the defaults.")
    ) 
    embed4 = (
        hikari.Embed(
            title = "Creating assignments - `!assign`",
            description = "`!assign [date], time=[time], assignment type=[assignment_type], head=[heading], [description]`",
        )
        .add_field("`[date]`", "The deadline date in DD.MM.YYYY format. Also accepts `today`, `tomorrow`, or any of the weekdays (such as `monday`) "
        "optionally accompanied by the keyword 'next' (such as `next wednesday`); in these cases the upcoming weekday is selected as the deadline. If 'next' is included, "
        "the second upcoming weekday (skipping a week) is selected.")
        .add_field("`[time]` (optional)", "The time of day in HH:MM format. If skipped, **defaults to 23:59.** The parameter prefix 'time=' can also be replaced by 't=' and "
        "is case sensitive with the exception of the first letter.")
        .add_field("`[atype]` (optional)", "The type of the assignment - `homework`, `h`, `reminder`, `r`, `project`, `p`, `test`, or `t`. Affects the thumbnail and color of the "
        "assignment message. The parameter prefix 'assignment type=' can also be replaced by 'atype=', 'at', or 't', and "
        "is case sensitive with the exception of the first letter.")
        .add_field("`[heading]` (optional)", "Sets the heading of the assignment message. If skipped, **defaults to 'Assignment'.** The parameter prefix 'head=' can also "
        "be replaced by 'h=' and is case sensitive with the exception of the first letter.")
        .add_field("`[description]`", "The desctiption of the assignment. **The first parameter to be separated by a comma "
        "which doesn't include a prefix is set as the description, along with the rest of the message.**")
        .add_field("-", "**-**")
        .add_field("Note:", "When not specifying optional arguments, also skip the parameter prefixes. (such as 'time=' when leaving time out)")
    ) 
    embed5 = (
        hikari.Embed(
            title = "Updating assignments - `!update`",
            description = "`!update [MessageID], date=[date], time=[time], assignment type=[assignment_type], head=[heading], [description]`",
        )
        .add_field("`[date]` (optional)", "The deadline date in DD.MM.YYYY format. Also accepts `today`, `tomorrow`, or any of the weekdays (such as `monday`) "
        "optionally accompanied by the keyword 'next' (such as `next wednesday`); in these cases the upcoming weekday is selected as the deadline. If 'next' is included, "
        "the second upcoming weekday (skipping a week) is selected. The parameter prefix 'date=' can also "
        "be replaced by 'd=' and is case sensitive with the exception of the first letter.")
        .add_field("`[time]` (optional)", "The time of day in HH:MM format. If skipped, **defaults to 23:59.** The parameter prefix 'time=' can also be replaced by 't=' and "
        "is case sensitive with the exception of the first letter.")
        .add_field("`[atype]` (optional)", "The type of the assignment - `homework`, `h`, `reminder`, `r`, `project`, `p`, `test`, or `t`. Affects the thumbnail and color of the "
        "assignment message. The parameter prefix 'assignment type=' can also be replaced by 'atype=', 'at', or 't', and "
        "is case sensitive with the exception of the first letter.")
        .add_field("`[heading]` (optional)", "Sets the heading of the assignment message. If skipped, **defaults to 'Assignment'.** The parameter prefix 'head=' can also "
        "be replaced by 'h=' and is case sensitive with the exception of the first letter.")
        .add_field("`[description]`", "The desctiption of the assignment. **The first parameter to be separated by a comma "
        "which doesn't include a prefix is set as the description, along with the rest of the message.**")
        .add_field("-", "**-**")
        .add_field("Getting the ID of the assignment message", "Right click the message and select Copy ID. Make sure that Developer Mode is turned on under User Settings - Advanced.")
        .add_field("Note:", "When not specifying optional arguments, also skip the parameter prefixes. (such as 'time=' when leaving time out)")
        .add_field("Note:", "If the date of the deadline changes, the message is deleted and resent into the correct text channel if needed. In this case, the reactions are reset.")
    ) 
    await ctx.respond(embed1)
    await ctx.respond(embed2)
    await ctx.respond(embed3)
    await ctx.respond(embed4)
    await ctx.respond(embed5)

bot.scheduler = AsyncIOScheduler()
bot.scheduler.configure(timezone=utc)
bot.load_extensions_from("./hikari_ppbot_public/extentions")



@bot.listen(hikari.StartingEvent)
async def on_starting(event):
    bot.db = await aiosqlite.connect("data/database.sqlite3")
    with open("data/build.sql") as f:
        await bot.db.executescript(f.read())
    #bot.scheduler.add_job(bot.db.commit, CronTrigger(second=0))


@bot.listen(hikari.StoppingEvent)
async def on_stopping(event):
    await bot.db.commit()
    await bot.db.close()
    bot.scheduler.shutdown()

# @bot.listen(hikari.GuildReactionAddEvent)
# async def on_reaction_switch(event:hikari.GuildReactionAddEvent):
#     cur = await event.app.db.execute(
#         "SELECT e.incompleteName, e.incompleteSnow, e.completeName, e.completeSnow "
#         "FROM emoji_list e "
#         "INNER JOIN assignment_list a USING (guildID) "
#         "WHERE a.messageID = ?",
#         (event.message_id,)         
#     )
#     if not (result := await cur.fetchone()):
#         return
    
#     message = await event.app.rest.fetch_message(event.channel_id, event.message_id)
#     print(event.emoji_id)
#     print(result[1])
#     print(result[3])
#     if event.emoji_id == result[1]:
#         await message.remove_reaction(result[2], int(result[3]), user=event.user_id)
#     elif event.emoji_id == result[3]:
#         await message.remove_reaction(result[0], int(result[1]), user=event.user_id)

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    bot.scheduler.start()
    guilds = await bot.rest.fetch_my_guilds()

    # await bot.db.executemany(
    #     "INSERT INTO guild_list VALUES (?) ON CONFLICT DO NOTHING", 
    #     ([g.id for g in guilds],)
    # )
    # await bot.db.executemany(
    #     "INSERT INTO channel_list (guildID) VALUES (?) ON CONFLICT DO NOTHING", 
    #     ([g.id for g in guilds],)
    # )
    # await bot.db.executemany(
    #     "INSERT INTO emoji_list (guildID) VALUES (?) ON CONFLICT DO NOTHING", 
    #     ([g.id for g in guilds],)
    # )

    guildlist = []
    for g in guilds:
        guildlist.append((g.id,))

    await bot.db.executemany("INSERT INTO guild_list VALUES (?) ON CONFLICT DO NOTHING", guildlist)
    await bot.db.executemany("INSERT INTO channel_list (guildID) VALUES (?) ON CONFLICT DO NOTHING", guildlist)
    await bot.db.executemany("INSERT INTO emoji_list (guildID) VALUES (?) ON CONFLICT DO NOTHING", guildlist)

    await bot.db.commit()
    print("ready :)")

@bot.listen(hikari.GuildJoinEvent)
async def on_guild_join(event):
    guilds = await bot.rest.fetch_my_guilds()
    guildlist = []
    for g in guilds:
        guildlist.append((g.id,))

    await bot.db.executemany("INSERT INTO guild_list VALUES (?) ON CONFLICT DO NOTHING", guildlist)
    await bot.db.executemany("INSERT INTO channel_list (guildID) VALUES (?) ON CONFLICT DO NOTHING", guildlist)
    await bot.db.executemany("INSERT INTO emoji_list (guildID) VALUES (?) ON CONFLICT DO NOTHING", guildlist)

    await bot.db.commit()
    print("New Server Joined :)")

@bot.listen(hikari.GuildLeaveEvent)
async def on_guild_leave(event):
    print(event.guild_id)
    await bot.db.execute("DELETE FROM guild_list WHERE guildID = ?", (event.guild_id,))
    await bot.db.execute("DELETE FROM channel_list WHERE guildID = ?", (event.guild_id,))
    await bot.db.execute("DELETE FROM emoji_list WHERE guildID = ?", (event.guild_id,))
    await bot.db.execute("DELETE FROM assignment_list WHERE guildID = ?", (event.guild_id,))

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