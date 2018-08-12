import discord
from discord.ext import commands
import codechefcrawler as cc
import sqlitedb as sql


bot = commands.Bot(command_prefix="!")


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




bot.run("NOP NOP NOP U CANT SEE THIS")
