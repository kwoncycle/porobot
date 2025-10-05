import os
import discord
import re
from dotenv import load_dotenv

_CUSTOM_EMOJI_RE = re.compile(r"<a?:([A-Za-z0-9_]+):\d+>")
TARGET_HANDLE = "hj_roh".lower()  # the handle you want to react to

async def react_if_hj_roh(message: discord.Message) -> bool:
    """
    If the sender's handle (username/global/display name) contains 'hj_roh',
    react with 🖕 (middle_finger).
    """
    author = message.author

    # collect all name forms that can appear
    candidates = {
        (author.global_name or "").lower(),
        (author.name or "").lower(),
        (getattr(author, "display_name", "") or "").lower(),
    }

    if any(TARGET_HANDLE in n for n in candidates if n):
        try:
            await message.add_reaction("🖕")
            print(f"🖕 reacted to message from {author}: {message.content}")
            return True
        except discord.HTTPException as e:
            print(f"⚠️ reaction failed: {e}")
            return False
    return False


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Required to read message text

client = discord.Client(intents=intents)

async def react_for_emojis(message: discord.Message) -> bool:
    """
    Reacts when the message includes certain custom emojis:
      - If ANY emoji name contains 'poro_ggang' → 🤬
      - Else if ANY emoji name contains 'ggang', 'kyaru_out', or 'byeongmin_ppak' → 🥰
      - Else → no reaction
    """

    # collect all custom emoji names from the message
    if hasattr(message, "emojis") and message.emojis:
        emoji_names = [e.name.lower() for e in message.emojis]
    else:
        emoji_names = [n.lower() for n in _CUSTOM_EMOJI_RE.findall(message.content)]

    if not emoji_names:
        return False

    # priority logic
    has_other_trigger = any(
        ("ggang" in n)
        or ("out" in n)
        or ("byeongmin_ppak" in n)
        or ("poro" in n)
        or ("kaorin" in n)
        for n in emoji_names
    )

    reaction = None
    if has_other_trigger:
        reaction = "🥰"

    if not reaction:
        return False

    try:
        await message.add_reaction(reaction)
        print(f"✅ reacted {reaction} to: {message.content}")
        return True
    except discord.HTTPException as e:
        print(f"⚠️ failed to react: {e}")
        return False


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    await react_for_emojis(message)
    await react_if_hj_roh(message)

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