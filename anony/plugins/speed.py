# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import filters, types

from anony import anon, app, db, lang, queue
from anony.helpers import can_manage_vc, utils


def _speed_markup(chat_id: int) -> types.InlineKeyboardMarkup:
    speeds = ["0.75", "1.0", "1.25", "1.5", "2.0"]
    row = [
        types.InlineKeyboardButton(
            text=f"{s}x", callback_data=f"speed {chat_id} {s}"
        )
        for s in speeds
    ]
    return types.InlineKeyboardMarkup([row])


@app.on_message(
    filters.command(["speed", "cspeed", "slow", "cslow", "playback", "cplayback"])
    & filters.group
    & ~app.bl_users
)
@lang.language()
@can_manage_vc
async def _speed(_, m: types.Message):
    await utils.maybe_delete_command(m)
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang.get("not_playing", "Nothing is playing."))
    media = queue.get_current(m.chat.id)
    if not media or not media.file_path or "downloads" not in media.file_path:
        return await m.reply_text(
            m.lang.get("speed_unsupported", "Speed control is only for downloaded tracks.")
        )
    await m.reply_text(
        m.lang.get("speed_panel", "Select a playback speed:"),
        reply_markup=_speed_markup(m.chat.id),
    )


@app.on_callback_query(filters.regex(r"^speed ") & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _speed_cb(_, query: types.CallbackQuery):
    _, chat_id, speed = query.data.split()
    chat_id = int(chat_id)
    await query.answer()

    if not await db.get_call(chat_id):
        return await query.answer(query.lang.get("not_playing", "Nothing is playing."), show_alert=True)

    media = queue.get_current(chat_id)
    if not media or not media.file_path or "downloads" not in media.file_path:
        return await query.answer(
            query.lang.get("speed_unsupported", "Speed control is only for downloaded tracks."),
            show_alert=True,
        )

    await query.edit_message_text(
        query.lang.get("speed_changing", "Changing speed...")
    )
    try:
        await anon.play_media(chat_id, query.message, media, media.time)
        await query.edit_message_text(
            query.lang.get("speed_changed", "Speed set to {0}x by {1}.").format(
                speed, query.from_user.mention
            )
        )
    except Exception:
        await query.edit_message_text(
            query.lang.get("speed_failed", "Failed to change speed.")
        )
