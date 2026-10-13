# Deli Downloader

link:
https://deli-downloader-production.up.railway.app/

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
