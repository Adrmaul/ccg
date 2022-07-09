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
from pyrogram import filters
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from pyromod.helpers import array_chunk, ikb

from amime.amime import Amime
from amime.database import Episodes, Users
from amime.modules.favorites import get_favorite_button
from amime.modules.mylists import get_mylist_button
from amime.modules.notify import get_notify_button



@Amime.on_callback_query(filters.regex(r"^settings_login (\d+)\s?(\d+)?\s?(\d+)?"))
async def anime_view(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    chat = message.chat
    user = union.from_user
    lang = union._lang

    is_private = await filters.private(bot, message)
    is_collaborator = await filters.sudo(bot, union)

    is_auth = await filters.collaborator(bot, union)

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
            results = await client.search(query, "anime", 10)
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
                        [(result.title.romaji, f"anime {result.id} {user.id} 1")]
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
        episodes = sorted(episodes, key=lambda episode: episode.number)
        episodes = [*filter(lambda episode: len(episode.file_id) > 0, episodes)]

        text = f"Silahkan untuk pilih tombol yang tersedia."
        if anime.status.lower() == "not_yet_released":
            text += f"\n⋟ Informasi terkait anime ini : <b>{lang.status}</b>: <code>{anime.status}" 

        buttons = [
            (
                        lang.Hapus_text, 
                        f"neko_delete, {user.id}"
                    ),       
        ]

        if is_collaborator:
            buttons.append(
                (
                    lang.manage_button,
                    f"manage1 anime {anime.id} 0 1 {language} 1",
                )
            )

        if is_auth and not anime.status.lower() == "not_yet_released":
            buttons.append(
                (
                    lang.manage_user_button,
                    f"manage_user anime {anime.id} 0 1 {language} 1",
                )
            ) 

        if not is_auth and not is_collaborator and not anime.status.lower() == "not_yet_released" and anime.status.lower() == "releasing":
            buttons.append(
                (
                    lang.manage_user_button,
                    f"manage_user anime {anime.id} 0 1 {language} 1",
                )
            )       


        if is_private:
            buttons.append(await get_favorite_button(lang, user, "anime", anime.id))
        
        if is_private:
            buttons.append(await get_mylist_button(lang, user, "anime", anime.id))
        
        if is_private:
            buttons.append(
                await get_notify_button(
                    lang, user if is_private else chat, "anime", anime.id
                )
            )

        if is_private and not anime.status.lower() == "not_yet_released":
            button = (
                lang.request_content_button,
                f"request1 episodes {anime.id} {language}",
            )
            if anime.status.lower() == "releasing":
                if hasattr(anime, "next_airing"):
                    next_episode = anime.next_airing.episode
                    if len(episodes) < (next_episode - 1):
                        buttons.append(button)
                else:
                    buttons.append(button)
            elif hasattr(anime, "episodes"):
                if len(episodes) < anime.episodes:
                    buttons.append(button)
        

        if is_private and len(episodes) > 0:
            buttons.append(
                (
                    lang.back_button,
                    f"episodes1 {anime.id} {episodes[0].season} 1",
                )
            )

        if is_private and len(episodes) < 1:
            buttons.append(
                (
                    lang.back_button,
                    f"btn_{anime.id}_True_{user.id}",
                )
            ) 

        keyboard = array_chunk(buttons, 2)

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