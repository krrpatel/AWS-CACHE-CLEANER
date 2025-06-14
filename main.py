import os
import shutil
import subprocess
import json
import asyncio
import tracemalloc
from telegram import Bot

tracemalloc.start()

CONFIG_PATH = os.path.expanduser("~/.tg_config")
THRESHOLD_GB = 29  # Set your desired threshold

def ask_user_credentials():
    print("🔐 Enter setup details for Telegram notifications")
    token = input("Enter Telegram Bot Token: ").strip()
    chat_id = input("Enter Telegram Chat ID: ").strip()
    vps_id = input("Enter VPS ID (like VPS name or hostname): ").strip()

    config = {
        "token": token,
        "chat_id": chat_id,
        "vps_id": vps_id
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)
    print("✅ Config saved to ~/.tg_config")

def load_credentials():
    if not os.path.exists(CONFIG_PATH):
        ask_user_credentials()
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return config["token"], config["chat_id"], config["vps_id"]

def get_used_storage_gb():
    result = subprocess.run(
        ['df', '--output=used', '--block-size=1G', '/'],
        stdout=subprocess.PIPE, text=True
    )
    lines = result.stdout.strip().split('\n')
    used_gb = int(lines[1].strip())
    return used_gb

def clear_cache():
    try:
        huggingface_path = os.path.expanduser("~/.cache/huggingface")
        pip_path = os.path.expanduser("~/.cache/pip")

        if os.path.exists(huggingface_path):
            shutil.rmtree(huggingface_path)
        if os.path.exists(pip_path):
            shutil.rmtree(pip_path)

        return True
    except Exception as e:
        return f"❌ Error clearing cache: {str(e)}"

async def check_and_notify(bot, chat_id, vps_id):
    used_gb = get_used_storage_gb()
    if used_gb >= THRESHOLD_GB:
        result = clear_cache()
        status = "✅ Cache cleared" if result is True else result
    else:
        status = "✅ No cleanup needed"

    msg = (
        f"📦 VPS ID: {vps_id}\n"
        f"📊 Used storage: {used_gb} GB\n"
        f"🧹 Status: {status}"
    )

    await bot.send_message(chat_id=chat_id, text=msg)

async def periodic_monitor():
    token, chat_id, vps_id = load_credentials()
    bot = Bot(token=token)

    while True:
        await check_and_notify(bot, chat_id, vps_id)
        await asyncio.sleep(1800)  # 30 minutes

def main():
    print("⏳ Monitoring started every 30 minutes. Press Ctrl+C to stop.")
    asyncio.run(periodic_monitor())

if __name__ == "__main__":
    main()
