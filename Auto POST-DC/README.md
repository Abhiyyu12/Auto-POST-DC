```markdown
# Auto POST-DC

Sebuah **web dashboard controller** berbasis Flask yang simpel, modern, dan powerful untuk mengatur **auto-posting pesan otomatis ke channel Discord** menggunakan multiple akun (multi-account).

## Fitur Utama
- Tambah, edit, hapus akun Discord (menggunakan token)
- Kelola channel target dengan pesan custom dan interval waktu (minimal 5 detik)
- Start / Stop posting per channel secara independen
- Logging real-time (10 log terakhir per channel)
- Optional: Kirim log sukses/gagal ke Discord webhook
- Dark / Light mode toggle
- Sidebar collapsible yang presisi dan responsif
- Desain UI modern dengan Bootstrap 5 + animasi halus

## Screenshot
*(Tambahkan screenshot dashboard kamu di sini nanti untuk membuat repo lebih menarik)*

![Auto POST-DC Dashboard](https://via.placeholder.com/1200x600?text=Auto+POST-DC+Dashboard+Screenshot)  
*(Ganti dengan screenshot asli setelah kamu upload ke repo atau Imgur)*

## Cara Instalasi & Menjalankan

1. **Clone repository**
   ```bash
   git clone https://github.com/Abhiyyu12/Auto-POST-DC.git
   cd Auto-POST-DC
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi**
   ```bash
   python app.py
   ```

4. Buka di browser:
   ```
   http://localhost:3000
   ```

## Struktur Project
```
Auto-POST-DC/
├── app.py                # Entry point Flask
├── utils.py              # Fungsi config & webhook log
├── threads.py            # Manajemen thread posting & logging
├── templates/
│   └── index.html        # UI dashboard utama
├── config.json           # Dibuat otomatis (jangan commit token!)
├── requirements.txt
├── README.md             # Dokumentasi ini
└── .gitignore
```

## Penggunaan
- **Accounts** → Tambah token Discord (gunakan alt account untuk aman)
- **Webhooks** → Tambah webhook Discord untuk notifikasi log (opsional)
- **Channels** → Atur channel ID, pesan, interval, pilih akun & webhook
- Klik **Start** untuk aktifkan auto-post, **Stop** untuk hentikan
- Log otomatis refresh setiap 1.5 detik

## Keamanan Penting ⚠️
- **JANGAN pernah commit `config.json` yang berisi token Discord asli!**
- File `config.json` sudah di-ignore oleh `.gitignore`
- Gunakan token dari akun alternatif untuk menghindari rate limit atau banned

## Credit
- Original base code oleh **Ke200**
- Refactor, modularisasi, fix sidebar, dan improvement oleh **Abhiyyu12**

---

**Auto POST-DC** – Posting otomatis ke Discord jadi mudah dan rapi! 🚀

Kalau ada issue atau saran fitur baru, buka Issue di repo ini ya!
```

Simpan seluruh teks di atas sebagai file **README.md** di root folder project kamu (https://github.com/Abhiyyu12/Auto-POST-DC).

Setelah itu tinggal commit & push:

```bash
git add README.md
git commit -m "Add complete README"
git push origin main
```

Repo kamu sekarang sudah punya README yang rapi, profesional, dan lengkap dalam **satu file** saja seperti yang kamu minta. Selamat! 🔥