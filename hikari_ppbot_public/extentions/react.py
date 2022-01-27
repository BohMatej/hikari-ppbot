from asyncio.windows_events import NULL
import datetime
from email import message
import hikari
import lightbulb
from lightbulb import plugins
from apscheduler.triggers.cron import CronTrigger
from matplotlib.style import use

class React(lightbulb.Plugin):
    @lightbulb.command(name="react", help="sdfsdfzfdssdffsd")
    async def react(self, ctx: lightbulb.Context):
        channel = await ctx.bot.rest.fetch_channel(882583345802907708)
        msg = await channel.send("aaaaaaaaaaa")
        await msg.add_reaction("testemoji", 906211448181624863)
    
    @lightbulb.command(name="dm", help="dms or sth")
    async def dm(self, ctx, target: hikari.Member, *, message: str):
        print(str (target) + " " + str(message))

        # if :
        #    return await ctx.respond("User does not exist/is not in the server.")

        try:
            for i in range(10):
                await target.send(message)
        except hikari.ForbiddenError:
            await ctx.respond("User has DMs off.")

    @lightbulb.command(name="insert", help="inserts or sth")
    async def insert(self, ctx, *, date: str):
        date = datetime.datetime.strptime(date, "%d/%m/%Y %H:%M")
        print("yay")
        cur = await ctx.bot.db.execute(
            "INSERT INTO assignment_list "
            "VALUES (?, ?, ?, ?, ?, ?)", 
            (
                ctx.guild_id,
                ctx.channel_id, 
                ctx.message.id,
                ctx.message.content,
                date.isoformat(" "),
                0,
            )
        )
        print(cur.rowcount)
        
        # cur = await ctx.bot.db.execute("SELECT mon FROM channel_list WHERE guildID = ?", (ctx.guild_id,))
        # channel = await ctx.bot.rest.fetch_channel(await cur.fetchone()) or ctx.get_guild().system_channel_id
        # await channel.send("aaaaaaaaaaa")

    @lightbulb.command(name="select", help="selects or sth")
    async def select(self, ctx):
        cur = await ctx.bot.db.execute(
            "SELECT * "
            "FROM assignment_list "
            "WHERE DueDate < datetime('now', '+1 days')" 
            "AND DueDate > datetime('now')"
        )
        results = await cur.fetchall()




        print(results)
    async def scheduled_dms(self, bot):
        cur = await bot.db.execute(
            "SELECT a.channelID, a.messageID, a.DueDate, a.Notified, a.details, e.incompleteName, e.incompleteSnow "
            "FROM assignment_list a " 
            "INNER JOIN emoji_list e USING (guildID) "
            "WHERE a.DueDate < datetime('now', '+1 days', 'localtime') " 
            "AND a.DueDate > datetime('now', 'localtime') "
            "AND a.Notified = 0"
        )
        results = await cur.fetchall()
        print(results)

        for result in results: 
            await bot.db.execute("UPDATE assignment_list SET Notified = 1 WHERE messageID = ?", (result[1],))
            embed = (
                hikari.Embed(
                    title = "Assignment Reminder", 
                    description = "fsaddfsasfdfsdfsd",
                    colour = 0xFF0000,
                )
                .add_field("Due date: ", result[2])
            )
            #for users in bot.rest.fetch_reactions_for_emoji(results[1], results[2], ):

            # channel = bot.cache.get_guild_channel(result[0])
            # message = await channel.fetch_message(result[1])

            if result[5] == None:
                async for user in bot.rest.fetch_reactions_for_emoji(result[0], result[1], "❌"):
                    if user.is_bot:
                        continue
                    print("None")
                    await user.send(embed)

            else: 
                async for user in bot.rest.fetch_reactions_for_emoji(result[0], result[1], result[5], result[6]):
                    if user.is_bot:
                        continue
                    print("Not none")
                    await user.send(embed)
        await bot.db.commit()
    async def scheduled_datadelete(self, bot):
        cur = await bot.db.execute(
            "SELECT ChannelID, MessageID "
            "FROM assignment_list "
            "WHERE DueDate < datetime('now', 'localtime')" 
        )
        results = await cur.fetchall()
        print(results)

        await bot.db.execute(
            "DELETE FROM assignment_list "
            "WHERE DueDate < datetime('now', 'localtime')" 
        )

        for result in results:
            try:
                await bot.rest.delete_message(result[0], result[1])
            except:
                pass

        



    #@plugins.listener()
    #async def on_command_error(se)


class Scheduletask(lightbulb.Plugin):
    @lightbulb.command(name="react", help="sdfsdfzfdssdffsd")
    async def react(self, ctx: lightbulb.Context):
        channel = await ctx.bot.rest.fetch_channel(882583345802907708)
        msg = await channel.send("aaaaaaaaaaa")
        await msg.add_reaction("testemoji", 906211448181624863)
    
    


def load(bot):
    r = React()
    bot.add_plugin(r)
    bot.scheduler.add_job(r.scheduled_dms, CronTrigger(second="0,30"), args = [bot])
    bot.scheduler.add_job(r.scheduled_datadelete, CronTrigger(second="15,45"), args = [bot])
    



def unload(bot):
    bot.remove_plugin("React")