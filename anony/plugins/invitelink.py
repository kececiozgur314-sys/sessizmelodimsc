# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import os

from pyrogram import errors, filters, types

from anony import app, lang
from anony.helpers import admin_check, utils


@app.on_message(filters.command(["givelink"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _givelink(_, m: types.Message):
    await utils.maybe_delete_command(m)
    try:
        link = await app.export_chat_invite_link(m.chat.id)
        await m.reply_text(
            m.lang.get("givelink_done", "Invite link for {0}:\n{1}").format(
                m.chat.title, link
            )
        )
    except Exception:
        await m.reply_text(m.lang.get("givelink_failed", "Failed to generate invite link."))


@app.on_message(filters.command(["link", "invitelink"]) & ~app.bl_users)
@lang.language()
async def _link(_, m: types.Message):
    if m.from_user.id not in app.sudoers:
        return await m.reply_text(m.lang.get("sudo_only", "This command is only for sudo users."))
    if len(m.command) != 2:
        return await m.reply_text(m.lang.get("link_usage", "Usage: /link <group_id>"))

    try:
        group_id = int(m.command[1])
    except ValueError:
        return await m.reply_text(m.lang.get("link_invalid", "Invalid group id."))

    file_name = f"group_info_{group_id}.txt"
    try:
        chat = await app.get_chat(group_id)
        try:
            invite_link = await app.export_chat_invite_link(chat.id)
        except (errors.ChannelInvalid, errors.ChannelPrivate):
            return await m.reply_text(
                m.lang.get("link_no_access", "I don't have access to that chat.")
            )
        group_data = {
            "id": chat.id,
            "type": str(chat.type),
            "title": chat.title,
            "members_count": chat.members_count,
            "description": chat.description,
            "invite_link": invite_link,
            "is_verified": chat.is_verified,
            "is_restricted": chat.is_restricted,
            "is_creator": chat.is_creator,
            "is_scam": chat.is_scam,
            "is_fake": chat.is_fake,
            "dc_id": chat.dc_id,
            "has_protected_content": chat.has_protected_content,
        }
        with open(file_name, "w", encoding="utf-8") as file:
            for key, value in group_data.items():
                file.write(f"{key}: {value}\n")
        await app.send_document(
            chat_id=m.chat.id,
            document=file_name,
            caption=m.lang.get("link_ready", "Group info for {0}").format(chat.title),
        )
    except Exception:
        await m.reply_text(m.lang.get("link_failed", "Failed to fetch group info."))
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
