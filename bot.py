import os
import discord
import re
from dotenv import load_dotenv

_CUSTOM_EMOJI_RE = re.compile(r"<a?:([A-Za-z0-9_]+):\d+>")

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required to read message text

client = discord.Client(intents=intents)

async def react_to_ggang(message: discord.Message) -> bool:
    """
    Reacts only if the message contains a **custom emoji** whose **name** contains 'ggang'.
    - If any such emoji's name contains 'poro_ggang' -> react with 🤬 (face_with_symbols_over_mouth)
    - Else (still contains 'ggang' in some emoji name) -> react with 🥰 (smiling_face_with_3_hearts)
    Returns True if a reaction was added, else False.
    """
    # 1) collect custom emoji names in the message
    emoji_names = []

    # Preferred: discord.py provides custom emojis used in the message
    if hasattr(message, "emojis") and message.emojis:
        emoji_names = [(e.name or "") for e in message.emojis]
    else:
        # Fallback: parse text for <:name:id> / <a:name:id>
        emoji_names = _CUSTOM_EMOJI_RE.findall(message.content or "")

    names_lower = [n.lower() for n in emoji_names]
    # 2) only proceed if at least one emoji name contains 'ggang'
    ggang_names = [n for n in names_lower if "ggang" in n]
    if not ggang_names:
        return False

    # 3) priority: if ANY emoji name contains 'poro_ggang' -> angry, else hearts
    reaction = "🤬" if any("poro_ggang" in n for n in ggang_names) else "🥰"

    try:
        await message.add_reaction(reaction)
        return True
    except discord.Forbidden:
        # missing Add Reactions permission
        return False
    except discord.HTTPException:
        return False


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    await react_to_ggang(message)


    # if message.content.lower() == "!ping":
    #     await message.channel.send("🏓 Pong!")
    # if "fault" in message.content.lower():
    #     try:
    #         await message.delete()
    #         print(f"🗑️ Deleted message from {message.author}: {message.content}")
    #         # (Optional) Notify in channel or DM
    #         await message.channel.send(f"⚠️ Message from {message.author.mention} deleted (contained banned word).", delete_after=5)
    #     except discord.Forbidden:
    #         print("❌ Missing permissions to delete messages.")
    #     except discord.HTTPException as e:
    #         print(f"⚠️ Error deleting message: {e}")

client.run(TOKEN)