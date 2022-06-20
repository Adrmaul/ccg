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
import re
from typing import List

import anilist
from pyrogram import filters
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import InlineQuery, InlineQueryResultPhoto
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_inline_query(filters.regex(r"^!anime (?P<query>.+)"))
async def anime_inline(bot: Amime, inline_query: InlineQuery):
    query = inline_query.matches[0]["query"].strip()
    lang = inline_query._lang

    if query.startswith("!"):
        inline_query.continue_propagation()

    results: List[InlineQueryResultPhoto] = []

    async with anilist.AsyncClient() as client:
        search_results = await client.search(query, "anime", 15)
        while search_results is None:
            search_results = await client.search(query, "anime", 10)
            await asyncio.sleep(5)

        for result in search_results:
            anime = await client.get(result.id, "anime")

            if anime is None:
                continue

            photo: str = ""
            if hasattr(anime, "banner"):
                photo = anime.banner
            elif hasattr(anime, "cover"):
                if hasattr(anime.cover, "extra_large"):
                    photo = anime.cover.extra_large
                elif hasattr(anime.cover, "large"):
                    photo = anime.cover.large
                elif hasattr(anime.cover, "medium"):
                    photo = anime.cover.medium

            description: str = ""
            if hasattr(anime, "description"):
                description = anime.description
                description = re.sub(re.compile(r"<.*?>"), "", description)
                description = description[0:260] + "..."

            text = f"<b>{anime.title.romaji}</b>"

            keyboard = [
                [
                    (
                        lang.view_more_button,
                        f"https://t.me/{bot.me.username}/?start=menu_{anime.id}",
                        "url",
                    )
                ],
            ]

            results.append(
                InlineQueryResultPhoto(
                    photo_url=photo,
                    title=f"{anime.title.romaji} | {anime.format}",
                    description=description,
                    caption=text,
                    reply_markup=ikb(keyboard),
                )
            )

    if len(results) > 0:
        try:
            await inline_query.answer(
                results=results,
                is_gallery=True,
                cache_time=3,
            )
        except QueryIdInvalid:
            pass
