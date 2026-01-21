# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import enums, filters, types

from anony import app, lang
from anony.helpers import admin_check, utils


@app.on_message(filters.command(["admins", "adminlist"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _admins(_, m: types.Message):
    await utils.maybe_delete_command(m)
    admins = []
    async for member in app.get_chat_members(
        m.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        if member.user.is_bot:
            continue
        admins.append(member.user.mention)
    if not admins:
        return await m.reply_text(m.lang.get("admins_empty", "No admins found."))
    text = m.lang.get("admins_list", "Admins:") + "\n" + "\n".join(admins)
    await m.reply_text(text)


@app.on_message(filters.command(["bots"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _bots(_, m: types.Message):
    await utils.maybe_delete_command(m)
    bots = []
    async for member in app.get_chat_members(
        m.chat.id, filter=enums.ChatMembersFilter.BOTS
    ):
        bots.append(member.user.mention)
    if not bots:
        return await m.reply_text(m.lang.get("bots_empty", "No bots found."))
    text = m.lang.get("bots_list", "Bots:") + "\n" + "\n".join(bots)
    await m.reply_text(text)
