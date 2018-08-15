import discord
from discord.ext import commands
import asyncio
import codechefcrawlerv2 as cc
import sqlitedb as sql
import datetime
from itertools import cycle
import os

invite = 'https://discordapp.com/oauth2/authorize?&client_id=477512556630507530&scope=bot&permissions=0'

bot = commands.Bot(command_prefix="!")
global verify
verify = {} # {codechef name : [Time , discord id , discord name , ctx.channel.id]} ##ctx.channel.id to Send message in the same channel if the user is verified (or not)
stats = ['A bot made by EmberCult','Current version v2','Say !commands','A bot made by Viplav','Online and ready to use!','Found any error,DM EmberCult!']

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
                embed.set_footer(text='Type !commands for a list of commands!')
                embed.set_author(name='EC BOT', url=invite)
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
                    embed.set_footer(text='Type !commands for a list of commands!')
                    embed.set_author(name='EC BOT',url=invite)
                    await bot.send_message(bot.get_channel(verify[user][3]), embed=embed)
                    del verify[user]
        await asyncio.sleep(60)


@bot.event
async def on_ready():
    print("Lol it actually started!")



@bot.command(pass_context=True)
async def ping(ctx):
    userid = ctx.message.author.id
    tnow = datetime.datetime.utcnow()
    lags = tnow-ctx.message.timestamp
    lags = str(lags).split(':')[2]

    embed = discord.Embed(title='PONG :ping_pong:', description='<@{}>  , took {} secs!'.format(userid, lags), color=discord.Color.blue())
    embed.set_footer(text='Type !commands for a list of commands!')
    embed.set_author(name='EC BOT', url=invite)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def cookie(ctx, user = None):
    embed = discord.Embed(title="COOKIE DELIVERY!", description= ':cookie:' , color=discord.Color.gold())
    if user == None:
        user = ctx.message.author.id
        embed.add_field(name='FROM', value='The almighty EC himself')
        embed.add_field(name='TO', value='<@{}>'.format(user))
    else:
        giver = ctx.message.author.id
        embed.add_field(name='FROM', value='<@{}>'.format(giver))
        embed.add_field(name='TO', value='{}'.format(user))
    embed.set_footer(text='Type !commands for a list of commands!')
    embed.set_author(name='EC BOT', url=invite)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def rating(ctx, user = None):
    if user == None:
        embed = discord.Embed(title='RATING', description='Rating from Code Chef', color=discord.Color.red())
        embed.add_field(name='ERROR', value='Please provide a code chef username!   ')
    else:
        rating = cc.user_rating(user)
        if rating:
            rcolor = '0x00' + star2color(rating2star(rating))
            embed = discord.Embed(title='RATING', description='Rating from Code Chef', color=int(rcolor,16))
            embed.add_field(name='USER', value='{}'.format(user), inline=True)
            embed.add_field(name='RATING', value='{}'.format(rating), inline=True)
            embed.add_field(name='STARS', value='{}'.format(rating2star(rating)), inline=True)
        else:
            embed = discord.Embed(title='RATING', description='Rating from Code Chef', color=discord.Color.red())
            embed.add_field(name='ERROR', value='No such user found!')

    embed.set_footer(text='Type !commands for a list of commands!')
    embed.set_author(name='EC BOT',
                     url=invite)
    await bot.say(embed = embed)


@bot.command(pass_context=True)
async def link(ctx, user=None):
    sender = ctx.message.author.name
    sender_id = ctx.message.author.id
    time = ctx.message.timestamp
    if user == None:
        embed = discord.Embed(title='**LINK**', description='*Links your codechef and discord ids*', color=discord.Color.red())
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

    embed.set_footer(text='Type !commands for a list of commands!')
    embed.set_author(name='EC BOT',
                     url=invite)

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

        embed.set_footer(text='Type !commands for a list of commands!')
        embed.set_author(name='EC BOT',
                         url=invite)
        await bot.say(embed=embed)


@bot.command(pass_context=True)
async def commands(ctx):
    embed=discord.Embed(title="**COMMANDS**", description="*A list of commands the bot currently supports*", color=0xc016d3)
    embed.set_author(name="EC BOT",url=invite)
    embed.add_field(name='!ping', value='Replies with pong if its working', inline=False)
    embed.add_field(name='!cookie [user]', value='Sends a cookie to [user]', inline=False)
    embed.add_field(name='!link [codechef username]', value='Will link the given code chef username to your discord id', inline=False)
    embed.add_field(name='!drating [user]', value='Gives you the rating of [user] is he/she has linked their codechef to discord', inline=True)
    embed.add_field(name='!rating [codechef username]', value='Gives you the rating of  [codechef username] directly from the website', inline=True)
    embed.set_footer(text="Type !commands for a list of commands!")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def todo(ctx,*message):
    uid = ctx.message.author.id
    embed = discord.Embed(title="**To Do List**", description="*A list of you need to do!*",
                          color=0xc016d3)
    embed.set_author(name="EC BOT", url=invite)
    if len(message) == 0:
        tasks = sql.gettodo(uid)
        if len(tasks) == 0:
            embed.add_field(name='Empty list!',value='Add some items to your todo list now!')
        for i in range(len(tasks)):
            embed.add_field(name='Task#{}'.format(i+1), value='{}'.format(tasks[i]))
    else:
        sql.addtodo(uid,message)
        embed.add_field(name='Task added', value='{}'.format(' '.join(message)))
    embed.set_footer(text="Type !commands for a list of commands!")
    await bot.say(embed=embed)


token = str(os.environ.get('TOKEN', 3))
bot.loop.create_task(check())
bot.loop.create_task(status())
bot.run(token)
