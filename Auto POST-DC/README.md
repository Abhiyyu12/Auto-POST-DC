Berikut **versi bahasa Inggris** dari teks Markdown yang kamu kirim, **siap langsung dipakai sebagai `README.md`**:

````markdown
# Auto POST-DC

A **simple, modern, and powerful Flask-based web dashboard controller** for managing **automatic message posting to Discord channels** using multiple accounts (multi-account support).

## Main Features
- Add, edit, and delete Discord accounts (using tokens)
- Manage target channels with custom messages and time intervals (minimum 5 seconds)
- Start / Stop posting per channel independently
- Real-time logging (last 10 logs per channel)
- Optional: Send success/failure logs to a Discord webhook
- Dark / Light mode toggle
- Precise and responsive collapsible sidebar
- Modern UI design with Bootstrap 5 + smooth animations

## Screenshot
*(Add your dashboard screenshot here later to make the repository more attractive)*

![Auto POST-DC Dashboard](https://via.placeholder.com/1200x600?text=Auto+POST-DC+Dashboard+Screenshot)  
*(Replace this with a real screenshot after uploading it to the repository or Imgur)*

## Installation & Running

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abhiyyu12/Auto-POST-DC.git
   cd Auto-POST-DC
````

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python app.py
   ```

4. Open in your browser:

   ```
   http://localhost:3000
   ```

## Project Structure

```
Auto-POST-DC/
├── app.py                # Flask entry point
├── utils.py              # Config & webhook logging helpers
├── threads.py            # Posting thread & logging management
├── templates/
│   └── index.html        # Main dashboard UI
├── config.json           # Auto-generated (DO NOT commit tokens!)
├── requirements.txt
├── README.md             # This documentation
└── .gitignore
```

## Usage

* **Accounts** → Add Discord tokens (use alt accounts for safety)
* **Webhooks** → Add Discord webhooks for log notifications (optional)
* **Channels** → Set channel ID, message, interval, select account & webhook
* Click **Start** to enable auto-posting, **Stop** to disable it
* Logs refresh automatically every 1.5 seconds

## Important Security Notice ⚠️

* **NEVER commit `config.json` containing real Discord tokens**
* `config.json` is already ignored by `.gitignore`
* Use alternative Discord accounts to avoid rate limits or bans

## Credits

* Original base code by **Ke200**
* Refactor, modularization, sidebar fixes, and improvements by **Abhiyyu12**


Tinggal bilang 👍
```
