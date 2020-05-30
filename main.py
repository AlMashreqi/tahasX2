import os, discord, random

from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']
WCI = os.environ['WELCOME_CHANNEL_ID']
RCI = os.environ['RULES_CHANNEL_ID']
GCI = os.environ['GENERAL_CHANNEL_ID']

bot = commands.Bot(command_prefix='0')
bot.remove_command('help')

bot.was_kick_ban = False
bot.color_code = 0x3333A2
bot.del_message = str()
bot.org_message = str()
bot.ed_message = str()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('11 Commands!'))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Woah! Command not Found!")
    elif (error, Exception):
        await ctx.send(error)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(WCI))
    guild = bot.get_guild(int(GUILD))
    embed = discord.Embed(title = f'**Welcome {member.name}**', description = f'{member.mention}, Be sure read the {bot.get_channel(int(RCI)).mention} and enjoy your stay.\n\n**• Username: ** {member}\n**• ID:** {member.id}\n**• Server Members: ** {len(guild.members)}', color = bot.color_code)
    embed.set_thumbnail(url = f'{member.avatar_url}')
    embed.set_footer(text = f'© TahasX | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
    await channel.send(embed = embed)
    print(f'Public Welcome message sent for {member}....')

@bot.event
async def on_member_remove(member):
    if not bot.was_kick_ban:
        channel = bot.get_channel(int(GCI))
        guild = bot.get_guild(int(GUILD))
        embed = discord.Embed(title = f'**Thanks for being Here**', description = f'{member.mention} has Left the Server.\nIt was good having you here.\n\n**• Username: ** {member}\n**• ID:** {member.id}\n**• Server Members: ** {len(guild.members)}', color = bot.color_code)
        embed.set_thumbnail(url = f'{member.avatar_url}')
        embed.set_footer(text = f'© TahasX | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
        await channel.send(embed = embed)
        print(f'Leave message sent for {member}.....')
    else:
        bot.was_kick_ban = False

@bot.command(name = 'help', help = 'Shows the help command')
async def help(ctx, *, category = 'display'):
    guild = bot.get_guild(int(GUILD))

    uti_embed = discord.Embed(title = 'Command Help', description = '**Utilities & Fun**', color = bot.color_code)
    uti_embed.add_field(name = 'avatar', value = 'Displays the Avatar of a User\nUsage: `0avatar <user>`', inline = False)
    uti_embed.add_field(name = 'help', value = 'Shows this Menu\nUsage: `0help`', inline = False)
    uti_embed.add_field(name = 'introduce', value = 'Displays the Introduction of the Bot\nUsage: `0introduce`', inline = False)
    uti_embed.add_field(name = 'ping', value = 'Displays the Latency of the Bot\nUsage: `0ping`', inline = False)
    uti_embed.add_field(name = 'rd', value = 'Simulates rolling of Dice\nUsage: `0rd`', inline = False)
    uti_embed.set_footer(text = f'© TahasX | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
    
    mod_embed = discord.Embed(title = 'Command Help', description = '**Moderation**', color = bot.color_code)
    mod_embed.add_field(name = 'ban', value = 'Bans a User from the Server\nUsage: `0ban <user> [reason]`', inline = False)
    mod_embed.add_field(name = 'clear', value = 'Clears last 5 Messages on Default\nUsage: `0clear <number-of-messages>`', inline = False)
    mod_embed.add_field(name = 'delsnipe', value = 'Displays the Last Deleted Message\nUsage: `0delsnipe`', inline = False)
    mod_embed.add_field(name = 'editsnipe', value = 'Displays the Last Edited Message with Orignal Content\nUsage: `0editsnipe`', inline = False)
    mod_embed.add_field(name = 'kick', value = 'Kicks out a user from the Server\nUsage: `0kick <user> [reason]`', inline = False)
    mod_embed.add_field(name = 'unban', value = 'Unbans a Banned User\nUsage: `0unban <user>`', inline = False)
    mod_embed.add_field(name = 'warn', value = 'Warns a User\nUsage: `0warn <user> [reason]`', inline = False)
    mod_embed.set_footer(text = f'© TahasX | Owned by {guild.owner}', icon_url = bot.user.avatar_url)

    help_embed = discord.Embed(title = 'Command Help', description = '**Categories**\n', color = bot.color_code)
    help_embed.add_field(name = '**Moderation**', value = '`0help Mod`')
    help_embed.add_field(name = '**Utilities & Fun**', value = '`0help Utils`')
    help_embed.set_footer(text = f'© TahasX | Owned by {guild.owner}', icon_url = bot.user.avatar_url)

    if category == 'Mod':
        await ctx.send(embed = mod_embed)
    elif category == 'Utils':
        await ctx.send(embed = uti_embed)
    elif category == 'display':
        await ctx.send(embed = help_embed)
    else:
        await ctx.send('Category Not Found!')

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
    avatar_embed.set_image(url = f'{member.avatar_url}')
    await ctx.send(embed = avatar_embed)

@bot.command(name = 'rd', help = 'simulates rolling of Dice')
async def roll(ctx):
    dice = str(random.choice(range(1, 7)))
    await ctx.send(', '.join(dice))
    print('Dice rolled....')

@bot.command(name = 'delsnipe', help = 'Shows last Deleted Message')
@commands.has_permissions(manage_messages = True)
async def delsnipe(ctx):
    message = bot.del_message
    embed = discord.Embed(title = '**Last Deleted Message**', description = f'Deleted Message:\n```{message.content}```', color = bot.color_code)
    embed.set_footer(text = f'Author: {message.author}', icon_url = message.author.avatar_url)
    await ctx.send(embed = embed)

@delsnipe.error
async def delsnipe_error(ctx, error):
    if isinstance(error, Exception):
        await ctx.send('Nothing to Snipe')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps You don't have Permissions to That!")

@bot.command(name = 'editsnipe', help = 'Shows last Edited Message')
@commands.has_permissions(manage_messages = True)
async def editsnipe(ctx):
    message = bot.org_message
    message2 = bot.ed_message
    embed = discord.Embed(title = '**Last Edited Message**', description = f'Orignal Message:\n```{message.content}```\nEdited Message:\n```{message2.content}```\n', color = bot.color_code)
    embed.set_footer(text = f'Author: {message.author}', icon_url = message.author.avatar_url)
    await ctx.send(embed = embed)

@editsnipe.error
async def editsnipe_error(ctx, error):
    if isinstance(error, Exception):
        await ctx.send('Nothing to Snipe')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps! You don't have Permissions to That!")

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
            embed = discord.Embed(description = f'{member_name}#{member_discriminator} has been Unbanned', color = bot.color_code)
            await ctx.guild.unban(user)
            await ctx.send(embed = embed)
            print(f'Unbanned {user.mention}....')
            return
    await ctx.send(f'User was not found!')
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
