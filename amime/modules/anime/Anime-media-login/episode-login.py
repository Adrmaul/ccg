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

import math

from pyrogram import filters
from pyrogram.types import CallbackQuery, InputMediaPhoto
from pyromod.helpers import array_chunk, ikb
from pyromod.nav import Pagination
import anilist

from amime.amime import Amime
from amime.database import Episodes, Users, Viewed, Watched

from pyrogram.types import CallbackQuery, InputMediaPhoto, Message


@Amime.on_callback_query(filters.regex(r"^episodes1 (\d+) (\d+) (\d+)"))
async def anime_episodes(bot: Amime, callback: CallbackQuery):
    message = callback.message
    user = callback.from_user
    lang = callback._lang

    anime_id = int(callback.matches[0].group(1))
    season = int(callback.matches[0].group(2))
    page = int(callback.matches[0].group(3))

    user_db = await Users.get(id=user.id)
    language = user_db.language_anime
    subtitled = user_db.subtitled_anime

    is_admin = bot.is_sudo(user)
    

    is_auth = await filters.collaborator(bot)

    episodes = await Episodes.filter(added_by=user.id)

    async with anilist.AsyncClient() as client:
        anime = await client.get(anime_id, "anime")

    buttons = [
        (
            f"{lang.language_button}: {lang.strings[language]['LANGUAGE_NAME']}",
            f"episodes1 language {anime_id} {season} {language} {page}",
        ),
    ]

    if season > 0:
        buttons.append(
            (
                f"{lang.season_button}: {season}",
                f"episodes1 season {anime_id} {season} {page}",
            )
        )

    buttons.append(
        (
            f"{lang.subtitled_button}: {lang.yes if subtitled else lang.no}",
            f"episodes1 subtitled {anime_id} {season} {page}",
        )
    )

    if not is_auth and not is_admin:
        buttons.append(
            (
                lang.order_button,
                f"http://t.me/akuiiki",
                "url",
            )
        )

    if is_auth and is_admin:
        buttons.append((lang.inline, f"{anime.title.romaji}", "switch_inline_query_current_chat"))

    keyboard = array_chunk(buttons, 2)

    episodes = await Episodes.filter(
        anime=anime_id, season=season, language=language, subtitled=subtitled
    )
    episodes = sorted(episodes, key=lambda episode: episode.number)
    episodes = [*filter(lambda episode: len(episode.file_id) > 0, episodes)]

    for index, episode in enumerate(
        sorted(episodes, key=lambda episode: episode.number, reverse=True)
    ):
        if await Watched.get_or_none(user=user.id, episode=episode.id) is not None:
            episode = episodes[-index]

            if index == 0:
                break

            if math.ceil(episode.number / (5 * 3)) != page:
                keyboard.append(
                    [
                        (
                            f"{lang.next_episode_button}: {lang.episode[0]}{episode.number}",
                            f"episode1 {anime_id} {episode.season} {episode.number}",
                        )
                    ]
                )
            break

    episodes_list = []
    for episode in episodes:
        viewed = bool(await Viewed.get_or_none(user=user.id, item=episode.id))
        watched = bool(await Watched.get_or_none(user=user.id, episode=episode.id))
        episodes_list.append((episode, viewed, watched))

    if is_auth and is_admin:
        layout = Pagination(
            episodes_list,
            item_data=lambda i, pg: f"episode1 {i[0].anime} {i[0].season} {i[0].number}",
            item_title=lambda i, pg: ("✅" if i[2] else "👁️" if i[1] else "")
            + f" {i[0].number}"
            + (f"-{i[0].unified_until}" if i[0].unified_until > 0 else ""),
            page_data=lambda pg: f"episode1 {anime_id} {season} {pg}",
        )

        lines = layout.create(page, lines=4, columns=3)
        if len(lines) > 0:
            keyboard += lines
    

    keyboard.append([
        (lang.back_button, f"media_login {anime_id}")])

    anime = await client.get(anime_id, "anime")
    
    if anime is None:
        return

    if is_auth and is_admin:
        text = f"<b>{anime.title.romaji}</b> (<code>{anime.title.native}</code>)"

    if not is_auth and not is_admin:
        text = f"[Beta] - Anda adalah trial user. Fitur ini nantinya hanya untuk user premium."
        text += f"\nUntuk lebih lanjutnya, silahkan buka tautan ini: <b><a href='http://telegra.ph/Premium---ccgnimex-06-23'>Premium</a></b>"

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

    await callback.edit_message_media(
        InputMediaPhoto(
            photo,
            caption=text,
        ),
        reply_markup=ikb(keyboard),
    )


@Amime.on_callback_query(filters.regex(r"^episodes1 season (\d+) (\d+) (\d+)"))
async def episodes_season(bot: Amime, callback: CallbackQuery):
    message = callback.message
    chat = message.chat
    user = callback.from_user
    lang = callback._lang

    anime_id = int(callback.matches[0].group(1))
    season = int(callback.matches[0].group(2))
    page = int(callback.matches[0].group(3))

    user_db = await Users.get(id=user.id)
    language = user_db.language_anime

    episodes = await Episodes.filter(anime=anime_id, language=language)
    episodes = sorted(episodes, key=lambda episode: episode.number)

    seasons = []
    for episode in episodes:
        if episode.season not in seasons:
            seasons.append(episode.season)

    seasons.sort()

    buttons = []
    for _season in seasons:
        text = ("✅" if _season == season else "") + f" {_season}"
        data = (
            "noop" if _season == season else f"episodes1 season {anime_id} {_season} 1"
        )
        buttons.append((text, data))

    keyboard = array_chunk(buttons, 2)

    keyboard.append([(lang.back_button, f"episodes1 {anime_id} {season} {page}")])

    await message.edit_text(
        lang.season_text,
        reply_markup=ikb(keyboard),
    )


@Amime.on_callback_query(filters.regex(r"^episodes1 subtitled (\d+) (\d+) (\d+)"))
async def episodes_subtitled(bot: Amime, callback: CallbackQuery):
    message = callback.message
    chat = message.chat
    user = callback.from_user
    lang = callback._lang

    user_db = await Users.get(id=user.id)
    user_db.update_from_dict({"subtitled_anime": not user_db.subtitled_anime})
    await user_db.save()

    await anime_episodes(bot, callback)
