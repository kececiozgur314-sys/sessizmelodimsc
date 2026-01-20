import io
import os

import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageOps


class WelcomeCard:
    def __init__(self):
        self.font_title = ImageFont.truetype("anony/helpers/Raleway-Bold.ttf", 52)
        self.font_body = ImageFont.truetype("anony/helpers/Inter-Light.ttf", 40)
        self.fill = (255, 255, 255)

    async def _fetch_image(self, url: str) -> bytes | None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    return await resp.read()
        except Exception:
            return None

    async def _load_background(self, source: str | None) -> Image.Image | None:
        if not source:
            return None
        if source.startswith("http://") or source.startswith("https://"):
            data = await self._fetch_image(source)
            if not data:
                return None
            return Image.open(io.BytesIO(data)).convert("RGBA")
        if os.path.exists(source):
            return Image.open(source).convert("RGBA")
        return None

    def _fit_text(self, draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> str:
        if draw.textlength(text, font=font) <= max_width:
            return text
        ellipsis = "..."
        while text and draw.textlength(text + ellipsis, font=font) > max_width:
            text = text[:-1]
        return text + ellipsis if text else ""

    async def _load_avatar(self, app, user, size: int) -> Image.Image:
        photo_path = None
        try:
            photos = await app.get_profile_photos(user.id, limit=1)
            if photos:
                photo_path = await app.download_media(
                    photos[0], file_name=f"cache/welcome_{user.id}.jpg"
                )
        except Exception:
            photo_path = None

        if photo_path and os.path.exists(photo_path):
            avatar = Image.open(photo_path).convert("RGBA")
            try:
                os.remove(photo_path)
            except Exception:
                pass
        else:
            avatar = Image.new("RGBA", (size, size), (60, 60, 60, 255))
            draw = ImageDraw.Draw(avatar)
            initials = (user.first_name or "U").strip()[:1].upper()
            w = draw.textlength(initials, font=self.font_title)
            draw.text(((size - w) / 2, size * 0.30), initials, font=self.font_title, fill=self.fill)

        avatar = ImageOps.fit(avatar, (size, size), method=Image.Resampling.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
        avatar.putalpha(mask)
        return avatar

    async def generate(self, app, user, background_source: str | None) -> str | None:
        bg = await self._load_background(background_source)
        if not bg:
            return None

        width, height = bg.size
        avatar_size = int(min(width, height) * 0.38)
        avatar = await self._load_avatar(app, user, avatar_size)

        cx, cy = int(width * 0.74), int(height * 0.50)
        bg.paste(avatar, (cx - avatar_size // 2, cy - avatar_size // 2), avatar)

        draw = ImageDraw.Draw(bg)
        name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Unknown"
        username = f"@{user.username}" if user.username else "-"
        max_width = int(width * 0.55)

        name = self._fit_text(draw, name, self.font_body, max_width)
        username = self._fit_text(draw, username, self.font_body, max_width)

        left_x = int(width * 0.17)
        name_y = int(height * 0.70)
        id_y = int(height * 0.80)
        user_y = int(height * 0.89)

        draw.text((left_x, name_y), name, font=self.font_body, fill=self.fill)
        draw.text((left_x, id_y), str(user.id), font=self.font_body, fill=self.fill)
        draw.text((left_x, user_y), username, font=self.font_body, fill=self.fill)

        output = f"cache/welcome_{user.id}.png"
        bg.save(output)
        return output
