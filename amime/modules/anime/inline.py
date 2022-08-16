import asyncio
import re
from typing import List
from datetime import datetime
from time import time
import math
from typing import Union

import anilist
from anilist.types import next_airing
from pyrogram import filters
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import InlineQuery, InlineQueryResultPhoto
from pyromod.helpers import ikb

from amime.amime import Amime
from amime.database import Episodes

from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from pyromod.helpers import array_chunk, ikb

from amime.database import Episodes, Users
from amime.modules.favorites import get_favorite_button
from amime.modules.mylists import get_mylist_button
from amime.modules.notify import get_notify_button



def make_it_rw(time_stamp):
    """Converting Time Stamp to Readable Format"""
    seconds, milliseconds = divmod(int(time_stamp), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " Hari, ") if days else "")
        + ((str(hours) + " Jam, ") if hours else "")
        + ((str(minutes) + " Menit, ") if minutes else "")
        + ((str(seconds) + " Detik, ") if seconds else "")
        + ((str(milliseconds) + " ms, ") if milliseconds else "")
    )
    return tmp[:-2]

@Amime.on_inline_query(filters.regex(r"^!a (?P<query>.+)"))
async def anime_inline(bot: Amime, inline_query: InlineQuery):
    query = inline_query.matches[0]["query"].strip()
    lang = inline_query._lang
    user = inline_query.from_user


    is_collaborator = await filters.sudo(bot, inline_query) or await filters.collaborator(bot, inline_query)


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

            user_db = await Users.get(id=user.id)
            language = user_db.language_anime

            episodes = await Episodes.filter(anime=anime.id, language=language)
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

            #Full
            if len(episodes) > 0 and anime.status.lower() == "releasing" and hasattr(anime, "genres") and hasattr(anime.score, "average"):
                description = f"✅ Tersedia ({len(episodes)}) Eps - {anime.episodes} Eps | ({anime.format}) - 🌟 {anime.score.average}%"
                air_on = make_it_rw(anime.next_airing.time_until*1000)
                if hasattr(anime.next_airing, "time_until") and air_on:
                    description += f"\nNext Eps ({anime.next_airing.episode}) : {air_on}"
                description += f"\n{', '.join(anime.genres)}"
            
            if len(episodes) > 0 and not anime.status.lower() == "releasing" and hasattr(anime, "genres") and hasattr(anime.score, "average"):
                description = f"✅ Tersedia ({len(episodes)}) Eps - {anime.episodes} Eps | ({anime.format}) - 🌟 {anime.score.average}%"
                description += f"\n{', '.join(anime.genres)}"

            if len(episodes) < 1 and hasattr(anime, "genres") and hasattr(anime.score, "average"):
                description = f"❌ Tidak Ada | {anime.episodes} Eps | ({anime.format}) - 🌟 {anime.score.average}%"
                description += f"\n{', '.join(anime.genres)}"
                if not anime.status.lower() == "not_yet_released":
                    description += f"\n{anime.start_date.day if hasattr(anime.start_date, 'day') else 0}/{anime.start_date.month if hasattr(anime.start_date, 'month') else 0}/{anime.start_date.year if hasattr(anime.start_date, 'year') else 0}"
                if not anime.status.lower() in ["not_yet_released", "releasing"]:
                    description += f" s/d {anime.end_date.day if hasattr(anime.end_date, 'day') else 0}/{anime.end_date.month if hasattr(anime.end_date, 'month') else 0}/{anime.end_date.year if hasattr(anime.end_date, 'year') else 0}"        

            #Tidak Full
            if len(episodes) > 0 and anime.status.lower() == "releasing" and not hasattr(anime, "genres") and not hasattr(anime.score, "average"):
                description = f"✅ Tersedia ({len(episodes)}) Eps - {anime.episodes} Eps | ({anime.format})"
                air_on = make_it_rw(anime.next_airing.time_until*1000)
                if hasattr(anime.next_airing, "time_until") and air_on:
                    description += f"\nNext Eps ({anime.next_airing.episode}) : {air_on}"
            
            if len(episodes) > 0 and not anime.status.lower() == "releasing" and not hasattr(anime, "genres") and not hasattr(anime.score, "average"):
                description = f"✅ Tersedia ({len(episodes)}) Eps - {anime.episodes} Eps | ({anime.format})"

            if len(episodes) < 1 and not hasattr(anime, "genres") and not hasattr(anime.score, "average"):
                description = f"❌ Tidak Ada | {anime.episodes} Eps | ({anime.format})"
                if not anime.status.lower() == "not_yet_released":
                    description += f"\n{anime.start_date.day if hasattr(anime.start_date, 'day') else 0}/{anime.start_date.month if hasattr(anime.start_date, 'month') else 0}/{anime.start_date.year if hasattr(anime.start_date, 'year') else 0}"
                if not anime.status.lower() in ["not_yet_released", "releasing"]:
                    description += f" s/d {anime.end_date.day if hasattr(anime.end_date, 'day') else 0}/{anime.end_date.month if hasattr(anime.end_date, 'month') else 0}/{anime.end_date.year if hasattr(anime.end_date, 'year') else 0}"        


            text = f"<b>{anime.title.romaji}</b>"
            text += f"\n<b>ID</b>: <code>{anime.id}</code> (<b>ANIME</b>)"

            keyboard = [
                [
                    (
                        lang.view_more_button,
                        f"https://t.me/{bot.me.username}/?start=anime_{anime.id}",
                        "url",
                    ),
                    (lang.search_button, f"{anime.title.romaji}", "switch_inline_query_current_chat"),

                ],
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

