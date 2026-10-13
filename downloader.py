
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "tiktok.com",
    "www.tiktok.com",
    "m.tiktok.com",
    "instagram.com",
    "www.instagram.com",
}

MAX_BYTES = 200 * 1024 * 1024


class DownloadError(Exception):
    """A safe, user-displayable download error."""


def validate_url(url: str) -> bool:
    if not url or len(url) > 2048:
        return False

    try:
        parsed = urlparse(url)

        if parsed.scheme != "https" or not parsed.hostname:
            return False

        if parsed.username or parsed.password:
            return False

        if parsed.port not in (None, 443):
            return False

        hostname = parsed.hostname.lower().rstrip(".")
        return hostname in ALLOWED_HOSTS

    except (ValueError, TypeError):
        return False


def download_media(url: str, output_dir: str) -> str:
    if not validate_url(url):
        raise DownloadError(
            "URL tidak valid atau platform belum didukung."
        )

    try:
        import yt_dlp

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        template = str(
            output_path / "%(title).80B-%(id)s.%(ext)s"
        )

        options = {
            "outtmpl": template,
            "noplaylist": True,
            "max_filesize": MAX_BYTES,
            "socket_timeout": 20,
            "retries": 2,
            "fragment_retries": 2,
            "restrictfilenames": True,
            "windowsfilenames": True,
            "quiet": True,
            "no_warnings": True,
            "format": "best/bestvideo+bestaudio",
            "overwrites": False,
            "ignoreerrors": False,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

            if not info:
                raise DownloadError(
                    "Media tidak ditemukan atau tidak bisa diakses."
                )

            prepared = Path(ydl.prepare_filename(info))

            if prepared.is_file():
                result = prepared
            else:
                candidates = [
                    p for p in output_path.glob("*")
                    if p.is_file()
                ]

                if not candidates:
                    raise DownloadError(
                        "File hasil download tidak ditemukan."
                    )

                result = max(
                    candidates,
                    key=lambda p: p.stat().st_mtime,
                )

            if result.stat().st_size > MAX_BYTES:
                result.unlink(missing_ok=True)
                raise DownloadError(
                    "File melebihi batas ukuran 200 MB."
                )

            return str(result)

    except DownloadError:
        raise

    except Exception as exc:
        message = str(exc).lower()

        if "sign in to confirm you're not a bot" in message:
            raise DownloadError(
                "YouTube menolak permintaan server karena "
                "pemeriksaan anti-bot. Coba lagi nanti."
            ) from exc

        if any(
            term in message
            for term in (
                "private video",
                "video is private",
                "login required",
                "sign in",
                "private",
            )
        ):
            raise DownloadError(
                "Media privat atau memerlukan login tidak didukung."
            ) from exc

        if any(
            term in message
            for term in (
                "max-filesize",
                "file is larger",
                "filesize",
                "maximum file size",
            )
        ):
            raise DownloadError(
                "File melebihi batas ukuran 200 MB."
            ) from exc

        raise DownloadError(
            "Platform gagal menyediakan media. "
            "Periksa URL dan koneksi, lalu coba lagi."
        ) from exc
