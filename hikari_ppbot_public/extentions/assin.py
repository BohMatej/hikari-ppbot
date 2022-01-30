from ast import arguments
from email import header
import hikari
import lightbulb, datetime

from matplotlib.image import thumbnail


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

        atype_startswith = [
            "assignment type=",
            "Assignment type=",
            "assignment type =",
            "Assignment type =",
            "atype=",
            "Atype=",
            "atype =",
            "Atype =",
            "a=",
            "A =",
            "a =",
            "A=",
            "at=",
            "At=",
            "at =",
            "At =",
            "AT=",
            "AT =",
        ]

        head_startswith = [
            "h=",
            "h =",
            "H=",
            "H =",
            "head=",
            "head =",
            "Head=",
            "Head ="
        ]

        arg_date = ""
        arg_time = ""
        arg_atype = ""
        arg_head = ""
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
                arglowered = arguments[i].lower()
                if arglowered.startswith(ts) and arg_time == "":
                    arg_time = arguments[i].replace(ts, "").strip()
                    cont_to_details = False
                    break
            
            for ats in atype_startswith: # find assignment type argument
                arglowered = arguments[i].lower()
                if arglowered.startswith(ats) and arg_atype == "":
                    arg_atype = arguments[i].replace(ats, "").strip()
                    cont_to_details = False
                    break
            
            for hs in head_startswith: # find assignment type argument
                arglowered = arguments[i].lower()
                if arglowered.startswith(hs) and arg_head == "":
                    arg_head = arguments[i].replace(hs, "").strip()
                    cont_to_details = False
                    break

            if cont_to_details == True:
                for j in range(i, len(arguments)):
                    arg_details += arguments[j]
                break
        
        #############setup date

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

        #############setup time and datetime

        if arg_time == "": # set a default time argument
            arg_time = "23:59"

        d_splitters = [".", "-", "/", ","]
        t_splitters = [".", "-", ":", ",", ";"]
        for splitter in d_splitters:
            arg_date = arg_date.replace(splitter, "-")
        arg_date = arg_date.split("-")
        for splitter in t_splitters:
            arg_time = arg_time.replace(splitter, "-")
        arg_time = arg_time.split("-")

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

        #############setup atype and color
        arg_atype = arg_atype.lower().strip()
        if arg_atype == "homework" or arg_atype == "h":
            url = "https://i.imgur.com/1c0WaqC.png"
            col = 0x1c8adb
        elif arg_atype == "reminder" or arg_atype == "r":
            url = "https://i.imgur.com/H9CqPo3.png"
            col = 0xfecc4e
        elif arg_atype == "project" or arg_atype == "p":
            url = "https://i.imgur.com/bi8a7CR.png"
            col = 0x7030a1
        elif arg_atype == "test" or arg_atype == "t":
            url = "https://i.imgur.com/y4GMZvW.png"
            col = 0x40b7ad
        elif arg_atype == "":
            col = 0x000000
        else:
            msg = (
            "Invalid assignment type input! "
            "Valid types are \"homework\", \"reminder\", \"project\", \"test\", "
            "or their single character equivalents \"h\", \"r\", \"p\", and \"t\"."
            )
            await ctx.respond(msg)
            return

        #############setup heading and color


        if arg_head == "":
            arg_head = "Assignment"

        #############setup channel

        defchannel = await ctx.bot.rest.fetch_channel(ctx.message.channel_id)
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
                weekday_channels.append(defchannel.id)

        channel = await ctx.bot.rest.fetch_channel(weekday_channels[deadline_datetime.weekday()+1])

        cur = await ctx.bot.db.execute(
            "SELECT * FROM emoji_list "
            "WHERE guildID = ?",
            (ctx.message.guild_id,)
        )
        emoji_raw = await cur.fetchall()
        print(arg_head)

        embed = (
            hikari.Embed(
                title = arg_head, 
                description = arg_details,
                colour = col,
            )
            .add_field("Due date: ", deadline_datetime.strftime("%d.%m.%Y %H:%M"))
        )
        if arg_atype != "":
            embed.set_thumbnail(url)

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
        await ctx.bot.db.commit()
        #delete user's message
        await ctx.bot.rest.delete_message(ctx.message.channel_id, ctx.message)


    


    @lightbulb.command(name="setemoji", help="sets an emoji that the bot will use to determine users who finished / haven't finished assignments. Type !help for more.")
    async def setemoji(self, ctx, *, args: str):
        arguments = args.split(",")

        g = ctx.message.guild_id
        emojitype = arguments[0].strip()
        emojisnow = arguments[1].strip()

        if emojisnow == "default":
            if emojitype == "complete":
                await ctx.bot.db.execute(
                    "UPDATE emoji_list SET completeName=?, completeSnow=? WHERE guildID = ?",
                    (None, None, g)
                ) # better way to write this command?
            elif emojitype == "incomplete":
                await ctx.bot.db.execute(
                    "UPDATE emoji_list SET incompleteName=?, incompleteSnow=? WHERE guildID = ?",
                    (None, None, g)
                ) # better way to write this command?
            else:
                ctx.message.respond("Set a valid emoji type: \"complete\" or \"incomplete\"")
        else:
            emojiname = arguments[2].strip()
            
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
            else:
                ctx.message.respond("Set a valid emoji type: \"complete\" or \"incomplete\"")
        await ctx.bot.db.commit()
        #delete user's message
        await ctx.bot.rest.delete_message(ctx.message.channel_id, ctx.message)

    @lightbulb.command(name="setchannel", help="sets a channel that the bot will message assignments into for a specific weekday. Type !help for more.")
    async def setchannel(self, ctx, *, args: str):
        arguments = args.split(",")

        g = ctx.message.guild_id
        day = arguments[0].lower().strip()
        channelID = arguments[1].lower().strip()
        cur = await ctx.bot.db.execute(
            f"UPDATE channel_list SET {day}=? WHERE guildID = ?",
            (channelID, g)
        ) # better way to write this command?
        await ctx.bot.db.commit()
        #delete user's message
        await ctx.bot.rest.delete_message(ctx.message.channel_id, ctx.message)
    





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