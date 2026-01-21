# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import asyncio

from pyrogram import enums, errors, filters, types

from anony import app, lang
from anony.helpers import admin_check, utils


@app.on_message(filters.command(["zombies"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _zombies(_, m: types.Message):
    await utils.maybe_delete_command(m)
    try:
        me = await app.get_chat_member(m.chat.id, "self")
        if me.status != enums.ChatMemberStatus.ADMINISTRATOR:
            return await m.reply_text(
                m.lang.get("zombie_need_admin", "I need admin rights to scan.")
            )
    except Exception:
        return await m.reply_text(
            m.lang.get("zombie_need_admin", "I need admin rights to scan.")
        )

    deleted_users = []
    async for member in app.get_chat_members(m.chat.id):
        if member.user and member.user.is_deleted:
            deleted_users.append(member.user.id)

    if not deleted_users:
        return await m.reply_text(m.lang.get("zombie_none", "No zombies found."))

    text = m.lang.get("zombie_found", "Found {0} deleted accounts.").format(
        len(deleted_users)
    )
    keyboard = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    m.lang.get("zombie_clean", "Clean"),
                    callback_data=f"zombie_clean {m.chat.id}",
                )
            ],
            [
                types.InlineKeyboardButton(
                    m.lang.get("close", "Close"),
                    callback_data="help close",
                )
            ],
        ]
    )
    await m.reply_text(text, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"^zombie_clean") & ~app.bl_users)
@lang.language()
async def _zombie_clean(_, query: types.CallbackQuery):
    await query.answer()
    chat_id = int(query.data.split()[-1])
    try:
        me = await app.get_chat_member(chat_id, "self")
        if me.status != enums.ChatMemberStatus.ADMINISTRATOR:
            return await query.message.reply_text(
                query.lang.get("zombie_need_admin", "I need admin rights to clean.")
            )
    except Exception:
        return await query.message.reply_text(
            query.lang.get("zombie_need_admin", "I need admin rights to clean.")
        )

    msg = await query.message.reply_text(
        query.lang.get("zombie_cleaning", "Cleaning deleted accounts...")
    )

    removed = 0
    async for member in app.get_chat_members(chat_id):
        if member.user and member.user.is_deleted:
            try:
                await app.ban_chat_member(chat_id, member.user.id)
                await app.unban_chat_member(chat_id, member.user.id)
                removed += 1
                await asyncio.sleep(0.2)
            except errors.FloodWait as fw:
                await asyncio.sleep(fw.value)
            except Exception:
                continue

    await msg.edit_text(
        query.lang.get("zombie_done", "Removed {0} deleted accounts.").format(removed)
    )
