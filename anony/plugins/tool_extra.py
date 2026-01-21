# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import time

from pyrogram import filters, types

from anony import __version__, app, boot, db, lang
from anony.helpers import utils


@app.on_message(filters.command(["uptime"]) & ~app.bl_users)
@lang.language()
async def _uptime(_, m: types.Message):
    up = utils.format_eta(int(time.time() - boot))
    await m.reply_text(m.lang.get("uptime_text", "Uptime: {0}").format(up))


@app.on_message(filters.command(["botinfo", "info_bot"]) & ~app.bl_users)
@lang.language()
async def _botinfo(_, m: types.Message):
    users = len(await db.get_users())
    chats = len(await db.get_chats())
    text = m.lang.get(
        "botinfo_text",
        "Bot: {0}\nVersion: {1}\nUsers: {2}\nChats: {3}",
    ).format(app.name, __version__, users, chats)
    await m.reply_text(text)
