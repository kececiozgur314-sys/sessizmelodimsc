# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import filters, types

from anony import app, lang
from anony.helpers import admin_check, utils


@app.on_message(filters.command(["totalmembers", "memberscount"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _totalmembers(_, m: types.Message):
    await utils.maybe_delete_command(m)
    count = await app.get_chat_members_count(m.chat.id)
    await m.reply_text(
        m.lang.get("members_count", "Total members: {0}").format(count)
    )
