# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import filters, types

from anony import anon, app, db, lang
from anony.helpers import can_manage_vc, utils


@app.on_message(filters.command(["replay", "again"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _replay(_, m: types.Message):
    await utils.maybe_delete_command(m)
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang.get("not_playing", "Nothing is playing."))
    await anon.replay(m.chat.id)
    await m.reply_text(
        m.lang.get("play_replayed", "Stream replayed by {0}").format(m.from_user.mention)
    )
