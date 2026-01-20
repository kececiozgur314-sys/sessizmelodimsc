# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import filters, types

from anony import app, db, lang, queue
from anony.helpers import can_manage_vc, utils


@app.on_message(filters.command(["shuffle", "cshuffle"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _shuffle(_, m: types.Message):
    await utils.maybe_delete_command(m)
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang.get("not_playing", "Nothing is playing."))
    if not queue.shuffle(m.chat.id):
        return await m.reply_text(m.lang.get("shuffle_empty", "Queue is too short to shuffle."))
    await m.reply_text(
        m.lang.get("shuffle_done", "Queue shuffled by {0}.").format(m.from_user.mention)
    )
