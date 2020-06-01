import os, random
import corona_api, discord

from discord.ext import commands

TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']
WCI = os.environ['WELCOME_CHANNEL_ID']
RCI = os.environ['RULES_CHANNEL_ID']
GCI = os.environ['GENERAL_CHANNEL_ID']
PREFIX = os.environ['COMMAND_PREFIX']

bot = commands.Bot(command_prefix = str(PREFIX))
bot.remove_command('help')

corona = corona_api.Client()

bot.color_code = 0x3333A2
bot.del_message = str()
bot.org_message = str()
bot.ed_message = str()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status = discord.Status.online, activity = discord.Game('15 Commands!'))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Woah! Command not Found!")
    else:
        await ctx.send(f'`{error}`')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(WCI))
    guild = bot.get_guild(int(GUILD))
    embed = discord.Embed(title = f'**Welcome {member.name}**', description = f'{member.mention}, Be sure read the {bot.get_channel(int(RCI)).mention} and enjoy your stay.\n\n**• Username: ** {member}\n**• ID:** {member.id}\n**• Server Members: ** {len(guild.members)}', color = bot.color_code)
    embed.set_thumbnail(url = f'{member.avatar_url}')
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
    await channel.send(embed = embed)
    print(f'Public Welcome message sent for {member}....')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(GCI))
    guild = bot.get_guild(int(GUILD))
    embed = discord.Embed(title = f'**Thanks for being Here**', description = f'{member.mention} has Left the Server.\nIt was good having you here.\n\n**• Username: ** {member}\n**• ID:** {member.id}\n**• Server Members: ** {len(guild.members)}', color = bot.color_code)
    embed.set_thumbnail(url = f'{member.avatar_url}')
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
    await channel.send(embed = embed)
    print(f'Leave message sent for {member}.....')
    
@bot.event
async def on_message_delete(message):
    bot.del_message = message

@bot.event
async def on_message_edit(before, after):
    if before.content != after.content:
        bot.org_message = before
        bot.ed_message = after

@bot.command(name = 'help', help = 'Shows the help command')
async def help(ctx, *, category = 'display'):
    guild = bot.get_guild(int(GUILD))
    prefix = str(PREFIX)

    uti_embed = discord.Embed(title = 'Help Command', description = '**Utilities & Fun**', color = bot.color_code)
    uti_embed.add_field(name = 'avatar', value = f'Displays the Avatar of a User\nUsage: `{prefix}avatar <user>`', inline = False)
    uti_embed.add_field(name = 'help', value = f'Shows this Menu\nUsage: `{prefix}help`', inline = False)
    uti_embed.add_field(name = 'introduce', value = f'Displays the Introduction of the Bot\nUsage: `{prefix}introduce`', inline = False)
    uti_embed.add_field(name = 'ping', value = f'Displays the Latency of the Bot\nUsage: `{prefix}ping`', inline = False)
    uti_embed.add_field(name = 'rd', value = f'Simulates rolling of Dice\nUsage: `{prefix}rd`', inline = False)
    uti_embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
    
    mod_embed = discord.Embed(title = 'Command Help', description = '**Moderation**', color = bot.color_code)
    mod_embed.add_field(name = 'ban', value = f'Bans a User from the Server\nUsage: `{prefix}ban <user> [reason]`', inline = False)
    mod_embed.add_field(name = 'clear', value = f'Clears last 5 Messages on Default\nUsage: `{prefix}clear <number-of-messages>`', inline = False)
    mod_embed.add_field(name = 'delsnipe', value = f'Displays the Last Deleted Message\nUsage: `{prefix}delsnipe`', inline = False)
    mod_embed.add_field(name = 'editsnipe', value = f'Displays the Last Edited Message with Orignal Content\nUsage: `{prefix}editsnipe`', inline = False)
    mod_embed.add_field(name = 'kick', value = f'Kicks out a user from the Server\nUsage: `{prefix}kick <user> [reason]`', inline = False)
    mod_embed.add_field(name = 'mute', value = f'Mutes the specified User\nUsage: `{prefix}mute <user> [reason]`', inline = False)
    mod_embed.add_field(name = 'unban', value = f'Unbans a Banned User\nUsage: `{prefix}unban <user>`', inline = False)
    mod_embed.add_field(name = 'unmute', value = f'Unmutes a muted user\nUsage: `{prefix}unmute <user>`', inline = False)
    mod_embed.add_field(name = 'warn', value = f'Warns a User\nUsage: `{prefix}warn <user> [reason]`', inline = False)
    mod_embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)

    help_embed = discord.Embed(title = 'Command Help', description = '**Categories**\n', color = bot.color_code)
    help_embed.add_field(name = '**Moderation**', value = f'`{prefix}help Mod`')
    help_embed.add_field(name = '**Utilities & Fun**', value = f'`{prefix}help Utils`')
    help_embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)

    if category == 'Mod':
        await ctx.send(embed = mod_embed)
    elif category == 'Utils':
        await ctx.send(embed = uti_embed)
    elif category == 'display':
        await ctx.send(embed = help_embed)
    else:
        await ctx.send('Category Not Found!')

@bot.command(name = 'introduce', help = 'Responds with Intoduction')
async def introduce(ctx):
    response = f"Hey I am {bot.user.name}! I was created by Sauood. Written in Python"
    await ctx.send(response)
    print("Response sent....")

@bot.command(name = 'ping', help = f'gives the latency of the Bot')
async def ping(ctx):
    guild = bot.get_guild(int(GUILD))
    embed = discord.Embed(description = f'Pong {round(bot.latency * 1000)}ms', color = bot.color_code)
    embed.set_footer(text=f'© {bot.user.name} | Owned by {guild.owner}', icon_url=bot.user.avatar_url)
    await ctx.send(embed = embed)

@bot.command(name = 'avatar', help = 'shows the avatar of a User')
async def avatar(ctx, member: discord.Member):
    guild = bot.get_guild(int(GUILD))
    embed = discord.Embed(color = bot.color_code)
    embed.set_image(url = f'{member.avatar_url}')
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
    await ctx.send(embed = embed)

@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        ctx.send('Please Specify a user!')

@bot.command(name = 'rd', help = 'simulates rolling of Dice')
async def roll(ctx):
    dice = str(random.choice(range(1, 7)))
    await ctx.send(', '.join(dice))
    print('Dice rolled....')

@bot.command(name = 'covid', help = 'Shows the current COVID stats')
async def covid(ctx):
    data = await client.all()  # get global data

    embed = discord.Embed(title = 'COVID-19 Stats', description = 'Worldwide Stats:', color = bot.color_code)
    embed.add_field(name = '**Global Cases**', value = f'{data.cases}', inline = False)
    embed.add_field(name = '**Global Deaths**', value=f'{data.deaths}', inline=False)
    embed.add_field(name = '**Global Recoveries**', value=f'{data.recoveries}', inline=False)
    embed.add_field(name = '**Cases Today**', value=f'{data.today_cases}', inline=False))
    embed.add_field(name='**Deaths Today**', value=f'{data.today_deaths}', inline=False)
    embed.set_footer(text=f'© {bot.user.name} | Owned by {guild.owner}', icon_url=bot.user.avatar_url)

    await ctx.send(embed = embed)
    await client.request_client.close()  # close the ClientSession

@bot.command(name = 'delsnipe', help = 'Shows last Deleted Message')
@commands.has_permissions(manage_messages = True)
async def delsnipe(ctx):
    guild = bot.get_guild(int(GUILD))
    message = bot.del_message
    embed = discord.Embed(title = 'Last Deleted Message', description = f'Deleted Message:\n```{message.content}```\nAuthor: {message.author}', color = bot.color_code)
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
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
    guild = bot.get_guild(int(GUILD))
    embed = discord.Embed(title = 'Last Edited Message', description = f'Orignal Message:\n```{bot.org_message.content}```\nEdited Message:\n```{bot.ed_message.content}```\nAuthor: {bot.org_message.author}', color = bot.color_code)
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
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
    guild = bot.get_guild(int(GUILD))
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot Warn yourself!")
        return
    embed = discord.Embed(title = 'User Warned',description = f'{member} has been Warned\n**Reason:** {reason}', color = bot.color_code)
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
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
    embed = discord.Embed(title='Messages Cleared', description = f'Cleared {amount} Messages', color = bot.color_code)
    embed.set_footer(text=f'© {bot.user.name} | Owned by {guild.owner}', icon_url=bot.user.avatar_url)
    print(f'{amount} messages Cleared')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps! You don't have Permissions to That!")

@bot.command(name = 'mute', help = 'Mutes a Member')
@commands.has_permissions(kick_members = True)
async def mute(ctx, member: discord.Member, *, reason = 'Unspecified'):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot Mute yourself!")
        return
    guild = bot.get_guild(int(GUILD))
    role = discord.utils.get(ctx.guild.roles, name='Prisoner')
    await member.add_roles(role)
    embed = discord.Embed(title = 'User Muted',description = f'{member.mention} has been Muted.\n**Reason:** {reason}', color = bot.color_code)
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
    await ctx.send(embed = embed)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify a User to Mute")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps! You don't have Permissions to That!")

@bot.command(name = 'unmute', help = 'unmutes a Member')
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member: discord.Member):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot Mute yourself!")
        return
    guild = bot.get_guild(int(GUILD))
    role = discord.utils.get(ctx.guild.roles, name='Prisoner')
    await member.remove_roles(role)
    embed = discord.Embed(title = 'User Unmuted',description = f'{member.mention} has been Unmuted', color = bot.color_code)
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
    await ctx.send(embed = embed)

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify a User to Unmute")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("OOps! You don't have Permissions to That!")


@bot.command(name = 'kick', help = 'kicks the user')
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = 'Unspecified'):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot kick yourself!")
        return
    guild = bot.get_guild(int(GUILD))
    await member.kick(reason=reason)
    channel = bot.get_channel(int(GCI))
    embed = discord.Embed(title = 'User Kicked',description = f'{member.mention} has been kicked from the Server\n**Reason:** {reason}', color = bot.color_code)
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
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
    guild = bot.get_guild(int(GUILD))
    await member.ban(reason=reason)
    channel = bot.get_channel(int(GCI))
    embed = discord.Embed(title = 'User Banned',description = f'{member.mention} has been banned from the Server\n**Reason:** {reason}', color = bot.color_code)
    embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
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
    guild = bot.get_guild(int(GUILD))
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if(user.name, user.discriminator) == (member_name, member_discriminator):
            embed = discord.Embed(title = 'User Unbanned',description = f'{member_name}#{member_discriminator} has been Unbanned', color = bot.color_code)
            embed.set_footer(text = f'© {bot.user.name} | Owned by {guild.owner}', icon_url = bot.user.avatar_url)
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
