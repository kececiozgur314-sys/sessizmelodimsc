# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import filters, types

from anony import app, lang
from anony.helpers import admin_check, utils


@app.on_message(
    filters.command(["ban", "unban"]) & filters.group & ~app.bl_users
)
@lang.language()
@admin_check
async def _ban(_, m: types.Message):
    await utils.maybe_delete_command(m)
    user = await utils.extract_user(m)
    if not user:
        return await m.reply_text(m.lang.get("user_not_found", "User not found."))

    if m.command[0] == "ban":
        try:
            await app.ban_chat_member(m.chat.id, user.id)
            return await m.reply_text(
                m.lang.get("ban_success", "User banned: {0}").format(user.mention)
            )
        except Exception:
            return await m.reply_text(
                m.lang.get("ban_failed", "I couldn't ban that user.")
            )

    try:
        await app.unban_chat_member(m.chat.id, user.id)
        return await m.reply_text(
            m.lang.get("unban_success", "User unbanned: {0}").format(user.mention)
        )
    except Exception:
        return await m.reply_text(
            m.lang.get("unban_failed", "I couldn't unban that user.")
        )


@app.on_message(
    filters.command(["mute", "unmute"]) & filters.group & ~app.bl_users
)
@lang.language()
@admin_check
async def _mute(_, m: types.Message):
    await utils.maybe_delete_command(m)
    user = await utils.extract_user(m)
    if not user:
        return await m.reply_text(m.lang.get("user_not_found", "User not found."))

    if m.command[0] == "mute":
        try:
            await app.restrict_chat_member(
                m.chat.id,
                user.id,
                permissions=types.ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                ),
            )
            return await m.reply_text(
                m.lang.get("mute_success", "User muted: {0}").format(user.mention)
            )
        except Exception:
            return await m.reply_text(
                m.lang.get("mute_failed", "I couldn't mute that user.")
            )

    try:
        await app.restrict_chat_member(
            m.chat.id,
            user.id,
            permissions=types.ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
            ),
        )
        return await m.reply_text(
            m.lang.get("unmute_success", "User unmuted: {0}").format(user.mention)
        )
    except Exception:
        return await m.reply_text(
            m.lang.get("unmute_failed", "I couldn't unmute that user.")
        )
