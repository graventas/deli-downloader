import os, tempfile, shutil
from pathlib import Path
from flask import Flask, render_template, request, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from downloader import download_media, validate_url, DownloadError

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-development-only-change-me")
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per hour"], storage_uri="memory://")

@app.get("/")
def index():
    return render_template("index.html", error=None)

@app.post("/download")
@limiter.limit("3 per hour")
def download():
    url = (request.form.get("url") or "").strip()
    if not validate_url(url):
        return render_template("index.html", error="Masukkan URL HTTPS yang valid dari platform yang didukung."), 400
    temp_dir = tempfile.mkdtemp(prefix="deli-download-")
    try:
        output_path = Path(download_media(url, temp_dir))
        if not output_path.is_file():
            raise DownloadError("File hasil download tidak ditemukan.")
        if output_path.stat().st_size > 200 * 1024 * 1024:
            raise DownloadError("File melebihi batas ukuran 200 MB.")
        response = send_file(output_path, as_attachment=True, download_name=output_path.name, conditional=True)
        response.call_on_close(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
        return response
    except DownloadError as exc:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return render_template("index.html", error=str(exc)), 400
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        app.logger.exception("Unexpected download failure")
        return render_template("index.html", error="Download gagal. Periksa koneksi, URL, atau coba lagi nanti."), 500

@app.errorhandler(429)
def rate_limited(_error):
    return render_template("index.html", error="Batas percobaan tercapai. Coba lagi nanti."), 429

@app.errorhandler(413)
def too_large(_error):
    return render_template("index.html", error="Permintaan terlalu besar."), 413

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
