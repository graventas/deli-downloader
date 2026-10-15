# Deli Downloader (Tiktok Only)

link online:
https://deli-downloader-production.up.railway.app/

## Kalo mau jalanin local di powershell
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
