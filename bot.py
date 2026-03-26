import discord
import os
import asyncio
import datetime
import zoneinfo
import random
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = 1480827835072643154
JST = zoneinfo.ZoneInfo("Asia/Tokyo")

NOTICE_MESSAGES = [
    "⚠️【ご案内】メンバー間のDMによる勧誘や案内にはご注意ください。公式からのご案内は本サーバー内の投稿のみとなります。",
    "📢【注意】運営が個別にDMで案内することはありません。不審な連絡は無視のうえ、ご不明点は公式窓口をご確認ください。",
    "🔒【安全対策】個人間でのやり取りによるトラブル防止のため、DMでの勧誘・情報共有には十分ご注意ください。",
    "🚨【ご注意】公式運営を名乗る個別DMにはご注意ください。ご案内はサーバー内の公式投稿をご確認ください。",
    "📌【お知らせ】運営から個別に勧誘や案内を行うことはありません。不審な連絡にはご注意ください。",
    "🛡️【安全のために】メンバー間のDMによる勧誘・案内・情報共有には十分ご注意いただきますようお願いいたします。",
    "🔔【ご案内】不審なDMや勧誘を受けた場合は、反応せず公式案内をご確認ください。",
    "📣【注意喚起】トラブル防止のため、個人間での勧誘や案内には十分ご注意ください。公式情報はサーバー内投稿のみです。",
    "🔐【安全対策】運営がDMで直接案内を行うことはありません。不審な連絡は無視していただきますようお願いいたします。",
    "⚠️【重要】安心してご利用いただくため、DMでの勧誘・案内・情報共有には十分ご注意ください。"
]

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
notice_task_started = False

@client.event
async def on_ready():
    global notice_task_started
    print(f"Bot起動: {client.user}", flush=True)

    if not notice_task_started:
        notice_task_started = True
        print("定期投稿タスク開始", flush=True)
        client.loop.create_task(send_notice_fixed_time())

@client.event
async def on_member_join(member):
    new_name = "user" + str(member.id)[-6:]
    try:
        await member.edit(nick=new_name)
        print(f"名前変更成功: {member} -> {new_name}", flush=True)
    except Exception as e:
        print(f"名前変更失敗: {member} / {e}", flush=True)

async def send_notice_fixed_time():
    await client.wait_until_ready()

    try:
        channel = await client.fetch_channel(CHANNEL_ID)
        print(f"チャンネル取得成功: {channel}", flush=True)
    except Exception as e:
        print(f"チャンネル取得失敗: {e}", flush=True)
        return

    now = datetime.datetime.now(JST)
    target = now.replace(hour=12, minute=0, second=0, microsecond=0)

    if now >= target:
        target += datetime.timedelta(days=1)

    wait_seconds = (target - now).total_seconds()
    print(f"次回投稿まで {int(wait_seconds)} 秒待機", flush=True)
    await asyncio.sleep(wait_seconds)

    last_msg = None

    while not client.is_closed():
        try:
            candidates = [m for m in NOTICE_MESSAGES if m != last_msg]

            if not candidates:
                candidates = NOTICE_MESSAGES

            msg = random.choice(candidates)

            await channel.send(msg, silent=True)
            print(f"送信成功: {msg}", flush=True)

            last_msg = msg

        except Exception as e:
            print(f"送信エラー: {e}", flush=True)

        await asyncio.sleep(86400)

client.run(os.environ["TOKEN"])
