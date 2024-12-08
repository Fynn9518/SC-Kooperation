import discord
from discord.ext import commands
from discord import app_commands
import datetime

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.reactions = True
intents.typing = False
intents.presences = False

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(intents=intents, command_prefix="!")
        self.issue_count = <issue count>
        self.news_channel_list = [<News Channel>]

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash-Befehle wurden global synchronisiert!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.tree.command(name="issue", description="Erstelle ein Anliegen mit einer Beschreibung.")
@app_commands.describe(beschreibung="Anliegen")
@app_commands.default_permissions(administrator=True)
async def issue(interaction: discord.Interaction, beschreibung: str):
    bot.issue_count += 1
    issue_id = bot.issue_count

    embed = discord.Embed(
        description=(
            f"**Name:** {interaction.user.name}\n"
            f"**Server:** {interaction.guild.name}\n"
            f"**Channel:** {interaction.channel.name}\n\n"
            f"**Server ID:** {interaction.guild.id}\n"
            f"**Channel ID:** {interaction.channel.id}\n\n"
            f"**Datum/Uhrzeit:** {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
            f"**Beschreibung:** {beschreibung}"
        ),
        color=2105893
    )
    embed.set_author(
        name=f"Anliegen #{issue_id}",
        icon_url="https://cdn.discordapp.com/attachments/1132957439189331968/1140574869969436793/1113118860627943435.png"
    )
    
    confirmation_embed = discord.Embed(
        description="Dein Anliegen wurde aufgenommen und bestätigt!\nSobald das Anliegen abgeschlossen ist, kommt in diesem Kanal eine Benachrichtigung.",
        color=discord.Color.green()
    )
    
    await interaction.response.send_message(embed=confirmation_embed)
    
    destination_channel = bot.get_channel(<Ziel Channel>)
    await destination_channel.send(embed=embed)
    
    with open("issue.txt", "a") as file:
        file.write(
            f"Issue #{issue_id}\n"
            f"User: {interaction.user.name}\n"
            f"Datum/Uhrzeit: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            f"Server: {interaction.guild.name} (ID: {interaction.guild.id})\n"
            f"Channel: {interaction.channel.name} (ID: {interaction.channel.id})\n"
            f"Beschreibung: {beschreibung}\n"
            "----------\n"
        )

@bot.tree.command(name="confirm", description="Bestätige ein Anliegen und sende eine Nachricht.")
@app_commands.describe(issue_id="Die ID des Anliegens.")
async def confirm(interaction: discord.Interaction, issue_id: int):
    if interaction.user.id != <Admin ID>:
        await interaction.response.send_message("Du hast keine Berechtigung, diesen Befehl auszuführen.", ephemeral=True)
        return

    try:
        with open("issue.txt", "r") as file:
            lines = file.readlines()
        
        issue_data = None
        for i, line in enumerate(lines):
            if f"Issue #{issue_id}" in line:
                server_id_line = lines[i + 3].strip()
                channel_id_line = lines[i + 4].strip()

                server_id = int(server_id_line.split("(ID: ")[1].strip(")"))
                channel_id = int(channel_id_line.split("(ID: ")[1].strip(")"))
                issue_data = {"server_id": server_id, "channel_id": channel_id}
                break

        if not issue_data:
            await interaction.response.send_message("Anliegen-ID nicht gefunden.", ephemeral=True)
            return

        channel = bot.get_channel(issue_data["channel_id"])
        if not channel:
            await interaction.response.send_message("Kanal für das Anliegen wurde nicht gefunden.", ephemeral=True)
            return

        embed = discord.Embed(
            description="Dein Anliegen wurde bearbeitet!",
            color=discord.Color.green()
        )
        
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Anliegen #{issue_id} wurde bestätigt und im entsprechenden Kanal benachrichtigt.", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"Fehler: {e}", ephemeral=True)

@bot.tree.command(name="addchannel", description="Fügt einen Kanal zur Liste der News-Channels hinzu.")
@app_commands.describe(channel_id="Channel ID")
@app_commands.default_permissions(administrator=True)
async def addchannel(interaction: discord.Interaction, channel_id: int):
    channel = bot.get_channel(channel_id)
    if channel:
        bot.news_channel_list.append(channel_id)
        await interaction.response.send_message(f"Kanal {channel.name} wurde zur News-Channel-Liste hinzugefügt.")
    else:
        await interaction.response.send_message("Ungültige Kanal-ID.")

@bot.tree.command(name="kooperation_news", description="Sende eine Nachricht an alle News-Channels.")
@app_commands.describe(nachricht="Die Nachricht, die gesendet werden soll.")
async def kooperation_news(interaction: discord.Interaction, nachricht: str):
    if interaction.user.id != <ADMIN ID>:
        await interaction.response.send_message("KEINE RECHTE.", ephemeral=True)
        return

    if not bot.news_channel_list:
        await interaction.response.send_message("Es gibt keine Kanäle in der News-Channel-Liste.", ephemeral=True)
        return
    
    embed = discord.Embed(
        description=nachricht,
        color=discord.Color.orange()
    )
    
    for channel_id in bot.news_channel_list:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(embed=embed)
    
    await interaction.response.send_message("Nachricht wurde an alle News-Channels gesendet.")
    
@bot.tree.command(name="help", description="Zeigt eine Liste der verfügbaren Befehle und deren Beschreibungen.")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Hilfe - Verfügbare Befehle",
        description="Hier sind die Befehle, die du verwenden kannst:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="/issue beschreibung",
        value="Erstellt ein Anliegen mit einer Beschreibung.\n**Benötigt:** Administrator-Rechte.",
        inline=False
    )
    embed.add_field(
        name="/addchannel channel_id",
        value="Fügt einen Kanal zur Liste der News-Channels hinzu.\n**Benötigt:** Administrator-Rechte.",
        inline=False
    )
    embed.add_field(
        name="/help",
        value="Zeigt diese Hilfeseite an.",
        inline=False
    )
    
    embed.set_footer(text="Benutze den entsprechenden Befehl mit den beschriebenen Argumenten.")
    await interaction.response.send_message(embed=embed)


TOKEN = '<BOT TOKEN>'
bot.run(TOKEN)
