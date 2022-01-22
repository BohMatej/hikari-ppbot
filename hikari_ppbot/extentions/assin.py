# from hikari import undefined
import hikari
import lightbulb, datetime


class Assin(lightbulb.Plugin):
    @lightbulb.command(name="assign", help="sdfsdfzfdssdffsd")
    async def assin(self, ctx, *, details: str):
        # print (details)
        arguments = details.split(",")
        # print(arguments)

        time_startswith = [
            "t=",
            "t =",
            "T=",
            "T =",
            "time=",
            "time =",
            "Time=",
            "Time ="
        ]

        arg_date = ""
        arg_time = ""
        arg_details = ""
        cont_to_details = False # checked to determine whether the rest of the args are details

        for i in range(len(arguments)):
            arguments[i] = arguments[i].strip()
            cont_to_details = True
            
            if i == 0: # first argument is always date
                arg_date = arguments[i].lower()
                cont_to_details = False
                continue

            for ts in time_startswith: # find time argument
                if arguments[i].startswith(ts) and arg_time == "":
                    arg_time = arguments[i].replace(ts, "").strip()
                    cont_to_details = False
                    break

            if cont_to_details == True:
                for j in range(i, len(arguments)):
                    arg_details += arguments[j]
                break

        if arg_date == "today":
            print("im here")
            arg_date = datetime.date.today().strftime("%d.%m.%Y")
        if arg_date == "tomorrow":
            d = datetime.date.today() + datetime.timedelta(days=1)
            arg_date = d.strftime("%d.%m.%Y")
        if arg_date == "next week" or arg_date == "nextweek":
            d = datetime.date.today() + datetime.timedelta(days=7)
            arg_date = d.strftime("%d.%m.%Y")
        
        weekday_list = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        wd_add = 0
        if "next" in arg_date:
            wd_add = 7
            arg_date = arg_date.replace("next", "").strip()
        for i in range(7):
            if arg_date == weekday_list[i]:
                daydelta = (i - datetime.date.today().weekday())
                if daydelta <= 0:
                    daydelta += 7
                #if wd_add == 7: wd_add = 14
                #if wd_add == 0: wd_add = 7
                print(wd_add)
                d = datetime.date.today() + datetime.timedelta(days=(wd_add+daydelta))
                arg_date = d.strftime("%d.%m.%Y")

        if arg_time == "": # set a default time argument
            arg_time = "23:59"

        print(f"date: {arg_date}")
        print(f"time: {arg_time}")
        print(f"details: {arg_details}")

        d_splitters = [".", "-", "/", ","]
        t_splitters = [".", "-", ":", ",", ";"]
        for splitter in d_splitters:
            arg_date = arg_date.replace(splitter, "-")
        arg_date = arg_date.split("-")
        for splitter in t_splitters:
            arg_time = arg_time.replace(splitter, "-")
        arg_time = arg_time.split("-")
        
        # print(arg_date)
        # print(arg_time)

        for check in arg_date:
            if check.isdigit() == False:
                await ctx.respond("Invalid date input!")
                return
        for check in arg_time:
            if check.isdigit() == False:
                await ctx.respond("Invalid time input!")
                return


        deadline_datetime = datetime.datetime(
            int(arg_date[2]),
            int(arg_date[1]),
            int(arg_date[0]),
            int(arg_time[0]),
            int(arg_time[1]),
        )

        syschannel = await ctx.bot.rest.fetch_channel(await ctx.bot.rest.fetch_guild(ctx.message.guild_id))
        cur = await ctx.bot.db.execute(
            "SELECT * FROM channel_list "
            "WHERE guildID = ?",
            (ctx.message.guild_id,)
        )
        weekday_channels_raw = await cur.fetchall()
        #print(weekday_channels_raw)
        
        weekday_channels = []
        for val in weekday_channels_raw[0]:
            try:
                weekday_channels.append(int(val))
            except TypeError:
                weekday_channels.append(syschannel.id)

        channel = await ctx.bot.rest.fetch_channel(weekday_channels[deadline_datetime.weekday()+1])

        cur = await ctx.bot.db.execute(
            "SELECT * FROM emoji_list "
            "WHERE guildID = ?",
            (ctx.message.guild_id,)
        )
        emoji_raw = await cur.fetchall()
        #print(emoji_raw)

        embed = (
            hikari.Embed(
                title = "Assignment Reminder", 
                description = arg_details,
                colour = 0xFF0000,
            )
            .add_field("Due date: ", deadline_datetime.strftime("%d.%m.%Y %H:%M"))
        )

        asgembed = await channel.send(embed)
        
        try:
            await asgembed.add_reaction(emoji_raw[0][1], int(emoji_raw[0][2]))
        except TypeError:
            await asgembed.add_reaction("✅")

        try:
            await asgembed.add_reaction(emoji_raw[0][3], int(emoji_raw[0][4]))
        except TypeError:
            await asgembed.add_reaction("❌")

        # asgmessage = await channel.send(arg_details)
        # await asgmessage.add_reaction("testemoji", 906211448181624863)
        
        await ctx.bot.db.execute(
            "INSERT INTO assignment_list "
            "VALUES (?, ?, ?, ?, ?, ?)", 
            (
                ctx.guild_id,
                weekday_channels[deadline_datetime.weekday()+1], 
                asgembed.id,
                arg_details,
                deadline_datetime.isoformat(" "),
                0,
            )
        )

    @lightbulb.command(name="setemoji", help="sets an emoji that the bot will use to determine users who finished / haven't finished assignments. Type !help for more.")
    async def setemoji(self, ctx, *, details: str):
        arguments = details.split(",")

        g = ctx.message.guild_id
        emojitype = arguments[0].strip()
        emojiname = arguments[1].strip()
        emojisnow = arguments[2].strip()

        if emojitype == "complete":
            await ctx.bot.db.execute(
                "UPDATE emoji_list SET completeName=?, completeSnow=? WHERE guildID = ?",
                (emojiname, emojisnow, g)
            ) # better way to write this command?
        elif emojitype == "incomplete":
            await ctx.bot.db.execute(
                "UPDATE emoji_list SET incompleteName=?, incompleteSnow=? WHERE guildID = ?",
                (emojiname, emojisnow, g)
            ) # better way to write this command?

    @lightbulb.command(name="setchannel", help="sets a channel that the bot will message assignments into for a specific weekday. Type !help for more.")
    async def setchannel(self, ctx, *, details: str):
        arguments = details.split(",")

        g = ctx.message.guild_id
        day = arguments[0].strip()
        channelID = arguments[1].strip()
        cur = await ctx.bot.db.execute(
            f"UPDATE channel_list SET {day}=? WHERE guildID = ?",
            (channelID, g)
        ) # better way to write this command?
    





def load(bot):
    bot.add_plugin(Assin())



def unload(bot):
    bot.remove_plugin("Assin")




    # async def assin(self, ctx, deadline_date: str, deadline_time: str, *, details: str): #make divider thingy something other than space?
    #     print(f"deadline_date: {deadline_date}, deadline_time: {deadline_time}, *, details: {details}")
    #     d = deadline_date
    #     t = deadline_time
    #     d_splitters = [".", "-", "/", ","]
    #     t_splitters = [".", "-", ":", ",", ";"]
    #     for splitter in d_splitters:
    #         d = d.replace(splitter, "-")
    #     d = d.split("-")
    #     for splitter in t_splitters:
    #         t = t.replace(splitter, "-")
    #     t = t.split("-")
        
    #     print(d)
    #     print(t)

    #     deadline_datetime = datetime.datetime(
    #         int(d[2]),
    #         int(d[1]),
    #         int(d[0]),
    #         int(t[0]),
    #         int(t[1]),
    #     )

    #     weekday_channels = [
    #         882583345802907708,
    #         882583367193878579,
    #         882583386416349204,
    #         913527188035350528,
    #         913527232029392966,
    #         913528417603960893,
    #         914979194813972530
    #     ]

    #     channel = await ctx.bot.rest.fetch_channel(weekday_channels[deadline_datetime.weekday()])

    #     # deadline_datetime = datetime.datetime(2004, 7, 29, 11, 3)
    #     print(deadline_datetime)
    #     # await ctx.respond(deadline_datetime.strftime("%A, %d. %B %Y %I:%M%p"))
    #     # await channel.send(deadline_datetime.strftime("%A, %d. %B %Y %I:%M%p"))
    #     asgmessage = await channel.send(details)
    #     await asgmessage.add_reaction("testemoji", 906211448181624863)
    #     await asgmessage.add_reaction("white_check_mark", 914981058074771467)
    #     await asgmessage.add_reaction("x", 914981140899700758)
    #     # await ctx.respond(ctx.message.content)