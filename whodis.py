import discord, json, asyncio, datetime
from discord.utils import get
from discord.ext.commands import has_permissions, CheckFailure
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext import tasks
from discord import File
from discord_slash import SlashCommand 
from requests_html import HTMLSession
###########################################################################################################
# Colors
Orange = 0xfc9003

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file) # CONFIG.JSON

intents = discord.Intents.all()
client = commands.Bot(command_prefix=config['bot']['prefix'], intents=intents, case_insensitive=False)
slash = SlashCommand(client, sync_commands=True) 
intents.members = True 
intents.messages = True
client.remove_command('help') 
# HTML 
s = HTMLSession()

@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print(f"{client.user.name} is online.")
    print("[!] CONSOLE LOG:")

# Rotating Status
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(name="🕵️: Providing fraud awareness."), status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game("Support: Feva#2571"), status=discord.Status.online)
        await asyncio.sleep(10)

@slash.slash(name="Lookup", description="Search a phone number. Ex: 111-111-1111")
async def lookup(ctx, query):
    url = f"https://directory.youmail.com/phone/{query}"
    r = s.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'})
    try:
        Calltype = (r.html.find('h1.mdc-typography--headline1.ym-phone-number-title', first=True).text)
    except AttributeError:
        Calltype = "No results"
    try:
        Detection = (r.html.find('span.mdc-typography--headline5.ym-phone-number-risk', first=True).text)
    except AttributeError:
        Detection = "No results"
    try:
        Callmessage = (r.html.find('p.typical-message-text', first=True).text)
    except AttributeError:
        Callmessage = "No results"
    try:
        Name = (r.html.find('h2.mdc-typography--headline5.ym-phone-number-field.mr-3', first=True).text)
    except AttributeError:
        Name = "No results"

    embed = discord.Embed(title="Phone Number Report", colour= Orange)
    embed.add_field(name="📡 Name:", value=f"{Name}", inline=False)
    embed.add_field(name="📄 Results:", value=f"{Calltype}", inline=False)
    embed.add_field(name="<:whodisalert:1052005461488054292> Type:", value=f"{Detection}", inline=False)
    embed.add_field(name="🔊 Typical Message:", value=f"{Callmessage}", inline=False)
    embed.set_thumbnail(url=f"https://directory.youmail.com/directory/map/United%20States/100x100/1")
    embed.set_footer(text = f"Number Searched: {query}")
    await ctx.send(embed=embed)

client.run(config['bot']['token'])