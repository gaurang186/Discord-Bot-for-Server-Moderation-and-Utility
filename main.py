import datetime
import json
import discord
from discord.ext import commands
bot_name = "" # replace with your bot name
bot_pfp = "" # replace with your image URL

intents = discord.Intents.all()
intents.members = True # This will enable the bot to receive member join events.
intents.guild_messages = True # This will enable the bot to receive messages in guilds/servers.

client = commands.Bot(command_prefix='.', intents=intents, self_bot=False, case_insensitive=True, activity=discord.Game(name="with Kenshin"), avatar_url=bot_pfp)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="with paolo"))
    print(f'{client.user} is online and ready to use!')

# Load the welcome message data from a JSON file
with open('welcome_messages.json', 'r') as f:
    welcome_messages = json.load(f)



@client.event
async def on_member_join(member):
    guild = member.guild
    channel = await guild.fetch_channel() #replace with your channel ID
    #role = discord.utils.get(guild.roles, name='1+ Manga')
    

   # Assign the new member role to the new member
    #await member.add_roles(role)
    
    # Get the server's welcome message from the JSON file, or use a default message
    message = welcome_messages.get(str(guild.id), 'Welcome to the server!')
    
    # Replace the placeholders with the member's username and the server's name
    message = message.replace('{user}', member.mention)
    message = message.replace('{server}', guild.name)

  
    await channel.send(message)

@client.event
async def on_member_remove(member):
    channel_id =   # Replace with your channel ID
    channel = client.get_channel(channel_id)
    message = f'{member.mention} ({member.name}#{member.discriminator}) has left the server. ID: {member.id}'
    await channel.send(message)
    




@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    print("Kick function called!")
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked from the server. Reason: {reason}')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned from the server. Reason: {reason}')

@client.command()
async def poll(ctx, question, *options):
    if len(options) > 10:
        await ctx.send("Sorry, I can only handle up to 10 options.")
        return
    
    # Create the poll message
    poll_message = f"{question}\n\n"
    for i, option in enumerate(options):
        poll_message += f"{i+1}. {option}\n"
    
    # Send the poll message and add reactions to each option
    poll = await ctx.send(poll_message)
    for i in range(len(options)):
        emoji = chr(ord('🇦') + i)
        await poll.add_reaction(emoji)

@client.command()
async def message_count(ctx, member: discord.Member, start_date: str, end_date: str):
    message_count = 0
    
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    
    for channel in ctx.guild.text_channels:
        async for message in channel.history(limit=None, before=end_date, after=start_date):
            if message.author == member:
                message_count += 1
    
    await ctx.send(f"{member.name} has sent {message_count} messages between {start_date.date()} and {end_date.date()} in this server.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role, reason=reason)
    await ctx.send(f'{member.mention} has been muted. Reason: {reason}')

@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role, reason=reason)
    await ctx.send(f'{member.mention} has been unmuted. Reason: {reason}')

@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    # Add code here to store warnings in a database or file
    await ctx.send(f'{member.mention} has been warned. Reason: {reason}')

@client.command()
async def commands(ctx):
    embed = discord.Embed(title="Bot Commands", description="Here are all the commands available for this bot:")
    for command in client.commands:
        embed.add_field(name=f"{command.name} {command.signature}", value=command.help, inline=False)
    await ctx.send(embed=embed)


client.run('') #replace with your discord api token