import os, discord, random

from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN'] 
GUILD = os.environ['DISCORD_GUILD']
WCI = os.environ['WELCOME_CHANNEL_ID']
RCI = os.environ['RULES_CHANNEL_ID']
GCI = os.environ['GENERAL_CHANNEL_ID']

was_kick_ban = False

bot = commands.Bot(command_prefix='0')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(WCI))
    welcomeMessage = f'Welcome to Universe 0, {member.mention},\nBe sure read the {bot.get_channel(int(RCI)).mention} and enjoy your stay.'
    await channel.send(welcomeMessage)
    print(f'Public Welcome message sent for {member}....')

@bot.event
async def on_member_remove(member):
    global was_kick_ban
    if not was_kick_ban:
        channel = bot.get_channel(int(GCI))
        leaveMessage = f'{member.mention} has Left the Server.\nIt was good having you here'
        await channel.send(leaveMessage)
        print(f'Leave message sent for {member}.....')
    else:
        was_kick_ban = False

@bot.command(name = 'introduce', help = 'Responds with Intoduction') 
async def introduce(ctx):
    response = "Hey I am TahasX! I was created by Sauood. Written in Python"
    await ctx.send(response)
    print("Response sent....")

@bot.command(name = 'ping', help = 'gives the latency of TahasX')
async def ping(ctx):
    await ctx.send(f'Pong {round(bot.latency * 1000)}ms')
    
@bot.command(name = 'rd', help = 'simulates rolling of Dice')
async def roll(ctx):
    dice = str(random.choice(range(1, 7)))
    await ctx.send(', '.join(dice))
    print('Dice rolled....')
 
@bot.command(name = 'clear', help = 'Clears a certian amount')
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount + 1)
    ctx.channel.send(f'Cleared {amount} messages!')
    print(f'{amount} messages Cleared')

@bot.command(name = 'kick', help = 'kicks the user')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason = 'unspecified'):  
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot kick yourself!")
        return
    global was_kick_ban
    was_kick_ban = True
    await member.kick(reason=reason)
    channel = bot.get_channel(int(GCI))
    kickMessage = f'{member.mention} has been kicked from the Server. Reason: {reason}'
    await channel.send(kickMessage)
    print(f'Kick message sent for {member}....')
    

@bot.command(name = 'ban' , help = 'bans a user')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason = 'unspecified'):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return  
    global was_kick_ban
    was_kick_ban = True
    await member.ban(reason=reason)
    channel = bot.get_channel(int(GCI))
    banMessage = f'{member.mention} has been banned from the Server. Reason: {reason}'
    await channel.send(banMessage)
    print(f'Ban message sent for {member}......')

@bot.command(name = 'unban', help = 'unbans a banned user')
@commands.has_permissions(ban_members=True)
async def unban(ctx, user, reason = 'unspecified'):
    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
        print(f'user found as {user}...')
    except:
        await ctx.send("Error: user could not be found in ban list!")
        return

    if user == None or user == ctx.message.author:
        await ctx.channel.send("You cannot unban yourself")
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
        else:
            await ctx.send("User not banned!")
            return
    except:
        await ctx.send("Unbanning failed!")
        return

    await ctx.guild.unban(user)
    channel = bot.get_channel(int(GCI))
    unbanMessage = f'{user} has been unbanned. Reason: {reason}'
    await channel.send(unbanMessage)
    print(f'UnBan message sent for {user}......')

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)
