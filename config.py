from os import getenv
from dotenv import load_dotenv

load_dotenv()


def _env_bool(key: str, default: bool = False) -> bool:
    val = getenv(key)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "y", "on"}

class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", "31939892"))
        self.API_HASH = getenv("API_HASH", "a7f3a115764c8c6eebba8b3cfdccc022")

        self.BOT_TOKEN = getenv("BOT_TOKEN", "8441056561:AAFhSeSQ49OoXZiuipYD-J94xjgjISd4KS0")
        self.MONGO_URL = getenv("MONGO_URL", "mongodb+srv://mongoguess:guessmongo@cluster0.zcwklzz.mongodb.net/?retryWrites=true&w=majority")

        self.LOGGER_ID = int(getenv("LOGGER_ID", "-1003639948579"))
        self.OWNER_ID = int(getenv("OWNER_ID", "8237345360"))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 60)) * 60
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 20))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 20))

        self.SESSION1 = getenv("SESSION1") or getenv("SESSION", "AQHnXTQAHgO1jteGgK7S2SJmZM8IC84bIo9uNqGkGjAnb0QvCkBYW_UleKgfauk3gKFdpLX0gR6V716d3OmCozBwdgBACmAzepeVU6FcAcpT9KzpQLgIDrY4YarwIlsaFyXSa1xgcO_4f9YV73eRug1W4_LK8zBKBI_x-i9qY_SuPiroy2pIYTxMSHDbFjPT2AypQm0YZTzLzXwOkUK1JEUNrp9PNdEyUvmORbg28P8oRKL0dbDEJQY-eCNmya0q8v1edezTaZHpFKQrZeCB14_5cNdmFGkgPW5ab-buiVYkrlJYqnksPd4FzpCOw7qBO6Ok8XtJ6smIK4bY-UlLMqnuoloLkwAAAAH00xWPAA")
        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)

        self.SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/sadistimki")
        self.SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/fizygrup")

        self.AUTO_END = _env_bool("AUTO_END", False)
        self.AUTO_LEAVE = _env_bool("AUTO_LEAVE", False)
        self.VIDEO_PLAY = _env_bool("VIDEO_PLAY", True)
        self.COOKIES_URL = [
            url for url in getenv("COOKIES_URL", "https://batbin.me/stealthiness").split(" ")
            if url and "batbin.me" in url
        ]
        self.DEFAULT_THUMB = getenv("DEFAULT_THUMB", "https://te.legra.ph/file/3e40a408286d4eda24191.jpg")
        self.PING_IMG = getenv("PING_IMG", "https://files.catbox.moe/haagg2.png")
        self.START_IMG = getenv("START_IMG", "https://files.catbox.moe/zvziwk.jpg")
        self.WELCOME_IMG = getenv("WELCOME_IMG", "")
        self.AUDIO_QUALITY = getenv("AUDIO_QUALITY", "HIGH")
        self.VIDEO_QUALITY = getenv("VIDEO_QUALITY", "HD_720p")
        self.STREAM_CACHE = int(getenv("STREAM_CACHE", 200))
        self.FFMPEG_PARAMS = getenv("FFMPEG_PARAMS", "")
        self.STREAM_FFMPEG = getenv(
            "STREAM_FFMPEG",
            "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        )
        self.START_VIDS = [
            "https://telegra.ph/file/9b7e1b820c72a14d90be7.mp4",
            "https://telegra.ph/file/72f349b1386d6d9374a38.mp4",
            "https://telegra.ph/file/a4d90b0cb759b67d68644.mp4",
        ]
        self.STICKERS = [
            "CAACAgUAAx0Cld6nKUAACASBI_rna1O1e6g7qS-ry-aZ1ZpVEnwACgg8AAi2LEfFI5wfykOC4h4E",
            "CAACAgUAAx0Cld6nKUAACATJI_rsEJOsaAPSYGhU7bo7iEwL8AAPMDgACu2PYV8Vb8aT4_HUPHgQ",
        ]
        self.HELP_IMG_URL = getenv("HELP_IMG_URL", "https://files.catbox.moe/yg2vky.jpg")
        self.PING_VID_URL = getenv("PING_VID_URL", "https://files.catbox.moe/3ivvgo.mp4")
        self.PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://files.catbox.moe/yhaja5.jpg")
        self.STATS_VID_URL = getenv("STATS_VID_URL", "https://telegra.ph/file/e2ab6106ace2e95862372.mp4")
        self.TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://files.catbox.moe/mlztag.jpg")
        self.TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://files.catbox.moe/tiss2b.jpg")
        self.STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://files.catbox.moe/1d3da7.jpg")
        self.SOUND_IMG_URL = getenv("SOUND_IMG_URL", "https://files.catbox.moe/zhmxl.jpg")
        self.YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://files.catbox.moe/yekyxq.jpg")
        self.SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", self.YOUTUBE_IMG_URL)
        self.SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", self.YOUTUBE_IMG_URL)
        self.SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", self.YOUTUBE_IMG_URL)
        self.PLAY_EMOJIS = [
            "💞",
            "🦋",
            "🔍",
            "🎤",
            "⚡",
            "🔥",
            "🎩",
            "🌈",
            "🍷",
            "🕺",
            "📱",
            "🕊️",
            "🎉",
            "💌",
            "🧪",
        ]

    def check(self):
        missing = []
        required = ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "LOGGER_ID", "OWNER_ID"]
        missing.extend([var for var in required if not getattr(self, var)])
        if not self.SESSION1:
            missing.append("SESSION1")
        if missing:
            raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
