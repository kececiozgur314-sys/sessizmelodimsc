# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import httpx
from pyrogram import filters, types

from anony import app, lang

BORED_API_URL = "https://apis.scrimba.com/bored/api/activity"


@app.on_message(filters.command(["bored"]) & ~app.bl_users)
@lang.language()
async def _bored(_, m: types.Message):
    try:
        async with httpx.AsyncClient(timeout=10.0) as http:
            response = await http.get(BORED_API_URL)
        if response.status_code != 200:
            return await m.reply_text(
                m.lang.get("bored_failed", "Failed to fetch activity.")
            )
        data = response.json()
        activity = data.get("activity")
        if activity:
            return await m.reply_text(
                m.lang.get("bored_ok", "Try this: {0}").format(activity)
            )
        return await m.reply_text(m.lang.get("bored_none", "No activity found."))
    except Exception:
        return await m.reply_text(m.lang.get("bored_failed", "Failed to fetch activity."))
