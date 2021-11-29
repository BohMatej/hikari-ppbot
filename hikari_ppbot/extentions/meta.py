import lightbulb


class Meta(lightbulb.Plugin):
    @lightbulb.command(name="ping", help="sdfsdfzfdssdffsd")
    async def pingcmd(self, ctx):
        await ctx.respond(ctx.message.content)
    # testemoji = await ctx.get_guild().fetch_emoji(906211448181624863)
    # await ctx.respond(testemoji)
    # await ctx.message.add_reaction(":testemoji:")
    # channel = await ctx.bot.rest.fetch_channel(882583345802907708)
    # await channel.send("Pong!")
    
    


def load(bot):
    bot.add_plugin(Meta())



def unload(bot):
    bot.remove_plugin("Meta")
