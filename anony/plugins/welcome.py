# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import enums, filters, types

from anony import app, config, db, lang
from anony.helpers import admin_check, utils, welcome


@app.on_message(
    filters.command(["welcome", "hosgeldin", "hoşgeldin"])
    & filters.group
    & ~app.bl_users
)
@lang.language()
@admin_check
async def _welcome_toggle(_, m: types.Message):
    await utils.maybe_delete_command(m)
    if len(m.command) < 2:
        return await m.reply_text(
            m.lang.get("welcome_usage", "Usage: /welcome on | off")
        )

    arg = m.command[1].lower()
    enable = arg in ["on", "enable", "ac", "aç", "aktif"]
    disable = arg in ["off", "disable", "kapat", "pasif"]
    if enable:
        await db.set_welcome(m.chat.id, True)
        return await m.reply_text(
            m.lang.get("welcome_on", "Welcome messages enabled.")
        )
    if disable:
        await db.set_welcome(m.chat.id, False)
        return await m.reply_text(
            m.lang.get("welcome_off", "Welcome messages disabled.")
        )

    return await m.reply_text(
        m.lang.get("welcome_usage", "Usage: /welcome on | off")
    )


@app.on_message(filters.new_chat_members, group=8)
@lang.language()
async def _welcome_new_member(_, m: types.Message):
    if m.chat.type != enums.ChatType.SUPERGROUP:
        return
    if not await db.get_welcome(m.chat.id):
        return

    for user in m.new_chat_members:
        if user.is_bot:
            continue

        image_path = await welcome.generate(app, user, config.WELCOME_IMG)
        caption = m.lang.get(
            "welcome_caption",
            "Hoş geldin {name}! 👋",
        ).format(
            name=user.mention,
            chat=m.chat.title,
        )

        if image_path:
            await app.send_photo(
                chat_id=m.chat.id,
                photo=image_path,
                caption=caption,
            )
        else:
            await app.send_message(chat_id=m.chat.id, text=caption)
