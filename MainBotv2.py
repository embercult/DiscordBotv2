import discord
from discord.ext import commands
import asyncio
import codechefcrawlerv2 as cc
import sqlitedb as sql
import datetime
import otherapis as ot


from itertools import cycle
import os


bot = commands.Bot(command_prefix="!")


# Some variables
ver = 'v0.2.6.0'
invite = 'https://discordapp.com/oauth2/authorize?&client_id=477512556630507530&scope=bot&permissions=0'
img = 'https://i.imgur.com/GX02jaL.png'
foot = 'For a list of commands tpye "!commands"\n{}'.format(ver)
ccicon = 'https://pbs.twimg.com/profile_images/470882849885667329/X48adYnt_400x400.jpeg'
global verify
verify = {} # {codechef name : [Time , discord id , discord name , ctx.channel.id]} ##ctx.channel.id to Send message in the same channel if the user is verified (or not)
stats = ['A bot made by EmberCult','Current version {}'.format(ver),'Say !commands','A bot made by Viplav','Online and ready to use!','Found any error,DM EmberCult',"I'am Better than gg-chan"]

def rating2star(rating):
    star = 0
    rating = int(rating)
    if rating <= 1399:
        star = 1
    elif 1400 <= rating <= 1599:
        star = 2
    elif 1600 <= rating <= 1799:
        star = 3
    elif 1800 <= rating <= 1999:
        star = 4
    elif 2000 <= rating <= 2199:
        star = 5
    elif 2200 <= rating <= 2499:
        star = 6
    elif rating >= 2500:
        star = 7
    return star


def star2color(star):
    if star == 1:
        return '666666'
    elif star == 2:
        return '1E7D22'
    elif star == 3:
        return '3366CC'
    elif star == 4:
        return '684273'
    elif star == 5:
        return 'FFBF00'
    elif star == 6:
        return 'FF7F00'
    elif star == 7:
        return 'D0011B'


async def status():
    await bot.wait_until_ready()  # check if bot is ready!
    msgs = cycle(stats)
    while not bot.is_closed:
        current_msg = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_msg))
        await asyncio.sleep(10)


async def check():
    await bot.wait_until_ready()    # check if bot is ready!
    while not bot.is_closed:
        print(verify)
        for user in list(verify.keys()): # turn verify.keys in a list cuz u cant remove stuff from dict while iterating over it.
            print('verifying :  ', user)
            exist = cc.verify_user(user)  # check if the user actually submitted a solution or not!
            if exist:   # got bored of writing these comments sorry understand this shit yourself
                rate = cc.user_rating(user)
                sql.adduser(verify[user][1], verify[user][2], user, rate)
                print("User {} was verified and added to database".format(user))
                embed = discord.Embed(title='**LINK SUCCESSFUL**', description='*Links your codechef and discord ids*',
                                      color=discord.Color.green())
                embed.add_field(name='CONGRATS!',
                                value='Successfully verified your account! {} is linked to your account now!'.format(
                                    user))
                embed.set_footer(text=foot)
                embed.set_author(name='EC BOT', url=invite, icon_url=img)
                await bot.send_message(bot.get_channel(verify[user][3]), embed=embed)
                del verify[user]
            else:
                time_passed = datetime.datetime.utcnow() - verify[user][0]
                time_passed = str(time_passed).split(':')[1]
                print('failed to verify: ', user)
                if int(time_passed) >= 1:
                    print("removed the", verify[user], "as 60secs have passed!")
                    embed = discord.Embed(title='**LINK FAILED**', description='*Links your codechef and discord ids*',
                                          color=discord.Color.red())
                    embed.add_field(name='**ERROR**',
                                    value='Failed to verify your account! {} is **NOT** linked to your account!'.format(user))
                    embed.set_footer(text=foot)
                    embed.set_author(name='EC BOT',url=invite, icon_url = img)
                    await bot.send_message(bot.get_channel(verify[user][3]), embed=embed)
                    del verify[user]
        await asyncio.sleep(60)


@bot.event
async def on_ready():
    print("BOT IS ONLINE")


@bot.command(pass_context=True)
async def version(ctx):
    embed = discord.Embed(title='**Current version**', description='{}!'.format(ver),
                          color=discord.Color.blue())
    embed.set_footer(text=foot)
    embed.set_author(name='EC BOT', url=invite, icon_url=img)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def ping(ctx):
    userid = ctx.message.author.id
    tnow = datetime.datetime.utcnow()
    lags = tnow-ctx.message.timestamp
    lags = str(lags).split(':')[2]

    embed = discord.Embed(title='PONG :ping_pong:', description='<@{}>  , took {} secs!'.format(userid, lags), color=discord.Color.blue())
    embed.add_field(name='Number of server', value=len(bot.servers))
    embed.set_footer(text=foot)
    embed.set_author(name='EC BOT', url=invite, icon_url=img)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def cookie(ctx, user = None):
    embed = discord.Embed(title="**COOKIE DELIVERY!**", description= '*You received a :cookie:*', color=discord.Color.gold())
    if user == None:
        user = ctx.message.author.id
        embed.add_field(name='FROM', value='The almighty EC himself')
        embed.add_field(name='TO', value='<@{}>'.format(user))
    else:
        giver = ctx.message.author.id
        embed.add_field(name='FROM', value='<@{}>'.format(giver))
        embed.add_field(name='TO', value='{}'.format(user))
    embed.set_footer(text=foot)
    embed.set_author(name='EC BOT', url=invite, icon_url=img)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def rating(ctx, user = None):
    if user == None:
        embed = discord.Embed(title='**FAILED TO GET RATING**',
                              description='*Something stopped me from getting the rating!*',
                              color=discord.Color.red())
        embed.add_field(name='ERROR', value='Please provide a code chef username!   ')
    else:
        rating = cc.user_rating(user)
        if rating:
            rcolor = '0x00' + star2color(rating2star(rating))
            embed = discord.Embed(title='**RATING CARD**', description='Rating from Code Chef', color=int(rcolor,16))
            embed.add_field(name='USER', value='{}'.format(user), inline=True)
            embed.add_field(name='RATING', value='{}'.format(rating), inline=True)
            embed.add_field(name='STARS', value='{}'.format(rating2star(rating)), inline=True)
        else:
            embed = discord.Embed(title='**FAILED TO GET RATING**',
                                  description='*Something stopped me from getting the rating!*',
                                  color=discord.Color.red())
            embed.add_field(name='ERROR', value='No such user found!')

    embed.set_footer(text=foot)
    embed.set_thumbnail(url=ccicon)
    embed.set_author(name='EC BOT',
                     url=invite, icon_url = img)
    await bot.say(embed = embed)


@bot.command(pass_context=True)
async def link(ctx, user=None):
    sender = ctx.message.author.name
    sender_id = ctx.message.author.id
    time = ctx.message.timestamp
    if user == None:
        embed = discord.Embed(title='**FAILED TO LINK**', description='*Something stopped me from linking your codechef to your discord*', color=discord.Color.red())
        embed.add_field(name='ERROR', value='Please provide a code chef username!   ')
    else:
        if user in verify:
            embed = discord.Embed(title='**LINK**', description='*Links your codechef and discord ids*',
                                  color=discord.Color.red())
            embed.add_field(name='ERROR', value='Someone else is trying to link that account! Please wait!   ')
        else:
            rating = cc.user_rating(user)
            if rating:
                embed = discord.Embed(title='**LINKING**',
                                      description='*<@{}> Please follow the steps mentioned below to link {} to your discord*'.format(ctx.message.author.id,user),
                                      color=discord.Color.orange())
                embed.add_field(name='Go to this link and submit a solution!',
                                value='https://www.codechef.com/submit/HS08TEST'),
                embed.add_field(name='You have *1 min* to do so!',
                                value='Wrong answers will work!', inline=True)
                #verify['ads'] = ['asd','asd']
                verify.update({user:[time,sender_id,sender,ctx.message.channel.id]})
                #verify[str(user)] = [time, sender_id, sender, ctx.message.channel.id]
                print(verify)
            else:
                embed = discord.Embed(title='**VERIFYING**', description='**Links your codechef and discord ids**', color=discord.Color.red())
                embed.add_field(name='ERROR', value='No such user found!')

    embed.set_footer(text=foot)
    embed.set_author(name='EC BOT',
                     url=invite, icon_url = img)

    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def printdb(ctx):
    member = ctx.message.author.id
    if member == '139955846900613120':
        await bot.say(sql.printdb())


@bot.command(pass_context=True)
async def drating(ctx, user = None):
    if user == None:
        embed = discord.Embed(title='**DRATING**', description='*Rating from database!*', color=discord.Color.red())
        embed.add_field(name='**ERROR**', value='Please provide a discord username!   ')
    else:
        member = ctx.message.author.id
        try:
            x = sql.searchuser(user)
            rate = x[0]
            rcolor = '0x00' + star2color(rating2star(rate))
            embed = discord.Embed(title='**DRATING**', description='*Rating from database*', color=int(rcolor, 16))
            embed.add_field(name='USER', value='{}'.format(x[1]), inline=True)
            embed.add_field(name='RATING', value='{}'.format(rate), inline=True)
            embed.add_field(name='STARS', value='{}'.format(rating2star(rate)), inline=True)
        except (IndexError, TypeError) as e:
            await bot.say("""<@{}>, The user <@{}> has not linked their code chef profile with discord!
    Try searching with code chef handle using the command `!ccrating [name]`""".format(member, user.id))
            embed = discord.Embed(title='**DRATING**', description='*Rating from database*', color=discord.Color.red())
            embed.add_field(name='ERROR', value='No such user found in database!')
            embed.add_field(name='How to add to database?', value='Use the !link command to add to database!')

        embed.set_footer(text=foot)
        embed.set_author(name='EC BOT',
                         url=invite, icon_url = img)
        await bot.say(embed=embed)


@bot.group(pass_context=True)
async def commands(ctx):
    if ctx.invoked_subcommand is None:
        embed=discord.Embed(title="**COMMANDS**", description="*For more info on a command type !commands [command name]*", color=0xc016d3)
        embed.set_author(name="EC BOT",url=invite, icon_url = img)
        commands = 'ping\ncookie\nrating\nlink\ndrating\ntodo\ncontest\ninsult\npb'
        embed.add_field(name="*A list of commands the bot currently supports*", value=commands)
        embed.set_footer(text=foot)
        await bot.say(embed=embed)


@commands.command()
async def ping():
    embed = discord.Embed(title="**COMMAND HELP**", description="*Details about a command*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    embed.add_field(name="!ping", value="Checks if the bot is online and sends a message back with the respond time")
    embed.set_footer(text=foot)
    await bot.say(embed=embed)


@commands.command()
async def cookie():
    embed = discord.Embed(title="**COMMAND HELP**", description="*Details about a command*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    embed.add_field(name="!cookie [@user]", value="Sends a warm cookie to the mentioned user")
    embed.set_footer(text=foot)
    await bot.say(embed=embed)


@commands.command()
async def rating(c):
    embed = discord.Embed(title="**COMMAND HELP**", description="*Details about a command*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    embed.add_field(name="!rating [codechef name]", value="Tells the rating of [codechef name] from the codechef website")
    embed.set_footer(text=foot)
    await bot.say(embed=embed)


@commands.command()
async def link():
    embed = discord.Embed(title="**COMMAND HELP**", description="*Details about a command*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    embed.add_field(name="!link [codechef name]", value="Will link your discord id with the [codechef name]")
    embed.set_footer(text=foot)
    await bot.say(embed=embed)


@commands.command()
async def drating():
    embed = discord.Embed(title="**COMMAND HELP**", description="*Details about a command*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    embed.add_field(name="!drating [discord name]", value="Will tell the rating of [discord name] if they have linked their codechef\n**NOTE**:*Works with partial names too*")
    embed.set_footer(text=foot)
    await bot.say(embed=embed)


@commands.command()
async def todo():
    embed = discord.Embed(title="**COMMAND HELP**", description="*Details about a command*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    embed.add_field(name="!todo", value="Will display your todo list")
    embed.add_field(name="!todo [item]", value="Will add the [item] to your todo list")
    embed.add_field(name="!clrtodo", value="Will clear your todo list")
    embed.set_footer(text=foot)
    await bot.say(embed=embed)


@commands.command()
async def contest():
    embed = discord.Embed(title="**COMMAND HELP**", description="*Details about a command*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    embed.add_field(name="!contest", value="Displays a list of ongoing and upcoming codechef contests")
    embed.set_footer(text=foot)
    await bot.say(embed=embed)


@commands.command()
async def insult():
    embed = discord.Embed(title="**COMMAND HELP**", description="*Details about a command*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    embed.add_field(name="!insult [user]", value="Sends [user] an insult!")
    embed.set_footer(text=foot)
    await bot.say(embed=embed)


@commands.command()
async def pb():
    embed = discord.Embed(title="**COMMAND HELP**", description="*Details about a command*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    embed.add_field(name="!pb [language] [code]", value="Makes a pastebin paste with contents of your [code] and syntax highlighting is set to [language]")
    embed.set_footer(text=foot)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def todo(ctx,*message):
    uid = ctx.message.author.id
    embed = discord.Embed(title="**To Do List**", description="*A list of you need to do!*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite, icon_url = img)
    if len(message) == 0:
        tasks = sql.gettodo(uid)
        if len(tasks) == 0:
            embed.add_field(name='Empty list!',value='Add some items to your todo list now!')
        for i in range(len(tasks)):
            #this = list(map(this.strip("'"), this[0]))
            embed.add_field(name='Task#{}'.format(i+1), value='{}'.format(tasks[i][0]),inline=False)
    else:
        sql.addtodo(uid, ' '.join(message))
        embed.add_field(name='Task added', value='{}'.format(' '.join(message)))
    embed.set_footer(text=foot)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def clrtodo(ctx):
    uid = ctx.message.author.id
    sql.deltodo(uid)
    embed = discord.Embed(title="**To Do List Cleared**", description="*All items from your todo list have been removed!*",
                          color=0xc016d3)
    embed.set_footer(text=foot)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def contest(ctx):
    embed1 = discord.Embed(title="**CODE CHEF CONTESTS**", description="*A list of up coming and present code chef contest!*",
                          color=0xc016d3)
    contests = cc.live_contest()
    present = contests[1]
    # print (len(contests[0][present:]))
    # print(len(contests[0]))
    # print(contests[0][present:])
    # code , name , link , start date , start time , end date , end time
    embed2 = discord.Embed(title='**PRESENT CONTESTS**', description='*Currently running code chef contests!*' ,color=discord.Colour.dark_green())
    for i in range(len(contests[0][:present])):

        embed2.add_field(name='{} - {}'.format(contests[0][i][0], contests[0][i][1]),
                        value='Contest started on {} {} and will end on {} {}'.format(contests[0][i][4][:6],
                                                                                      contests[0][i][3],
                                                                                      contests[0][i][6][:6],
                                                                                      contests[0][i][5]), inline=False)
    embed3= discord.Embed(title='**UPCOMING CONTESTS**', description='*Code chef contests coming soon!*', color=discord.Colour.dark_orange() )
    for i in range(present, len(contests[0][present:]) + present):
        embed3.add_field(name='{} - {}'.format(contests[0][i][0], contests[0][i][1]),
                        value='Contest will start on {} {} and will end on {} {}'.format(contests[0][i][4][:6],
                                                                                         contests[0][i][3],
                                                                                         contests[0][i][6][:6],
                                                                                         contests[0][i][5]), inline=False)

    embed3.set_footer(text=foot)
    embed1.set_author(name="EC BOT", url=invite, icon_url=img)
    await bot.say(embed=embed1)
    await bot.say(embed=embed2)
    await bot.say(embed=embed3)


@bot.command(pass_context=True)
async def updatedb(ctx):
    member = ctx.message.author.id
    if member == '139955846900613120':
        sql.updatedb()
        await bot.say("Database ratings have been updated!")


@bot.command(pass_context=True)
async def gif(ctx,tag):
    await bot.say(ot.giphy(tag))


@bot.command(pass_context=True)
async def insult(ctx,person = None,destination=None):
    user = ctx.message.author.id
    insultstr = ot.insult()
    x = ['139955846900613120','<@139955846900613120>','<@!139955846900613120>','ember','viplav','embercult']

    if person == None:
        embed = discord.Embed(title='YOU GOT A INSULT!', description="*{} received a insult from <@477512556630507530>*".format(user) , color= discord.colour.Colour.dark_teal())
        embed.add_field(name="**{}**".format(insultstr), value=":fire:")

    elif person.lower() in x:
        embed = discord.Embed(title='YOU GOT A INSULT!',
                              description="*<@{}> received a insult from <@139955846900613120>*".format(user),
                              color=discord.colour.Colour.dark_teal())
        embed.add_field(name="**{}**".format(insultstr), value=":fire:")

    else:
        embed = discord.Embed(title='YOU GOT A INSULT!',
                              description="*{} received a insult from <@{}>*".format(person, user))
        embed.add_field(name="**{}**".format(insultstr), value=":fire:")


    embed.set_footer(text=foot)
    embed.set_author(name="EC BOT", url=invite, icon_url=img)
    await bot.say(embed = embed)


# async def send_insults():
#     await bot.wait_until_ready()  # check if bot is ready!
#     ids = ['476878010855981056','139955846900613120']
#     while not bot.is_closed:
#         for i in ids:
#             ins = ot.insult()
#             user = discord.Server.get_member('139955846900613120')
#             await bot.send_message(user, ins)
#         await asyncio.sleep(10)


@bot.command(pass_context=True)
async def pb(ctx,lang = 'text',*,msg):
    langs =  {"4cs" : "4CS", "6502acme" : "6502 ACME Cross Asse...", "6502kickass" : "6502 Kick Assembler", "6502tasm" : "6502 TASM/64TASS", "abap" : "ABAP", "actionscript" : "ActionScript", "actionscript3" : "ActionScript 3", "ada" : "Ada", "aimms" : "AIMMS", "algol68" : "ALGOL 68", "apache" : "Apache Log", "applescript" : "AppleScript", "apt_sources" : "APT Sources", "arm" : "ARM", "asm" : "ASM (NASM)", "asp" : "ASP", "asymptote" : "Asymptote", "autoconf" : "autoconf", "autohotkey" : "Autohotkey", "autoit" : "AutoIt", "avisynth" : "Avisynth", "awk" : "Awk", "bascomavr" : "BASCOM AVR", "bash" : "Bash", "basic4gl" : "Basic4GL", "dos" : "Batch", "bibtex" : "BibTeX", "blitzbasic" : "Blitz Basic", "b3d" : "Blitz3D", "bmx" : "BlitzMax", "bnf" : "BNF", "boo" : "BOO", "bf" : "BrainFuck", "c" : "C", "c_winapi" : "C (WinAPI)", "c_mac" : "C for Macs", "cil" : "C Intermediate Language", "csharp" : "C#", "cpp" : "C++", "cpp-winapi" : "C++ (WinAPI)", "cpp-qt" : "C++ (with Qt extensi...", "c_loadrunner" : "C: Loadrunner", "caddcl" : "CAD DCL", "cadlisp" : "CAD Lisp", "ceylon" : "Ceylon", "cfdg" : "CFDG", "chaiscript" : "ChaiScript", "chapel" : "Chapel", "clojure" : "Clojure", "klonec" : "Clone C", "klonecpp" : "Clone C++", "cmake" : "CMake", "cobol" : "COBOL", "coffeescript" : "CoffeeScript", "cfm" : "ColdFusion", "css" : "CSS", "cuesheet" : "Cuesheet", "d" : "D", "dart" : "Dart", "dcl" : "DCL", "dcpu16" : "DCPU-16", "dcs" : "DCS", "delphi" : "Delphi", "oxygene" : "Delphi Prism (Oxygene)", "diff" : "Diff", "div" : "DIV", "dot" : "DOT", "e" : "E", "ezt" : "Easytrieve", "ecmascript" : "ECMAScript", "eiffel" : "Eiffel", "email" : "Email", "epc" : "EPC", "erlang" : "Erlang", "euphoria" : "Euphoria", "fsharp" : "F#", "falcon" : "Falcon", "filemaker" : "Filemaker", "fo" : "FO Language", "f1" : "Formula One", "fortran" : "Fortran", "freebasic" : "FreeBasic", "freeswitch" : "FreeSWITCH", "gambas" : "GAMBAS", "gml" : "Game Maker", "gdb" : "GDB", "genero" : "Genero", "genie" : "Genie", "gettext" : "GetText", "go" : "Go", "groovy" : "Groovy", "gwbasic" : "GwBasic", "haskell" : "Haskell", "haxe" : "Haxe", "hicest" : "HicEst", "hq9plus" : "HQ9 Plus", "html4strict" : "HTML", "html5" : "HTML 5", "icon" : "Icon", "idl" : "IDL", "ini" : "INI file", "inno" : "Inno Script", "intercal" : "INTERCAL", "io" : "IO", "ispfpanel" : "ISPF Panel Definition", "j" : "J", "java" : "Java", "java5" : "Java 5", "javascript" : "JavaScript", "jcl" : "JCL", "jquery" : "jQuery", "json" : "JSON", "julia" : "Julia", "kixtart" : "KiXtart", "kotlin" : "Kotlin", "latex" : "Latex", "ldif" : "LDIF", "lb" : "Liberty BASIC", "lsl2" : "Linden Scripting", "lisp" : "Lisp", "llvm" : "LLVM", "locobasic" : "Loco Basic", "logtalk" : "Logtalk", "lolcode" : "LOL Code", "lotusformulas" : "Lotus Formulas", "lotusscript" : "Lotus Script", "lscript" : "LScript", "lua" : "Lua", "m68k" : "M68000 Assembler", "magiksf" : "MagikSF", "make" : "Make", "mapbasic" : "MapBasic", "markdown" : "Markdown", "matlab" : "MatLab", "mirc" : "mIRC", "mmix" : "MIX Assembler", "modula2" : "Modula 2", "modula3" : "Modula 3", "68000devpac" : "Motorola 68000 HiSof...", "mpasm" : "MPASM", "mxml" : "MXML", "mysql" : "MySQL", "nagios" : "Nagios", "netrexx" : "NetRexx", "newlisp" : "newLISP", "nginx" : "Nginx", "nim" : "Nim", "text" : "None", "nsis" : "NullSoft Installer", "oberon2" : "Oberon 2", "objeck" : "Objeck Programming L...", "objc" : "Objective C", "ocaml-brief" : "OCalm Brief", "ocaml" : "OCaml", "octave" : "Octave", "oorexx" : "Open Object Rexx", "pf" : "OpenBSD PACKET FILTER", "glsl" : "OpenGL Shading", "oobas" : "Openoffice BASIC", "oracle11" : "Oracle 11", "oracle8" : "Oracle 8", "oz" : "Oz", "parasail" : "ParaSail", "parigp" : "PARI/GP", "pascal" : "Pascal", "pawn" : "Pawn", "pcre" : "PCRE", "per" : "Per", "perl" : "Perl", "perl6" : "Perl 6", "php" : "PHP", "php-brief" : "PHP Brief", "pic16" : "Pic 16", "pike" : "Pike", "pixelbender" : "Pixel Bender", "pli" : "PL/I", "plsql" : "PL/SQL", "postgresql" : "PostgreSQL", "postscript" : "PostScript", "povray" : "POV-Ray", "powerbuilder" : "PowerBuilder", "powershell" : "PowerShell", "proftpd" : "ProFTPd", "progress" : "Progress", "prolog" : "Prolog", "properties" : "Properties", "providex" : "ProvideX", "puppet" : "Puppet", "purebasic" : "PureBasic", "pycon" : "PyCon", "python" : "Python", "pys60" : "Python for S60", "q" : "q/kdb+", "qbasic" : "QBasic", "qml" : "QML", "rsplus" : "R", "racket" : "Racket", "rails" : "Rails", "rbs" : "RBScript", "rebol" : "REBOL", "reg" : "REG", "rexx" : "Rexx", "robots" : "Robots", "rpmspec" : "RPM Spec", "ruby" : "Ruby", "gnuplot" : "Ruby Gnuplot", "rust" : "Rust", "sas" : "SAS", "scala" : "Scala", "scheme" : "Scheme", "scilab" : "Scilab", "scl" : "SCL", "sdlbasic" : "SdlBasic", "smalltalk" : "Smalltalk", "smarty" : "Smarty", "spark" : "SPARK", "sparql" : "SPARQL", "sqf" : "SQF", "sql" : "SQL", "standardml" : "StandardML", "stonescript" : "StoneScript", "sclang" : "SuperCollider", "swift" : "Swift", "systemverilog" : "SystemVerilog", "tsql" : "T-SQL", "tcl" : "TCL", "teraterm" : "Tera Term", "thinbasic" : "thinBasic", "typoscript" : "TypoScript", "unicon" : "Unicon", "uscript" : "UnrealScript", "upc" : "UPC", "urbi" : "Urbi", "vala" : "Vala", "vbnet" : "VB.NET", "vbscript" : "VBScript", "vedit" : "Vedit", "verilog" : "VeriLog", "vhdl" : "VHDL", "vim" : "VIM", "visualprolog" : "Visual Pro Log", "vb" : "VisualBasic", "visualfoxpro" : "VisualFoxPro", "whitespace" : "WhiteSpace", "whois" : "WHOIS", "winbatch" : "Winbatch", "xbasic" : "XBasic", "xml" : "XML", "xorg_conf" : "Xorg Config", "xpp" : "XPP", "yaml" : "YAML", "z80" : "Z80 Assembler", "zxbasic" : "ZXBasic"}
    user = ctx.message.author.name
    embed=discord.Embed(title="**PASTEBIN POSTER**", description="*Pastes your code on pastebin*", color=0xc016d3)
    embed.set_author(name="EC BOT",url=invite, icon_url = img)
    # msg = ' '.join(msg)
    if not lang in langs.keys():
        lang = 'text'

    codeurl = ot.pastebinpost(user,lang,msg)
    embed.add_field(name="*Code successfully pasted*", value=codeurl)
    embed.set_footer(text=foot)
    await bot.say(embed=embed)



token = str(os.environ.get('TOKEN', 3))
bot.loop.create_task(check())
bot.loop.create_task(status())
# bot.loop.create_task(send_insults())
bot.run('NDc3NTEyNTU2NjMwNTA3NTMw.Dmb_Og.QS_ydbWquXQWPbUEXJd7owhxPKY')
