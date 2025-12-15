import time
import requests
import datetime
from threading import Event, Thread

channel_threads = {}
channel_stop_events = {}
channel_logs = {}

def log_channel(channel_id, message, success=True):
    if channel_id not in channel_logs:
        channel_logs[channel_id] = []
    now = datetime.datetime.now().strftime("%H:%M:%S")
    entry = {"time": now, "message": message, "success": success}
    channel_logs[channel_id].insert(0, entry)
    channel_logs[channel_id] = channel_logs[channel_id][:10]

def post_loop(channel, config):
    from utils import get_account, send_webhook_log
    acc = get_account(config, channel["account_id"])
    if not acc:
        log_channel(channel["id"], "Account not found!", False)
        send_webhook_log(channel["id"], "Account not found!", False, channel.get("webhook_id"), config)
        return

    stop_event = channel_stop_events.get(channel["id"])
    if not stop_event:
        return

    headers = {"Authorization": acc["token"], "Content-Type": "application/json"}

    while not stop_event.is_set():
        try:
            url = f"https://discord.com/api/v10/channels/{channel['id']}/messages"
            r = requests.post(url, headers=headers, json={"content": channel["message"]}, timeout=10)
            ok = r.status_code in (200, 201, 204)
            msg = f"Sent [{r.status_code}] - {'Success ✅' if ok else 'Failed'}"
            log_channel(channel["id"], msg, ok)
            send_webhook_log(channel["id"], msg, ok, channel.get("webhook_id"), config)
        except Exception as e:
            err = f"Error: {str(e)[:100]}"
            log_channel(channel["id"], err, False)
            send_webhook_log(channel["id"], err, False, channel.get("webhook_id"), config)

        for _ in range(channel["interval"]):
            if stop_event.is_set():
                break
            time.sleep(1)

def start_channel(channel, config):
    stop_event = Event()
    channel_stop_events[channel["id"]] = stop_event
    t = Thread(target=post_loop, args=(channel.copy(), config), daemon=True)
    channel_threads[channel["id"]] = t
    t.start()

def stop_channel(channel_id):
    if channel_id in channel_stop_events:
        channel_stop_events[channel_id].set()
        channel_threads.pop(channel_id, None)
        channel_stop_events.pop(channel_id, None)