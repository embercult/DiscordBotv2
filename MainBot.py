import discord
from discord.ext import commands
import codechefcrawler as cc
import sqlitedb as sql
import time
from threading import Timer
import os
sql.createtable()
bot = commands.Bot(command_prefix="!")

pending = {}


def hello():
    if len(pending):
        print('These people need to be verified!', pending)
        for i in list(pending.keys()):
            z = cc.usercheck(i)
            if z:
                sql.adduser(pending[i][0], pending[i][2], i, cc.userrating(i))
                print("added shit to sql, name = {} , ccname = {} and the rating".format(pending[i][0], i))
                verified(pending[i][0], i, cc.userrating(i), pending[i][3])
                del pending[i]
            else:
                x = time.time() - pending[i][1]
                if x > 1:
                    print("removed the", pending[i], "as 60secs have passed!")
                    print(pending[i][3])
                    notverified(pending[i][0], i, pending[i][3])

                    del pending[i]
    else:
        print("No pending user!")


    t = Timer(10, hello)
    t.start()


t = Timer(10, hello)
t.start()


async def notverified(usern, id, cc):
    print("Telling users it failed to verify their account!")
    print(cc)
    await bot.send_message(cc, "<@{}> Failed to verify {} ,Account is **not** linked to you!".format(id, usern))


def verified(usern, id, rating, ctx):
    star = 0
    x = ctx.message.channel
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
    bot.send_message(x,"<@{}> you have been linked to {}, you're a {} Star coder!".format(id,usern,star))

    print("told user their account is verified!")

@bot.event
async def on_ready():
    print("Lol it actually started!")

# @bot.event
# async def on_command_error(ctx, error):
#     print('well someone error occured and i dont wanna know what')

@bot.command(pass_context=True)
async def cookie(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author

    await bot.say("<@{}> heres a cookie for you :cookie:".format(member.id))


@bot.command(pass_context=True)
async def ping(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id
    await bot.say("<@{}> Pong! :ping_pong:".format(member))


@bot.command(pass_context=True)
async def rating(ctx, usern):
    member = ctx.message.author.id
    try:
        x = sql.searchuser(usern)
        print(xw)
        if x:
            rating = x[0]
            if rating:
                await bot.say("<@{}>, {}'s rating is {}!".format(member, x[1], rating))
    except (IndexError, TypeError) as e:
        await bot.say("""<@{}>, The user <@{}> has not linked their code chef profile with discord!
Try searching with code chef handle using the command `!ccrating [name]`""".format(member, usern.id))


@bot.command(pass_context=True)
async def ccrating(ctx, usern):
    if usern.startswith("<@"):
        return
    member = ctx.message.author.id
    usern = usern.lower()

    rating = cc.userrating(usern)
    if rating != False:
        await bot.say("<@{}>, {}'s rating is {}!".format(member, usern, rating))
    else:
        await bot.say(
            "<@{}>, No user called {} found, Please check the spelling!".format(member, usern))

@bot.command(pass_context=True)
async def verify(ctx, usern: str):
    usern = usern.lower()
    member = ctx.message.author.id
    memname = ctx.message.author.name
    x = sql.searchuser(usern)
    try:
        x = x[0][0]
        await bot.say("<@{}>, {} is already linked with <@{}>! Please check the spelling!".format(member, usern, x))

    except (IndexError, TypeError) as e:
        await bot.say("""<@{}>```python
You have 1 min to submit a solution to this problem to link {} to your discord id!
(Wrong answers will work too)```https://www.codechef.com/problems/HS08TEST
                """.format(member, usern))
        pending[usern] = [member, time.time(), memname, ctx.message.channel.id]


@bot.command(pass_context=True)
async def printdb(ctx):
    member = ctx.message.author.id
    if member == '139955846900613120':
        await bot.say(sql.printdb())



@bot.command(pass_context=True)
async def commands(ctx):
    await bot.say("""This bot was made by `Embercult`!
Current commands:
    
    
    `!ping` - Bot will reply with pong if its wokring!
    
    
    `!cookie (user)` - Bot will reply with cookie mentioning the (user) if no user was mentioned it will mention the sender!
    
    
    `!ccrating (code_chef_username)` - Bot will do some magic and will give you code chef rating of the given username
    
    
    `!verify (code_chef_username)` - Bot will again do some magic and will link the given username to your discord account if you pass its test!
    
    
    `!rating (user)` - Bot will do magic and tell you the rating of the mentioned user if he has linked his code chef to discord""")


token = str(os.environ.get('TOKEN', 3))
bot.run(token)
