import asyncio
import re
import math
from typing import List

import anilist
from pyrogram import filters
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import InlineQuery, InlineQueryResultPhoto
from pyromod.helpers import ikb

from amime.amime import Amime
from amime.database import Episodes, Users
from typing import Union

from datetime import datetime
from time import time
from anilist.types import next_airing
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from pyromod.helpers import array_chunk, ikb

from amime.modules.favorites import get_favorite_button
from amime.modules.mylists import get_mylist_button
from amime.modules.notify import get_notify_button

@Amime.on_inline_query(filters.regex(r"^!a (?P<query>.+)"))
async def anime_inline(bot: Amime, inline_query: InlineQuery):
    query = inline_query.matches[0]["query"].strip()
    lang = inline_query._lang
    user = inline_query.from_user

    is_collaborator = await filters.sudo(bot, inline_query) or await filters.collaborator(bot, inline_query)

    user_db = await Users.get(id=user.id)
    language = user_db.language_anime


    #if query.startswith("!"):
        #inline_query.continue_propagation()

    results: List[InlineQueryResultPhoto] = []

    async with anilist.AsyncClient() as client:
        search_results = await client.search(query, "anime", 25)
        while search_results is None:
            search_results = await client.search(query, "anime", 10)
            await asyncio.sleep(5)

        for result in search_results:
            anime = await client.get(result.id, "anime")

            if anime is None:
                continue

            episodes = await Episodes.filter(anime=anime.id)
            episodes = sorted(episodes, key=lambda episode: episode.number)
            episodes = [*filter(lambda episode: len(episode.file_id) > 0, episodes)]
          

            #photo = f"https://img.anili.st/media/{anime.id}"
            
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

            
            if len(episodes) > 0 and hasattr(anime, "genres") and hasattr(anime.score, "average"):
                description = f"✅ Tersedia | {anime.episodes} Eps ({anime.format}) - 🌟 {anime.score.average}%"
                description += f"\n{', '.join(anime.genres)}"
                if not anime.status.lower() == "not_yet_released":
                    description += f"\n{anime.start_date.day if hasattr(anime.start_date, 'day') else 0}/{anime.start_date.month if hasattr(anime.start_date, 'month') else 0}/{anime.start_date.year if hasattr(anime.start_date, 'year') else 0}"
                if not anime.status.lower() in ["not_yet_released", "releasing"]:
                    description += f" s/d {anime.end_date.day if hasattr(anime.end_date, 'day') else 0}/{anime.end_date.month if hasattr(anime.end_date, 'month') else 0}/{anime.end_date.year if hasattr(anime.end_date, 'year') else 0}"

            if len(episodes) < 1 and hasattr(anime, "genres") and hasattr(anime.score, "average"):
                description = f"❌ Tidak Ada | {anime.episodes} Eps ({anime.format}) - 🌟 {anime.score.average}%"
                description += f"\n{', '.join(anime.genres)}"
                if not anime.status.lower() == "not_yet_released":
                    description += f"\n{anime.start_date.day if hasattr(anime.start_date, 'day') else 0}/{anime.start_date.month if hasattr(anime.start_date, 'month') else 0}/{anime.start_date.year if hasattr(anime.start_date, 'year') else 0}"
                if not anime.status.lower() in ["not_yet_released", "releasing"]:
                    description += f" s/d {anime.end_date.day if hasattr(anime.end_date, 'day') else 0}/{anime.end_date.month if hasattr(anime.end_date, 'month') else 0}/{anime.end_date.year if hasattr(anime.end_date, 'year') else 0}"        

            text = f"<b>{anime.title.romaji}</b>"
            text += f"\n<b>ID</b>: <code>{anime.id}</code> (<b>ANIME</b>)"

            
            keyboard = [
                [
                    (
                        lang.watch_button,
                        f"episodes {anime.id} 0 1",
                    ),
                    (lang.search_button, f"!a {anime.title.romaji}", "switch_inline_query_current_chat"),

                ]
            ]

            results.append(
                InlineQueryResultPhoto(
                    photo_url=photo,
                    title=f"{anime.title.romaji}",
                    description=description,
                    caption=text,
                    reply_markup=ikb(keyboard),
                )
            )

    if is_collaborator and len(results) > 0:
        try:
            await inline_query.answer(
                results=results,
                is_gallery=False,
                cache_time=3,
            )
        except QueryIdInvalid:
            pass

