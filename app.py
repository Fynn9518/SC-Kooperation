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

issue_count = ISSUE_COUNT  
news_channel_list = [CHANNEL_IDs] 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
@commands.has_permissions(administrator=True)
async def issue(ctx, *, beschreibung):
    global issue_count
    issue_count += 1
    
    embed = discord.Embed(
        description=f'**Name:** {ctx.author.name}\n**Server:** {ctx.guild.name}\n**Channel:** {ctx.channel.name}\n\n**Server ID:** {ctx.guild.id}\n**Channel ID:** {ctx.channel.id}\n\n**Datum/Uhrzeit:** {datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}\n\n**Beschreibung:** {beschreibung}',
        color=2105893
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1132957439189331968/1140574869969436793/1113118860627943435.png")
    embed.set_author(name=f"Anliegen #{issue_count}", icon_url="https://cdn.discordapp.com/attachments/1132957439189331968/1140574869969436793/1113118860627943435.png")
    
    confirmation_embed = discord.Embed(description="Dein Anliegen wurde aufgenommen und bestätigt!", color=discord.Color.green())
    
    await ctx.send(embed=confirmation_embed)
    
    destination_channel = bot.get_channel(ISSUE_CHANNEL)  
    issue_message = await destination_channel.send(embed=embed)  
    
  
    with open("issue.txt", "a") as file:
        file.write(f"Issue #{issue_count}\n")
        file.write(f"User: {ctx.author.name}\n")
        file.write(f"Datum/Uhrzeit: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        file.write(f"Server: {ctx.guild.name} (ID: {ctx.guild.id})\n")
        file.write(f"Channel: {ctx.channel.name} (ID: {ctx.channel.id})\n")
        file.write(f"Beschreibung: {beschreibung}\n")
        file.write("----------\n")
    
    
    await issue_message.add_reaction('✅')

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
   
    if reaction.message.channel.id == ISSUE_CHANNEL and reaction.emoji == '✅':
        try:
           
            new_channel = bot.get_channel(ISSUE_LOG_CHANNEL)
            
            
            await reaction.message.delete()
            await new_channel.send(embed=reaction.message.embeds[0])
        
        except Exception as e:
          
            print(f"Fehler beim Verschieben der Nachricht: {e}")

@bot.command()
async def sc_help(ctx):
    help_embed = discord.Embed(
        title="Bot Commands",
        description="Hier sind die verfügbaren Befehle für diesen Bot:",
        color=discord.Color.blue()
    )
    help_embed.add_field(
        name="!issue [beschreibung]",
        value="Erstelle ein Anliegen mit einer Beschreibung. Dieses Anliegen wird direkt an Supportive-Connect weitergeleitet. Admin only!",
        inline=False
    )
    help_embed.add_field(
        name="!sc_channel [channel_id]",
        value="Füge einen Kanal zur Liste der News-Channels hinzu. Admin only!",
        inline=False
    )
    
    await ctx.send(embed=help_embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def sc_channel(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)
    if channel:
        news_channel_list.append(channel_id)
        await ctx.send(f"Kanal {channel.name} wurde zur News-Channel-Liste hinzugefügt.")
    else:
        await ctx.send("Ungültige Kanal-ID.")

@bot.command()
async def kooperation_news(ctx, *, nachricht):
   
    if ctx.author.id != AUTHOR_ID:
        await ctx.send("Du bist nicht berechtigt, diesen Befehl zu nutzen.")
        return

    if not news_channel_list:
        await ctx.send("Es gibt keine Kanäle in der News-Channel-Liste.")
        return
    
    embed = discord.Embed(
        description=nachricht,
        color=discord.Color.orange()
    )
    
    for channel_id in news_channel_list:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed)
    
    await ctx.send("Nachricht wurde an alle News-Channels gesendet.")

TOKEN = 'BOT_TOKEN'
bot.run(TOKEN)
