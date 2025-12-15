from flask import Flask, render_template, request, redirect, flash, jsonify, url_for
import uuid
from utils import load_config, save_config, get_account, get_webhook, send_webhook_log
from threads import start_channel, stop_channel, channel_logs

app = Flask(__name__)
app.secret_key = "supersecretkey_change_this_to_random_string"

# ========================
# ROUTE UTAMA - INDEX
# ========================
@app.route("/")
def index():
    config = load_config()
    channels_view = []
    active_channels = 0

    for c in config["channels"]:
        acc = get_account(config, c["account_id"])
        wh = get_webhook(config, c.get("webhook_id"))
        channels_view.append({
            **c,
            "account_name": acc["name"] if acc else "Unknown",
            "webhook_name": wh["name"] if wh else None,
            "logs": channel_logs.get(c["id"], [])
        })
        if c.get("active", False):
            active_channels += 1

    total_accounts = len(config["accounts"])

    return render_template("index.html",
                           config=config,
                           channels=channels_view,
                           active_channels=active_channels,
                           total_accounts=total_accounts)


# ========================
# API LOGS REAL-TIME
# ========================
@app.route("/api/logs")
def api_logs():
    config = load_config()
    logs = {}
    for c in config["channels"]:
        logs[c["id"]] = channel_logs.get(c["id"], [])
    return jsonify(logs)


# ========================
# ACCOUNT ROUTES
# ========================
@app.route("/add-account", methods=["POST"])
def add_account():
    config = load_config()
    name = request.form["name"].strip()
    token = request.form["token"].strip()
    if not name or not token:
        flash("Account name and token are required!", "danger")
        return redirect("/#accounts")

    config["accounts"].append({
        "id": str(uuid.uuid4()),
        "name": name,
        "token": token
    })
    save_config(config)
    flash("Account added successfully!", "success")
    return redirect("/#accounts")


@app.route("/edit-account/<acc_id>", methods=["POST"])
def edit_account(acc_id):
    config = load_config()
    account = get_account(config, acc_id)
    if not account:
        flash("Account not found!", "danger")
        return redirect("/#accounts")

    name = request.form["name"].strip()
    token = request.form["token"].strip()
    if not name or not token:
        flash("Name and token are required!", "warning")
        return redirect("/#accounts")

    account["name"] = name
    account["token"] = token
    save_config(config)
    flash("Account updated successfully!", "success")
    return redirect("/#accounts")


@app.route("/delete-account/<acc_id>", methods=["POST"])
def delete_account(acc_id):
    config = load_config()
    used = any(c["account_id"] == acc_id for c in config["channels"])
    if used:
        flash("Cannot delete: account is used by a channel!", "danger")
        return redirect("/#accounts")

    config["accounts"] = [a for a in config["accounts"] if a["id"] != acc_id]
    save_config(config)
    flash("Account deleted!", "info")
    return redirect("/#accounts")


# ========================
# WEBHOOK ROUTES
# ========================
@app.route("/add-webhook", methods=["POST"])
def add_webhook():
    config = load_config()
    name = request.form["name"].strip()
    url = request.form["url"].strip()

    if not name or not url:
        flash("Webhook name and URL are required!", "danger")
        return redirect("/#webhooks")
    if not url.startswith("https://discord.com/api/webhooks/"):
        flash("Invalid Discord webhook URL!", "warning")
        return redirect("/#webhooks")

    config["webhooks"].append({
        "id": str(uuid.uuid4()),
        "name": name,
        "url": url
    })
    save_config(config)
    flash("Webhook added successfully!", "success")
    return redirect("/#webhooks")


@app.route("/edit-webhook/<wh_id>", methods=["POST"])
def edit_webhook(wh_id):
    config = load_config()
    webhook = get_webhook(config, wh_id)
    if not webhook:
        flash("Webhook not found!", "danger")
        return redirect("/#webhooks")

    name = request.form["name"].strip()
    url = request.form["url"].strip()
    if not name or not url:
        flash("Name and URL are required!", "warning")
        return redirect("/#webhooks")
    if not url.startswith("https://discord.com/api/webhooks/"):
        flash("Invalid Discord webhook URL!", "warning")
        return redirect("/#webhooks")

    webhook["name"] = name
    webhook["url"] = url
    save_config(config)
    flash("Webhook updated successfully!", "success")
    return redirect("/#webhooks")


@app.route("/delete-webhook/<wh_id>", methods=["POST"])
def delete_webhook(wh_id):
    config = load_config()
    config["webhooks"] = [w for w in config["webhooks"] if w["id"] != wh_id]
    for c in config["channels"]:
        if c.get("webhook_id") == wh_id:
            c["webhook_id"] = None
    save_config(config)
    flash("Webhook deleted!", "info")
    return redirect("/#webhooks")


# ========================
# CHANNEL ROUTES
# ========================
@app.route("/add-channel", methods=["POST"])
def add_channel():
    config = load_config()
    try:
        channel_id = request.form["channel_id"].strip()
        if not channel_id.isdigit():
            flash("Channel ID must be numeric!", "danger")
            return redirect("/#channels")

        message = request.form["message"].strip()
        if not message:
            flash("Message cannot be empty!", "danger")
            return redirect("/#channels")

        account_id = request.form["account_id"]
        if not get_account(config, account_id):
            flash("Invalid account selected!", "danger")
            return redirect("/#channels")

        webhook_id = request.form.get("webhook_id") or None

        h = int(request.form.get("hours", 0))
        m = int(request.form.get("minutes", 0))
        s = int(request.form.get("seconds", 10))
        interval = max(5, h*3600 + m*60 + s)

        config["channels"].append({
            "id": channel_id,
            "message": message,
            "interval": interval,
            "account_id": account_id,
            "webhook_id": webhook_id,
            "active": False
        })
        save_config(config)
        flash("Channel added successfully!", "success")
    except ValueError:
        flash("Invalid time format!", "danger")
    return redirect("/#channels")


@app.route("/edit-channel/<cid>", methods=["POST"])
def edit_channel(cid):
    config = load_config()
    channel = next((c for c in config["channels"] if c["id"] == cid), None)
    if not channel:
        flash("Channel not found!", "danger")
        return redirect("/#channels")

    was_active = channel.get("active", False)
    if was_active:
        stop_channel(cid)
        channel["active"] = False

    try:
        message = request.form["message"].strip()
        if not message:
            flash("Message cannot be empty!", "danger")
            return redirect("/#channels")

        account_id = request.form["account_id"]
        if not get_account(config, account_id):
            flash("Invalid account selected!", "danger")
            return redirect("/#channels")

        webhook_id = request.form.get("webhook_id") or None

        h = int(request.form.get("hours", 0))
        m = int(request.form.get("minutes", 0))
        s = int(request.form.get("seconds", 10))
        interval = max(5, h*3600 + m*60 + s)

        channel.update({
            "message": message,
            "interval": interval,
            "account_id": account_id,
            "webhook_id": webhook_id
        })

        if was_active:
            channel["active"] = True
            start_channel(channel, config)

        save_config(config)
        flash("Channel updated successfully!", "success")
    except ValueError:
        flash("Invalid time format!", "danger")

    return redirect("/#channels")


@app.route("/delete-channel/<cid>", methods=["POST"])
def delete_channel(cid):
    config = load_config()
    stop_channel(cid)
    config["channels"] = [c for c in config["channels"] if c["id"] != cid]
    channel_logs.pop(cid, None)
    save_config(config)
    flash("Channel deleted!", "info")
    return redirect("/#channels")


@app.route("/toggle-channel/<cid>", methods=["POST"])
def toggle_channel(cid):
    config = load_config()
    channel = next((c for c in config["channels"] if c["id"] == cid), None)
    if not channel:
        flash("Channel not found!", "danger")
        return redirect("/#channels")

    if channel.get("active", False):
        stop_channel(cid)
        channel["active"] = False
        flash(f"Stopped posting to channel {cid}", "warning")
    else:
        if not get_account(config, channel["account_id"]):
            flash("Account not valid or missing!", "danger")
            return redirect("/#channels")
        channel["active"] = True
        start_channel(channel, config)
        flash(f"Started posting to channel {cid}", "success")

    save_config(config)
    return redirect("/#channels")


# ========================
# DARK MODE TOGGLE
# ========================
@app.route("/toggle-dark-mode", methods=["POST"])
def toggle_dark_mode():
    config = load_config()
    config["dark_mode"] = not config["dark_mode"]
    save_config(config)
    return jsonify({"dark_mode": config["dark_mode"]})


if __name__ == "__main__":
    # Pastikan folder templates ada
    import os
    if not os.path.exists("templates"):
        os.makedirs("templates")
    app.run(host="0.0.0.0", port=3000, debug=False)