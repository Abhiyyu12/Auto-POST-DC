import json
import os
import requests
import datetime
import uuid

CONFIG_PATH = "config.json"

def load_config():
    default_config = {
        "accounts": [],
        "webhooks": [],
        "channels": [],
        "dark_mode": True
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            default_config.update(data)
        except Exception as e:
            print(f"Error loading config: {e}")
    return default_config

def save_config(config):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

def get_account(config, acc_id):
    return next((a for a in config["accounts"] if a["id"] == acc_id), None)

def get_webhook(config, wh_id):
    return next((w for w in config["webhooks"] if w["id"] == wh_id), None)

def send_webhook_log(channel_id, message, success, webhook_id, config):
    webhook = get_webhook(config, webhook_id)
    if not webhook:
        return

    now_full = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    status_text = "Success ✅" if success else "Failed ❌"
    color = 65280 if success else 16711680

    payload = {
        "embeds": [{
            "title": "🚀 Auto POST-DC",
            "description": "> ✨ **Details Information**",
            "color": color,
            "fields": [
                {"name": "📡 Status Log", "value": f"> ```{status_text}```", "inline": True},
                {"name": "🕒 Date & Time", "value": f"> ```{now_full}```", "inline": True},
                {"name": "🎯 Channel Target", "value": f"> <#{channel_id}>" if channel_id else "> ❓ Unknown"},
                {"name": "💬 Status Message", "value": f">>> {message}"}
            ],
            "footer": {"text": "Auto POST-DC • By Ke200", "icon_url": "https://i.imgur.com/4M34hi2.png"},
            "timestamp": datetime.datetime.utcnow().isoformat()
        }]
    }

    try:
        requests.post(webhook["url"], json=payload, timeout=10)
    except:
        pass