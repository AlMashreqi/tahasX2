import os, discord, random

from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']
WCI = os.environ['WELCOME_CHANNEL_ID']
RCI = os.environ['RULES_CHANNEL_ID']
GCI = os.environ['GENERAL_CHANNEL_ID']

bot = commands.Bot(command_prefix='0')

bot.was_kick_ban = False
bot.color_code = 0x3333A2
bot.del_message = str()
bot.org_message = str()
bot.ed_message = str()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('11 Commands!'))

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send("Woah! Command not Found!")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(WCI))
    welcomeMessage = f'Welcome to Universe 0, {member.mention},\nBe sure read the {bot.get_channel(int(RCI)).mention} and enjoy your stay.'
    await channel.send(welcomeMessage)
    print(f'Public Welcome message sent for {member}....')

@bot.event
async def on_member_remove(member):
    if not bot.was_kick_ban:
        channel = bot.get_channel(int(GCI))
        leaveMessage = f'{member.mention} has Left the Server.\nIt was good having you here'
        await channel.send(leaveMessage)
        print(f'Leave message sent for {member}.....')
    else:
        bot.was_kick_ban = False

@bot.event
async def on_message_delete(message):
    bot.del_message = message

@bot.event
async def on_message_edit(before, after):
    bot.org_message = before
    bot.ed_message = after

@bot.command(name = 'introduce', help = 'Responds with Intoduction')
async def introduce(ctx):
    response = "Hey I am TahasX! I was created by Sauood. Written in Python"
    await ctx.send(response)
    print("Response sent....")

@bot.command(name = 'ping', help = 'gives the latency of TahasX')
async def ping(ctx):
    embed = discord.Embed(description = f'Pong {round(bot.latency * 1000)}ms', color = bot.color_code)
    await ctx.send(embed = embed)

@bot.command(name = 'avatar', help = 'shows the avatar of a User')
async def avatar(ctx, member: discord.Member):
    avatar_embed = discord.Embed(color = bot.color_code)
    avatar_embed.set_image(url = '{}'.format(member.avatar_url))
    await ctx.send(embed = avatar_embed)

@bot.command(name = 'rd', help = 'simulates rolling of Dice')
async def roll(ctx):
    dice = str(random.choice(range(1, 7)))
    await ctx.send(', '.join(dice))
    print('Dice rolled....')

@bot.command(name = 'delsnipe', help = 'Shows last Deleted Message')
async def delsnipe(ctx):
    message = bot.del_message
    embed = discord.Embed(title = '**Last Deleted Message**', description = f'Deleted Message: _{message.content}_\nAuthor: _{message.author}_', color = bot.color_code)
    await ctx.send(embed = embed)

@bot.command(name = 'editsnipe', help = 'Shows last Edited Message')
async def editsnipe(ctx):
    message = bot.org_message
    message2 = bot.ed_message
    embed = discord.Embed(title = '**Last Edited Message**', description = f'Orignal Message: _{message.content}_\nEdited Message: _{message2.content}_\nAuthor: _{message.author}_', color = bot.color_code)
    await ctx.send(embed = embed)

@bot.command(name = 'warn', help = 'Warns the Specified User')
@commands.has_permissions(kick_members = True)
async def warn(ctx, member: discord.Member, *, reason = 'Unspecified'):
    embed = discord.Embed(description = f'{member} has been Warned\n**Reason:** {reason}', color = bot.color_code)
    await ctx.send(embed = embed)

@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify a User to Warn")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps! You don't have Permissions to That!")

@bot.command(name = 'clear', help = 'Clears a certian amount')
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount + 1)
    await ctx.channel.send(f'Cleared {amount} messages!')
    print(f'{amount} messages Cleared')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps! You don't have Permissions to That!")

@bot.command(name = 'kick', help = 'kicks the user')
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = 'Unspecified'):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot kick yourself!")
        return
    bot.was_kick_ban = True
    await member.kick(reason=reason)
    channel = bot.get_channel(int(GCI))
    embed = discord.Embed(description = f'{member.mention} has been kicked from the Server\n**Reason:** {reason}', color = bot.color_code)
    await ctx.send(embed = embed)
    print(f'Kick message sent for {member}....')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify a User to kick")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps! You don't have Permissions to That!")

@bot.command(name = 'ban' , help = 'bans a user')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason = 'Unspecified'):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return
    bot.was_kick_ban = True
    await member.ban(reason=reason)
    channel = bot.get_channel(int(GCI))
    embed = discord.Embed(description = f'{member.mention} has been banned from the Server\n**Reason:** {reason}', color = bot.color_code)
    await ctx.send(embed = embed)
    print(f'Ban message sent for {member}......')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify a User to Ban")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps! You don't have Permissions to That!")

@bot.command(name = 'unban', help = 'unbans a banned user')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(description = f'{member.mention} has been Unbanned', color = bot.color_code)
            await ctx.send(embed = embed)
            print(f'Unbanned {user.mention}....')
            return
    ctx.send(f'User was not found!')
    print('User was not Found....')

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify a User to Unban!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps! You don't have Permissions to That!")

# @bot.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise

bot.run(TOKEN)
