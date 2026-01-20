# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import csv
from io import StringIO, BytesIO

from pyrogram import filters, types

from anony import app, lang
from anony.helpers import admin_check, utils


@app.on_message(filters.command(["user", "members"]) & filters.group & ~app.bl_users)
@lang.language()
@admin_check
async def _members(_, m: types.Message):
    await utils.maybe_delete_command(m)
    keyboard = types.InlineKeyboardMarkup(
        [
            [
                types.InlineKeyboardButton(
                    m.lang.get("members_csv", "CSV"), callback_data="members_format csv"
                ),
                types.InlineKeyboardButton(
                    m.lang.get("members_txt", "TXT"), callback_data="members_format txt"
                ),
            ]
        ]
    )
    await m.reply_text(
        m.lang.get("members_choose", "Which format do you want?"),
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex(r"^members_format") & ~app.bl_users)
@lang.language()
async def _members_cb(_, query: types.CallbackQuery):
    await query.answer()
    try:
        await query.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    format_choice = query.data.split()[-1].lower()
    processing = await query.message.reply_text(
        query.lang.get("members_collecting", "Collecting members...")
    )

    members = []
    async for member in app.get_chat_members(query.message.chat.id):
        user = member.user
        members.append(
            {
                "username": user.username or user.first_name,
                "userid": user.id,
            }
        )
        if len(members) % 100 == 0:
            try:
                await processing.edit_text(
                    query.lang.get("members_progress", "Collected {0} members...").format(
                        len(members)
                    )
                )
            except Exception:
                pass

    if format_choice == "csv":
        csv_text = StringIO()
        writer = csv.DictWriter(csv_text, fieldnames=["username", "userid"])
        writer.writeheader()
        for member in members:
            writer.writerow(member)
        data = csv_text.getvalue().encode("utf-8")
        file_name = "members.csv"
        caption = query.lang.get("members_csv_ready", "Members list (CSV).")
    else:
        text = "\n".join([f"{m['username']} - {m['userid']}" for m in members])
        data = text.encode("utf-8")
        file_name = "members.txt"
        caption = query.lang.get("members_txt_ready", "Members list (TXT).")

    file_bytes = BytesIO(data)
    file_bytes.seek(0)
    await app.send_document(
        chat_id=query.message.chat.id,
        document=file_bytes,
        caption=caption,
        file_name=file_name,
    )
    await processing.delete()
