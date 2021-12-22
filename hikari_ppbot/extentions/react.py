import datetime
import hikari
import lightbulb
from lightbulb import plugins
from apscheduler.triggers.cron import CronTrigger

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
            "(ChannelID, MessageID, DueDate)"
            "VALUES (?, ?, ?)", 
            (ctx.channel_id, ctx.message.id, date.isoformat(" "))
        )
        print(cur.rowcount)

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
            "SELECT * "
            "FROM assignment_list "
            "WHERE DueDate < datetime('now', '+1 days')" 
            "AND DueDate > datetime('now', '+23 hours')"
        )
        results = await cur.fetchall()

        for result in results:
            if result[3] == 1:
                return
            
            embed = (
                hikari.Embed(
                    title = "Assignment Reminder", 
                    description = "fsaddfsasfdfsdfsd",
                    colour = 0xFF0000,
                )
                .add_field("Due date: ", result[2])
            )
            user = await bot.rest.fetch_user(341218733546668033)
            await user.send(embed)


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
    bot.scheduler.add_job(
        r.scheduled_dms, 
        CronTrigger(second=30),
        args = [bot])
    



def unload(bot):
    bot.remove_plugin("React")