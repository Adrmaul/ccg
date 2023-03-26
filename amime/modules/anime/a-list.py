# MIT License
#
# Copyright (c) 2021 Andriel Rodrigues for Amano Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
import anilist
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyromod.helpers import ikb
from pyromod.nav import Pagination
from aiocache import cached, SimpleMemoryCache

from amime.amime import Amime
from amime.database import A_lists


async def fetch_anime_data(anime_ids):
    async with anilist.AsyncClient() as client:
        tasks = [client.get(anime_id, "anime") for anime_id in anime_ids]
        return await asyncio.gather(*tasks)


@cached(ttl=3600, cache=SimpleMemoryCache, key="a_lists_cache")
async def get_a_lists():
    a_lists = await A_lists.filter(type="anime")
    return a_lists


@Amime.on_callback_query(filters.regex(r"a_lists anime (?P<page>\d+)"))
async def anime_a_lists(bot: Amime, callback: CallbackQuery):
    page = int(callback.matches[0]["page"])

    message = callback.message
    user = callback.from_user
    lang = callback._lang

    keyboard = []

    a_lists = await get_a_lists()
    anime_ids = [a_list.item for a_list in a_lists]
    anime_data = await fetch_anime_data(anime_ids)

    results = list(zip(a_lists, anime_data))

    layout = Pagination(
        results,
        item_data=lambda i, pg: f"menu {i[0].item}",
        item_title=lambda i, pg: i[1].title.romaji,
        page_data=lambda pg: f"a_lists anime {pg}",
    )

    lines = layout.create(page, lines=8)

    if len(lines) > 0:
        keyboard += lines

    keyboard.append([(lang.back_button, "listsx")])

    await message.edit_text(
        lang.a_lists_list_title,
        reply_markup=ikb(keyboard),
    )
