import discord
from discord.ext import commands
import codechefcrawler as cc
import sqlitedb as sql
import time
from threading import Timer
import os

bot = commands.Bot(command_prefix="!")

pending = {}






def hello():

    if len(pending):

        for i in list(pending.keys()):
            z = cc.usercheck(i)
            if z:
                sql.adduser(pending[i][0], i, cc.userrating(i))
                print("added shit to sql, name = {} , ccname = {} and the rating".format(pending[i][0], i))
                verified(pending[i][0], i, cc.userrating(i))
                del pending[i]
            else:
                x = time.time() - pending[i][1]
                if x > 60:
                    notverified(pending[i][0], i)
                    del pending[i]

    t = Timer(60, hello)
    t.start()


t = Timer(60, hello)
t.start()


def notverified(usern, id):
    bot.say("<@{}> Failed to verify {} ,Account is **not** linked to you!".format(id, usern))


def verified(usern, id, rating):
    star = 0
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
    bot.say("<@{}> you have been linked to {}, you're a {} Star coder!".format(id,usern,star))

@bot.event
async def on_ready():
    print("Lol it actually started!")

@bot.event
async def on_command_error(ctx, error):
    print('well someone error occured and i dont wanna know what')

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
async def rating(ctx, usern: discord.User):
    member = ctx.message.author.id
    try:
        x = sql.searchid(usern.id)

        rating = x
    except IndexError:
        rating = False
    if rating != False:
        await bot.say("<@{}>, <@{}>'s rating is {}!".format(member, usern.id, rating))
    else:
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
    x = sql.searchuser(usern)
    try:
        x = x[0][0]
        await bot.say("<@{}>, {} is already linked with <@{}>! Please check the spelling!".format(member, usern, x))

    except IndexError:
        await bot.say("""<@{}>```python
You have 1 min to submit a solution to this problem to link {} to your discord id!
(Wrong answers will work too)```https://www.codechef.com/problems/HS08TEST
                """.format(member, usern))
        pending[usern] = [member, time.time()]


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
