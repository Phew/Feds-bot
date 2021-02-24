import discord, discord.utils, requests, time, os ,json, asyncio, logging, ipapi, pythonping, subprocess, socket, random, re
import bs4
from colorama import Fore, Back, init
from discord.ext import commands
from discord.utils import get
from bs4 import BeautifulSoup
from datetime import datetime
from itertools import cycle
intents = discord.Intents.default()
intents.members = True

token = 'TOKEN-HERE'
client = commands.Bot(command_prefix='/', intents=intents)
client.remove_command('help')
prefix = '/'
clear = lambda: os.system('cls')
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="chat")
    now = member.joined_at.strftime("%a, %d %B %Y, %I:%M %p")
    embed = discord.Embed(title=f"<:ak:811040807850737715> **Welcome To Feds**", description=f"・ welcome {member.mention}\n・ read <#811039803528708097>\n・ be active\n・ invite ur friends\n・ {member.guild.member_count} members", color=0x010000)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/797217597145088000/811459829498904576/duck-isis-1-redditt.png")
    await channel.send(embed=embed)

@client.command()
async def av(ctx, *, user: discord.Member=None):
    await ctx.message.delete()
    if not user:  
        user = ctx.message.author  
    embed=discord.Embed(title=str(user) + "'s Profile Picture", color=0x000000, timestamp=ctx.message.created_at)
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"for /help"))

@client.command()
@commands.has_guild_permissions(manage_roles=True, ban_members=True)
async def ban(ctx, member: discord.Member, *, reason = None):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}Ban")
    try:
        await member.ban(reason = reason)
        await ctx.send(f"banned `{member}`", delete_after=10)
    except:
        await ctx.send(f'could not ban `{member}`')

@client.command(name='unban')
@commands.has_guild_permissions(manage_roles=True, ban_members=True)
async def _unban(ctx, id: int):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}Unban")
    try:
        user = await client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f'unbanned `{id}`', delete_after=10)
    except:
        await ctx.send(f'could not unban `{id}`')

@client.command()
@commands.has_guild_permissions(manage_messages=True)
async def purge(ctx, limit=6000, member: discord.Member=None):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}Purge")
    await ctx.message.delete()
    msg = []
    try:
        limit = int(limit)
    except:
        return await ctx.send("please give me a number of messages to purge")
    if not member:
        await ctx.channel.purge(limit=limit)
        return await ctx.send(f"purged `{limit}` messages", delete_after=10)
    async for m in ctx.channel.history():
        if len(msg) == limit:
            break
        if m.author == member:
            msg.append(m)
    await ctx.channel.delete_messages(msg)
    await ctx.send(f"purged `{limit}` messages from `{member}`", delete_after=10)

@client.command(pass_context=True)
@commands.has_guild_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}Mute")
    try:
        role = get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.send(f'muted `{member}`', delete_after=10)
    except:
        await ctx.send(f'could not mute `{member}`')

@client.command(pass_context=True)
@commands.has_guild_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}Unmute")
    try:
        role = get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role)
        await ctx.send(f'unmuted `{member}`', delete_after=10)
    except:
        await ctx.send(f'could not unmute `{member}`')

@client.command()
async def host2ip(ctx, *, host: str):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}Host2IP")
    await ctx.message.delete()
    ip = socket.gethostbyname(host)
    embed=discord.Embed(title="IP Found!",color=0x000000, timestamp=ctx.message.created_at)
    embed.add_field(name="IP", value=f"{ip}\n", inline=True)
    embed.add_field(name="Host", value=f"{host}", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def lookup(ctx, *, ip: str):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}IP Lookup")
    ip_info = ipapi.location(ip=ip)    
    await ctx.message.delete()
    embed = discord.Embed(title=f"**{ip}** lookup!", description='',color=0x000000, timestamp=ctx.message.created_at)
    embed.add_field(name="ASN", value=f"{ip_info['asn']}", inline=True)
    embed.add_field(name="Region", value=f"{ip_info['region']}", inline=True)
    embed.add_field(name="Country", value=f"{ip_info['country_name']}", inline=True)
    embed.add_field(name="City", value=f"{ip_info['city']}", inline=True)
    embed.add_field(name="Timezone", value=f"{ip_info['timezone']}", inline=True)
    embed.add_field(name="Language", value=f"{ip_info['languages']}", inline=True)
    embed.add_field(name="ORG", value=f"{ip_info['org']}", inline=True)
    await ctx.send(embed=embed)

@client.command()
async def whois(ctx, member: discord.Member = None):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}WhoIS")
    if not member:  
        member = ctx.message.author  
    roles = [role for role in member.roles if role != ctx.guild.default_role]
    embed = discord.Embed(color=0x000000, timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)
    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Roles:", value=''.join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    embed.set_footer(text=f'Requested by {ctx.author} ')
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}Nuke")
    try:
        channel = ctx.channel
        channel_position = channel.position
        new_channel = await channel.clone()
        await channel.delete()
        await new_channel.edit(position=channel_position, sync_permissions=True)
        embed=discord.Embed(title=f" **Nuked!** ", description=f"", color=0x000000, timestamp=ctx.message.created_at)
        embed.set_image(url="https://media0.giphy.com/media/RuhIAu5P0LO7u/giphy.gif")
        await new_channel.send(embed=embed)
    except:
        await ctx.send(f'could not nuke channel')



@client.command()
async def ping(ctx, *, ip: str):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}Ping")
    result = pythonping.ping(ip, verbose=False)
    embed=discord.Embed(title="**Ping Results**", description=f"Returning Ping Results For: {ip}", color=0x000000, timestamp=ctx.message.created_at)
    embed.add_field(name="Is Live", value=result.success(), inline=False)
    embed.add_field(name="Output", value='```%s```' % "\n".join(str(x) for x in result), inline=False)
    await ctx.send(embed=embed)  

@client.command()
@commands.has_permissions(administrator=True)
async def dmall(ctx, *, dmall):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}DMALL")
    await ctx.message.delete()
    embed=discord.Embed(title=f" **Attempting to DM {ctx.guild.member_count} users** ", description=f"With the message of **{dmall}**", color=0x000000, timestamp=ctx.message.created_at)
    await ctx.send(embed=embed)
    for user in ctx.guild.members:
        try:
                await user.send(dmall)
                await asyncio.sleep(1)
        except:
                print(f"[{Fore.RED}!{Fore.WHITE}]{Fore.RED} Error messaging {Fore.WHITE}{Fore.RED}[{Fore.WHITE}{user.name}{Fore.RED}]")

@client.command()
async def sav(ctx):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}SAV")
    await ctx.message.delete()
    server = ctx.message.guild
    embed=discord.Embed(title=f" **{server.name}'s Icon** ", description=f"", color=0x000000, timestamp=ctx.message.created_at)
    embed.set_image(url=server.icon_url)
    await ctx.send(embed=embed,delete_after=10)

@client.command()
async def backend(ctx, site):
    await ctx.message.delete()
    r = requests.post('http://www.crimeflare.org:82/cgi-bin/cfsearch.cgi', data={'cfS': site})
    embed=discord.Embed(title=f"Backend", description=str(re.findall(r'(\<LI\>+(.*))', r.text)[0][1]),color=0xbf00ff, timestamp=ctx.message.created_at)

    await ctx.send(embed=embed,delete_after=10)

@client.command()
async def sba(ctx):
    print(f"{Back.BLACK}{Fore.WHITE}[{Fore.RED}{current_time}{Fore.WHITE}] {Fore.WHITE}Command Used {Fore.WHITE}- {Fore.RED}SBA")
    await ctx.message.delete()
    server = ctx.message.guild
    embed=discord.Embed(title=f" **{server.name}'s Banner** ", description=f"", color=0x000000, timestamp=ctx.message.created_at)
    embed.set_image(url=server.banner_url)
    await ctx.send(embed=embed,delete_after=10)

@client.command()
async def cpp(ctx, url: str): #Cloudssp but in a bot wow sexy epic
    req = requests.get(f'{url}//mailman/listinfo/mailman', stream=True)
    frontend = req.raw._connection.sock.getpeername()[0]

    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        backend = soup.find_all('a')
        backend = requests.get(f'{backend[0].get("href")}', stream=True)
        backend = backend.raw._connection.sock.getpeername()[0]
    else:
        backend = 'Failed'
        return

    embed=discord.Embed(title="just to flex on charge and nano cause they're retarded", description="*yeah just to flex*", color=0xbe696b)
    embed.set_author(name="CloudSSP")
    embed.add_field(name="Backend :", value=backend, inline=False)
    embed.add_field(name="Frontend Protection :", value=frontend, inline=False)
    embed.add_field(name="Target : ", value=url, inline=False)
    await ctx.send(embed=embed)

@client.command()
async def help(ctx):
     embed=discord.Embed(title=f"*Feds Help Commands*", description=f"**Moderation**\nShows all moderation commands\n\n**Tools**\nShows all tools", color=0x000000, timestamp=ctx.message.created_at)
     embed.set_image(url="https://media.discordapp.net/attachments/810275288785223782/811440020472070174/36.png")
     await ctx.send(embed=embed)

@client.command()
async def moderation(ctx):
    embed=discord.Embed(title=f"*Feds Moderation Commands*", description=f"**Ban**\nBans user\n\n**Unban**\nUnbans user\n\n**Mute**\nMutes user\n\n**Unmute**\nUnmutes user\n\n**Nuke**\nNukes current channel\n\n**DMAll**\nDM's every user in the server\n\n**Purge <NUMBER>**\nPurges amount of messages\n\n**Purge <NUMBER> <USER>**\nPurges messages from user", color=0x000000, timestamp=ctx.message.created_at)
    embed.set_image(url="https://media.discordapp.net/attachments/810275288785223782/811440020472070174/36.png")
    await ctx.send(embed=embed)

@client.command()
async def tools(ctx):
    embed=discord.Embed(title=f"*Feds Tool Commands*", description=f"**Lookup**\nFinds the geo-location of given IP\n\n**Ping**\nPings given IP", color=0x000000, timestamp=ctx.message.created_at)
    embed.set_image(url="https://media.discordapp.net/attachments/810275288785223782/811440020472070174/36.png")
    await ctx.send(embed=embed)

client.run(token)
