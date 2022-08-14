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


@Amime.on_message(filters.cmd(r"media_login (.+)"))
@Amime.on_callback_query(filters.regex(r"^media_login (\d+)\s?(\d+)?\s?(\d+)?"))
async def anime_view(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    chat = message.chat
    user = union.from_user
    lang = union._lang

    is_private = await filters.private(bot, message)
    is_collaborator = await filters.collaborator(bot, union) or await filters.sudo(
        bot, union
    )

    query = union.matches[0].group(1)

    if is_callback:
        user_id = union.matches[0].group(2)
        if user_id is not None:
            user_id = int(user_id)

            if user_id != user.id:
                return

        to_delete = union.matches[0].group(3)
        if bool(to_delete) and not is_private:
            await message.delete()

    if not bool(query):
        return

    async with anilist.AsyncClient() as client:
        if not query.isdecimal():
            results = await client.search(query, "anime", 15)
            if results is None:
                await asyncio.sleep(0.5)
                results = await client.search(query, "anime", 10)

            if results is None:
                return

            if len(results) == 1:
                anime_id = results[0].id
            else:
                keyboard = []
                for result in results:
                    keyboard.append(
                        [(result.title.romaji, f"media_login {result.id} {user.id} 1")]
                    )
                await message.reply_text(
                    lang.search_results_text(
                        query=query,
                    ),
                    reply_markup=ikb(keyboard),
                )
                return
        else:
            anime_id = int(query)

        anime = await client.get(anime_id, "anime")

        if anime is None:
            return

        user_db = await Users.get(id=user.id)
        language = user_db.language_anime

        episodes = await Episodes.filter(anime=anime.id)
        episodes1 = await Episodes.filter(anime=anime_id, language=language)
        episodes = sorted(episodes, key=lambda episode: episode.number)
        episodes = [*filter(lambda episode: len(episode.file_id) > 0, episodes)]

        
        if len(episodes) > 0 and anime.status.lower() == "releasing":
            air_on = make_it_rw(anime.next_airing.time_until*1000)
            text = f"<b>{anime.title.romaji}</b> (<b>{anime.title.native}</b>) | ✅ ({len(episodes1)}) List Episode Tersedia untuk ditonton."
            if hasattr(anime.next_airing, "time_until") and air_on:
                text += f"\n\nℹ️ Episode ({anime.next_airing.episode}) akan rilis dalam {air_on}"
        if len(episodes) > 0 and not anime.status.lower() == "releasing":
            text = f"✅ List Episode Tersedia untuk ditonton. - <code>{anime.title.romaji}"
        if len(episodes) < 1 :
            text = f"\n\n❌ Belum tersedia. - <code>{anime.title.romaji}"
            if hasattr(anime.title, "native"):
                text += f" (<b>{anime.title.native}</b>)"
            text += f"\nCek progres: <a href='https://t.me/otakuindonew/49696'>Disini</a></b>"
        buttons = [
            (lang.menu_login, f"settings_login {anime_id}")       
        ]
         

        if len(episodes) > 0:
            if is_private:
                buttons.append(
                    (
                        lang.watch_button,
                        f"episodes1 {anime.id} {episodes[0].season} 1",
                    )
                )
        
        if len(episodes) < 1 and is_private:
            buttons.append((lang.inline, f"{anime.title.romaji}", "switch_inline_query_current_chat"))    

       
        buttons.append(
                (
                    lang.Hapus_text, 
                    f"close_data"
                ),
            )
        
        if is_private:       
            buttons.append(
                    (lang.back_button, f"btn_{anime_id}_True_{user.id}")
                )

        keyboard = array_chunk(buttons, 2)

        if is_collaborator:
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
                    
        if not is_collaborator:
            photo = f"https://img.anili.st/media/{anime.id}"

        if bool(message.video) and is_callback:
            await union.edit_message_media(
                InputMediaPhoto(
                    photo,
                    caption=text,
                ),
                reply_markup=ikb(keyboard),
            )
        elif bool(message.photo) and not bool(message.via_bot):
            await message.edit_text(
                text,
                reply_markup=ikb(keyboard),
            )
        else:
            await message.reply_photo(
                photo,
                caption=text,
                reply_markup=ikb(keyboard),
            )