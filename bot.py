import discord
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Render用ダミーサーバー ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
# --------------------------------

intents = discord.Intents.none()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("LOGIN SUCCESS:", client.user)
    await client.close()

client.run(os.environ["TOKEN"])
