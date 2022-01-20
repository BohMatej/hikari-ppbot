import hikari, lightbulb


class Meta(lightbulb.Plugin):
    @lightbulb.command(name="ping", help="sdfsdfzfdssdffsd")
    async def pingcmd(self, ctx):
        await ctx.respond(ctx.message.content)
    # testemoji = await ctx.get_guild().fetch_emoji(906211448181624863)
    # await ctx.respond(testemoji)
    # await ctx.message.add_reaction(":testemoji:")
    # channel = await ctx.bot.rest.fetch_channel(882583345802907708)
    # await channel.send("Pong!")
        #syschannel = hikari.api.rest.RESTClient.fetch_guild(ctx.message.guild_id)
        syschannel = await ctx.bot.rest.fetch_channel(await ctx.bot.rest.fetch_guild(ctx.message.guild_id))
        msg = await syschannel.send("aaaaaaaaaaa")
        await msg.add_reaction("testemoji", 906211448181624863)
    


def load(bot):
    bot.add_plugin(Meta())



def unload(bot):
    bot.remove_plugin("Meta")
