import discord
import random
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot起動: {client.user}")

@client.event
async def on_member_join(member):
    new_name = "U-" + str(random.randint(1000, 9999))
    try:
        await member.edit(nick=new_name)
        print(f"名前変更成功: {member} -> {new_name}")
    except Exception as e:
        print(f"名前変更失敗: {member} / {e}")

client.run(os.environ["TOKEN"])
