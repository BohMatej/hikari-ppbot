import lightbulb, re, datetime


class Assin(lightbulb.Plugin):
    @lightbulb.command(name="assign", help="sdfsdfzfdssdffsd")
    async def assin(self, ctx, deadline_date: str, deadline_time: str, *, details: str): #make divider thingy something other than space?
        print(f"deadline_date: {deadline_date}, deadline_time: {deadline_time}, *, details: {details}")
        d = deadline_date
        t = deadline_time
        d_splitters = [".", "-", "/", ","]
        t_splitters = [".", "-", ":", ",", ";"]
        for splitter in d_splitters:
            d = d.replace(splitter, "-")
        d = d.split("-")
        for splitter in t_splitters:
            t = t.replace(splitter, "-")
        t = t.split("-")
        
        print(d)
        print(t)

        deadline_datetime = datetime.datetime(
            int(d[2]),
            int(d[1]),
            int(d[0]),
            int(t[0]),
            int(t[1]),
        )

        weekday_channels = [
            882583345802907708,
            882583367193878579,
            882583386416349204,
            913527188035350528,
            913527232029392966,
            913528417603960893,
            914979194813972530
        ]

        channel = await ctx.bot.rest.fetch_channel(weekday_channels[deadline_datetime.weekday()])

        # deadline_datetime = datetime.datetime(2004, 7, 29, 11, 3)
        print(deadline_datetime)
        # await ctx.respond(deadline_datetime.strftime("%A, %d. %B %Y %I:%M%p"))
        # await channel.send(deadline_datetime.strftime("%A, %d. %B %Y %I:%M%p"))
        await channel.send(details)
        # await ctx.respond(ctx.message.content)


def load(bot):
    bot.add_plugin(Assin())



def unload(bot):
    bot.remove_plugin("Assin")
