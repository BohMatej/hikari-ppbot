import hikari
import lightbulb
from lightbulb import plugins


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
        

    #@plugins.listener()
    #async def on_command_error(se)



def load(bot):
    bot.add_plugin(React())



def unload(bot):
    bot.remove_plugin("React")