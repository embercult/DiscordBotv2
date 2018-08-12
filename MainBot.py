import discord
from discord.ext import commands
import codechefcrawler as cc
import sqlitedb as sql
import time
from threading import Timer


bot = commands.Bot(command_prefix="!")

pending = {}


def hello():
    print(pending)

    {k: v for k, v in pending.items() if v is not None}
    if len(pending):

        for i in list(pending.keys()):
            print("in the loop" , i)
            z = cc.usercheck(i)
            print("did it find user?", z)
            if z:
                sql.adduser(pending[i][0], i, cc.userrating(i))
                print("added shit to sql")
                verified(pending[i][0], i, cc.userrating(i))
                del pending[i]
            else:
                x = time.time() - pending[i][1]
                if x > 60:
                    notverified(pending[i][0], i)
                    del pending[i]

    t = Timer(30, hello)
    t.start()


t = Timer(30, hello)
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


@bot.command(pass_context=True)
async def cookie(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id

    await bot.say("<@{}> heres a cookie for you :cookie:".format(member))


@bot.command(pass_context=True)
async def ping(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author.id
    await bot.say("<@{}> Pong! :ping_pong:".format(member))


@bot.command(pass_context=True)
async def rating(ctx, usern: str):
    usern = usern.lower()
    member = ctx.message.author.id
    rating = cc.userrating(usern)
    if rating:
        await bot.say("<@{}>, {}'s rating is {}!".format(member, usern, rating))
    else:
        await bot.say("<@{}>, No user called {} found! Please check the spelling!".format(member, usern))

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


bot.run("NOT FOR YOU")
