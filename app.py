import discord
import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.reactions = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

issue_count = 0  # Zähler für Anliegen

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def issue(ctx, anliegen, prioritaet: int, *, beschreibung):
    global issue_count
    issue_count += 1
    
    if anliegen.lower() not in ['frage', 'info', 'aufgabe']:
        await ctx.send("Ungültiges Anliegen. Bitte wähle zwischen 'frage', 'info' oder 'aufgabe'.")
        return
    
    if prioritaet < 1 or prioritaet > 5:
        await ctx.send("Ungültige Priorität. Bitte wähle eine Zahl zwischen 1 und 5.")
        return
    
    embed = discord.Embed(
        description=f'**Name:** {ctx.author.name}\n**Server:** {ctx.guild.name}\n**Channel:** {ctx.channel.name}\n**Server ID:** {ctx.guild.id}\n**Channel ID:** {ctx.channel.id}\n**Datum/Uhrzeit:** {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}\n\n**Anliegen:** {anliegen}\n**Priorität:** {prioritaet}\n\n**Beschreibung:** {beschreibung}',
        color=2105893
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1132957439189331968/1140574869969436793/1113118860627943435.png")
    embed.set_author(name=f"Anliegen #{issue_count}", icon_url="https://cdn.discordapp.com/attachments/1132957439189331968/1140574869969436793/1113118860627943435.png")
    
    confirmation_embed = discord.Embed(description="Dein Anliegen wurde aufgenommen und bestätigt!", color=discord.Color.green())
    
    await ctx.send(embed=confirmation_embed)
    
    destination_channel = bot.get_channel(1140576927837605908)  # Ziel-Channel-ID für Anliegen-Embeds
    issue_message = await destination_channel.send(embed=embed)  # Anliegen-Embed im Ziel-Channel senden
    
    # Logging der Anliegen in issue.txt
    with open("issue.txt", "a") as file:
        file.write(f"Issue #{issue_count}\n")
        file.write(f"User: {ctx.author.name}\n")
        file.write(f"Datum/Uhrzeit: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Server: {ctx.guild.name} (ID: {ctx.guild.id})\n")
        file.write(f"Channel: {ctx.channel.name} (ID: {ctx.channel.id})\n")
        file.write(f"Anliegen: {anliegen}\n")
        file.write(f"Priorität: {prioritaet}\n")
        file.write(f"Beschreibung: {beschreibung}\n")
        file.write("----------\n")

    
TOKEN = 'BOT_TOKEN'  # Hier den Token deines Bots einfügen
bot.run(TOKEN)
