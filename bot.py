import discord
import random
import os

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot起動")

@client.event
async def on_member_join(member):
    new_name = "U-" + str(random.randint(1000, 9999))
    try:
        await member.edit(nick=new_name)
    except Exception as e:
        print("名前変更失敗", e)

client.run(os.getenv["TOKEN"])