import discord
import random
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- ダミーHTTPサーバー（Render対策） ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
# ----------------------------------------

# Discord設定
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

# 環境変数からトークン取得
client.run(os.environ["TOKEN"])