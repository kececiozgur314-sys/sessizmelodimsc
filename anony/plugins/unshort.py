# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import httpx
import pyshorteners
from pyrogram import filters, types

from anony import app, lang

shortener = pyshorteners.Shortener()


@app.on_message(filters.command(["short"]) & ~app.bl_users)
@lang.language()
async def _short(_, m: types.Message):
    if len(m.command) < 2:
        return await m.reply_text(
            m.lang.get("short_usage", "Usage: /short https://example.com")
        )
    link = m.command[1]
    try:
        tiny = shortener.tinyurl.short(link)
        dagd = shortener.dagd.short(link)
        clck = shortener.clckru.short(link)
        markup = types.InlineKeyboardMarkup(
            [
                [types.InlineKeyboardButton("🔗 TinyURL", url=tiny)],
                [
                    types.InlineKeyboardButton("🔗 Dagd", url=dagd),
                    types.InlineKeyboardButton("🔗 Clck.ru", url=clck),
                ],
            ]
        )
        await m.reply_text(
            m.lang.get("short_done", "Here are your shortened URLs:"),
            reply_markup=markup,
        )
    except Exception:
        await m.reply_text(m.lang.get("short_failed", "Failed to shorten the link."))


@app.on_message(filters.command(["unshort"]) & ~app.bl_users)
@lang.language()
async def _unshort(_, m: types.Message):
    if len(m.command) < 2:
        return await m.reply_text(
            m.lang.get("unshort_usage", "Usage: /unshort https://bit.ly/example")
        )
    short_link = m.command[1]
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            response = await client.get(short_link)
            final_url = str(response.url)
        markup = types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("🔗 View Final URL", url=final_url)]]
        )
        await m.reply_text(
            m.lang.get("unshort_done", "Final URL:\n{0}").format(final_url),
            reply_markup=markup,
        )
    except Exception:
        await m.reply_text(m.lang.get("unshort_failed", "Failed to unshorten the link."))
