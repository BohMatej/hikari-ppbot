import lightbulb, re, datetime


class Assin(lightbulb.Plugin):
    @lightbulb.command(name="assign", help="sdfsdfzfdssdffsd")
    async def assin(self, ctx, deadline_date: str, deadline_time: str, *, details: str): #make divider thingy something other than space?
        print(f"deadline_date: {deadline_date}, deadline_time: {deadline_time}, *, details: {details}")
        d = deadline_date
        t = deadline_time
        d = re.split("[.-/]", d)
        print(d)
        t = re.split("[.-/]", t)
        print(t)
        deadline_datetime = datetime.datetime(
            int(d[2]),
            int(d[1]),
            int(d[0]),
            int(t[0]),
            int(t[1]),
        )
        # deadline_datetime = datetime.datetime(2004, 7, 29, 11, 3)
        print(deadline_datetime)
        await ctx.respond(deadline_datetime.strftime("%A, %d. %B %Y %I:%M%p"))
        # await ctx.respond(ctx.message.content)


def load(bot):
    bot.add_plugin(Assin())



def unload(bot):
    bot.remove_plugin("Assin")
