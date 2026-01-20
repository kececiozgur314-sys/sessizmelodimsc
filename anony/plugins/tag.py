# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import asyncio

from pyrogram import filters, types

from anony import app, lang
from anony.helpers import admin_check, utils


@app.on_message(filters.command(["tag", "tagall", "etiket"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _tag_all(_, m: types.Message):
    await utils.maybe_delete_command(m)
    text = None
    if m.reply_to_message:
        text = m.reply_to_message.text or m.reply_to_message.caption
    if len(m.command) > 1:
        text = " ".join(m.command[1:])
    if not text:
        return await m.reply_text(m.lang.get("tag_usage", "Usage: /tag <text>"))

    await m.reply_text(m.lang.get("tag_start", "Tagging members..."))

    mentions = []
    count = 0
    async for member in app.get_chat_members(m.chat.id):
        if member.user.is_bot:
            continue
        mentions.append(member.user.mention)
        if len(mentions) == 5:
            await app.send_message(
                chat_id=m.chat.id,
                text=f"{text}\n\n" + " ".join(mentions),
                disable_web_page_preview=True,
            )
            mentions.clear()
            count += 5
            await asyncio.sleep(1.2)

    if mentions:
        await app.send_message(
            chat_id=m.chat.id,
            text=f"{text}\n\n" + " ".join(mentions),
            disable_web_page_preview=True,
        )
        count += len(mentions)

    await m.reply_text(m.lang.get("tag_done", "Tagged {0} members.").format(count))
