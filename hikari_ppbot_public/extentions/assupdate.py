from ast import arguments
from email import header
import hikari
import lightbulb, datetime

from matplotlib.image import thumbnail



class Assupdate(lightbulb.Plugin):
    @lightbulb.command(name="update", help="sdfsdfzfdssdffsd")
    async def update(self, ctx, *, details: str):
        arguments = details.split(",")
        # print(arguments)

        date_startswith = [
            "d=",
            "d =",
            "D=",
            "D =",
            "date=",
            "date =",
            "Date=",
            "Date ="
        ]

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
            "type=",
            "Type=",
            "type =",
            "Type =",
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

        arg_messageid = ""
        arg_date = None
        arg_time = ""
        arg_atype = ""
        arg_head = ""
        arg_details = ""
        cont_to_details = False # checked to determine whether the rest of the args are details

        for i in range(len(arguments)):
            arguments[i] = arguments[i].strip()
            cont_to_details = True
            
            if i == 0: # first argument is always date
                arg_messageid = arguments[i].lower().strip()
                if arg_messageid.isdigit() == False:
                    await ctx.respond("Invalid messageID input!")
                    print(arg_messageid)
                    return
                cont_to_details = False
                continue
            
            for ds in date_startswith: # find time argument
                arglowered = arguments[i].lower()
                if arglowered.startswith(ds) and arg_date == "":
                    arg_date = arguments[i].replace(ds, "").strip()
                    cont_to_details = False
                    break

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
        
        cur = await ctx.bot.db.execute(
            "SELECT ChannelID, MessageID, DueDate "
            "FROM assignment_list "
            "WHERE MessageID = ?", (arg_messageid,)
        )
        results = await cur.fetchall() # results[0][0] = ChannelID, results[0][1] = MessageID, results[0][2] = DueDate bcuz tuple


        #############setup date

        if arg_date != None:
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
        else:
            print(results)
            arg_date = f"{results[0][2][8:10]}.{results[0][2][5:7]}.{results[0][2][0:4]}"
        
        print(arg_date)
        #############setup time and datetime

        if arg_time == "": # set a default time argument
            arg_time = results[0][2][11:16]

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
        elif arg_atype == "default":
            col = 0x000000
        elif arg_atype != "":
            msg = (
            "Invalid assignment type input! "
            "Valid types are \"homework\", \"reminder\", \"project\", \"test\", "
            "or their single character equivalents \"h\", \"r\", \"p\", and \"t\"."
            )
            await ctx.respond(msg)
            return

        #############setup heading and color

        if arg_head == "default":
            arg_head = "Assignment"
        
        ##########################################Before enabling code below, make sure the command can update existing embeds

        # #############setup channel 

        # defchannel = await ctx.bot.rest.fetch_channel(ctx.message.channel_id)
        # cur = await ctx.bot.db.execute(
        #     "SELECT * FROM channel_list "
        #     "WHERE guildID = ?",
        #     (ctx.message.guild_id,)
        # )
        # weekday_channels_raw = await cur.fetchall()
        # #print(weekday_channels_raw)
        
        # weekday_channels = []
        # for val in weekday_channels_raw[0]:
        #     try:
        #         weekday_channels.append(int(val))
        #     except TypeError:
        #         weekday_channels.append(defchannel.id)

        # channel = await ctx.bot.rest.fetch_channel(weekday_channels[deadline_datetime.weekday()+1])

        # cur = await ctx.bot.db.execute(
        #     "SELECT * FROM emoji_list "
        #     "WHERE guildID = ?",
        #     (ctx.message.guild_id,)
        # )
        # emoji_raw = await cur.fetchall()
        # print(arg_head)


def load(bot):
    bot.add_plugin(Assupdate())


def unload(bot):
    bot.remove_plugin("Assupdate")
