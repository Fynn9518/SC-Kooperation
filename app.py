import discord
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
        description=f'**Name:** {ctx.author.name}\n**Server:** {ctx.guild.name}\n\n**Anliegen:** {anliegen}\n**Priorität:** {prioritaet}\n\n**Beschreibung:** {beschreibung}',
        color=2105893
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1132957439189331968/1140574869969436793/1113118860627943435.png")
    embed.set_author(name="Anliegen #{issue_count}", icon_url="https://cdn.discordapp.com/attachments/1132957439189331968/1140574869969436793/1113118860627943435.png")
    
    confirmation_embed = discord.Embed(description="Dein Anliegen wurde aufgenommen und bestätigt!", color=discord.Color.green())
    
    await ctx.send(embed=confirmation_embed)
    
    destination_channel = bot.get_channel(CHANNEL_ID_AWNSER)  # Ziel-Channel-ID für Anliegen-Embeds
    issue_message = await destination_channel.send(embed=embed)  # Anliegen-Embed im Ziel-Channel senden
    await issue_message.add_reaction('✅')  # Hinzufügen der Reaktion für Bestätigung
    await issue_message.add_reaction('📌')  # Hinzufügen der Reaktion für "zur Kenntnis genommen"

@bot.event
async def on_reaction_add(reaction, user):
    global issue_count
    if user.bot:
        return
    
    if str(reaction.emoji) == '✅':
        await reaction.message.channel.send(f'Das Anliegen #{issue_count} wurde bearbeitet.')
    elif str(reaction.emoji) == '📌':
        await reaction.message.channel.send('Information wurde zur Kenntnis genommen.')

    
TOKEN = 'BOT_TOKEN'  # Hier den Token deines Bots einfügen
bot.run(TOKEN)
