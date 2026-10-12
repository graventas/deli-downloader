# Deli Downloader

A small portfolio project built with Python, Flask, and `yt-dlp`. Paste a supported public media URL and the app will attempt to return a downloadable file.

## Features
- Responsive dark interface
- Compatible public URLs from YouTube, TikTok, and Instagram
- HTTPS URL allowlist, 200 MB limit, and basic rate limiting
- Temporary per-request download storage
- Render deployment configuration and basic tests

## Responsible use
Only download content you own or have permission to save. Respect copyright, platform terms, and applicable law. Private/login-only media is not supported; do not use this project to bypass DRM or access controls. Platform support can change, and successful deployment does not guarantee every URL will work. Review hosting-provider policies before public deployment.

## Run locally on Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe app.py
```
Open `http://127.0.0.1:5000`.

## Deploy to Render
1. Upload the project files to a GitHub repository named `deli-downloader`.
2. In Render, select **New → Blueprint** and connect that repository.
3. Render reads `render.yaml`, installs dependencies, and starts Gunicorn.
4. Test the public URL with media you are allowed to download.

Downloaded media is temporary, not permanent storage. Free hosting may sleep or impose resource, bandwidth, and runtime limits.

## Project layout
```text
deli-downloader/
├── app.py
├── downloader.py
├── requirements.txt
├── render.yaml
├── README.md
├── LICENSE
├── .gitignore
├── templates/index.html
├── static/style.css
└── tests/
    ├── test_app.py
    └── test_downloader.py
```
