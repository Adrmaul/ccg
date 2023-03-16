import asyncio
import math
from typing import Union

import anilist
from datetime import datetime
from time import time
from anilist.types import next_airing
from pyrogram import filters
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from pyromod.helpers import array_chunk, ikb

from amime.amime import Amime
from amime.database import Episodes, Users
from amime.modules.favorites import get_favorite_button
from amime.modules.mylists import get_mylist_button
from amime.modules.notify import get_notify_button

@Amime.on_callback_query(filters.regex(r"^ngelist dong (\d+) (\d+)"))
async def anime_view_more(bot: Amime, callback: CallbackQuery):
    message = callback.message
    user = callback.from_user
    lang = callback._lang

    anime_id = int(callback.matches[0].group(1))
    user_id = int(callback.matches[0].group(2))

    if user_id != user.id:
        return

    async with anilist.AsyncClient() as client:
        anime = await client.get(anime_id, "anime")

        buttons.append(await get_mylist_button(lang, user.id, "anime", anime.id)),

        keyboard.append([(lang.back_button, f"menu {anime_id} {user_id}")])

        await message.edit_text(
            lang.view_more_text,
            reply_markup=ikb(keyboard),
        )