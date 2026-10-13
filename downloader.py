
from pathlib import Path
from urllib.parse import urlparse
import shutil

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
    """Error aman untuk ditampilkan kepada pengguna."""


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

        return parsed.hostname.lower().rstrip(".") in ALLOWED_HOSTS

    except (ValueError, TypeError):
        return False


def download_media(url: str, output_dir: str) -> str:
    if not validate_url(url):
        raise DownloadError(
            "URL tidak valid atau platform belum didukung."
        )

    try:
        import yt_dlp

        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)

        # ID media membantu menemukan hasil unduhan yang tepat.
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
            "format": (
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]"
                "/best[ext=mp4]"
                "/bestvideo+bestaudio"
                "/best"
            ),
            "merge_output_format": "mp4",
            "overwrites": False,
            "ignoreerrors": False,
        }

        if not shutil.which("ffmpeg"):
            raise DownloadError(
                "FFmpeg belum tersedia di server."
            )

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

            if not info:
                raise DownloadError(
                    "Media tidak ditemukan atau tidak bisa diakses."
                )

            # Playlist tidak diizinkan; ambil ID media tunggal.
            media_id = info.get("id")
            if not media_id:
                raise DownloadError(
                    "Informasi media tidak lengkap."
                )

            # Cari file yang benar-benar dihasilkan untuk ID ini,
            # termasuk hasil merge yang berekstensi .mp4.
            candidates = [
                p for p in output_path.glob(f"*-{media_id}.*")
                if p.is_file()
                and p.suffix.lower() in {
                    ".mp4", ".webm", ".mkv", ".mov"
                }
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
                "YouTube menolak permintaan server "
                "karena pemeriksaan anti-bot. Coba lagi nanti."
            ) from exc

        if any(term in message for term in (
            "private video",
            "video is private",
            "login required",
            "private",
        )):
            raise DownloadError(
                "Media privat atau memerlukan login tidak didukung."
            ) from exc

        if any(term in message for term in (
            "max-filesize",
            "file is larger",
            "filesize",
            "maximum file size",
        )):
            raise DownloadError(
                "File melebihi batas ukuran 200 MB."
            ) from exc

        if "ffmpeg" in message:
            raise DownloadError(
                "Pemrosesan video gagal. Periksa instalasi FFmpeg."
            ) from exc

        raise DownloadError(
            "Platform gagal menyediakan media. "
            "Periksa URL dan koneksi, lalu coba lagi."
        ) from exc
