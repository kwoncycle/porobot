import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required to read message text

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == "!ping":
        await message.channel.send("🏓 Pong!")
    if "fault" in message.content.lower():
        try:
            await message.delete()
            print(f"🗑️ Deleted message from {message.author}: {message.content}")
            # (Optional) Notify in channel or DM
            await message.channel.send(f"⚠️ Message from {message.author.mention} deleted (contained banned word).", delete_after=5)
        except discord.Forbidden:
            print("❌ Missing permissions to delete messages.")
        except discord.HTTPException as e:
            print(f"⚠️ Error deleting message: {e}")
            
client.run(TOKEN)