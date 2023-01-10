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
from typing import Tuple

import anilist
from pyrogram import filters
from pyrogram.types import CallbackQuery, InputMediaVideo, User
from pyromod.helpers import bki, ikb

from amime.amime import Amime
from amime.database import Episodes, Users, Viewed, Watched


@Amime.on_callback_query(filters.regex(r"^episode_global (\d+) (\d+) (\d+)"))
async def anime_episode(bot: Amime, callback: CallbackQuery):
    user = callback.from_user
    lang = callback._lang

    anime_id = int(callback.matches[0].group(1))
    season = int(callback.matches[0].group(2))
    number = int(callback.matches[0].group(3))

    async with anilist.AsyncClient() as client:
        anime = await client.get(anime_id, "anime")

        if anime is None:
            return

        text = f"<b>{anime.title.romaji}</b> (<code>{anime.title.native}</code>)\n"

        user_db = await Users.get(id=user.id)
        language = user_db.language_anime
        subtitled = user_db.subtitled_anime

        is_admin = bot.is_sudo(user)
        if is_admin:
            episodes = await Episodes.filter(added_by=user.id)

        is_auth = bot.is_collaborator(user)

        episodes = await Episodes.filter(
            anime=anime_id, season=season, language=language, subtitled=subtitled
        )
        episodes = sorted(episodes, key=lambda episode: episode.number)
        all_episodes = await Episodes.filter(
            anime=anime_id, language=language, subtitled=subtitled
        )
        all_episodes = sorted(all_episodes, key=lambda episode: episode.number)

        episode = await Episodes.get_or_none(
            anime=anime_id,
            season=season,
            number=number,
            language=language,
            subtitled=subtitled,
        )
        if episode is not None:
            await Viewed.get_or_create(user=user.id, item=episode.id, type="anime")

            keyboard = [[await get_watched_button(lang, user, episode.id), (
                        lang.report_button,
                        f"report1 episode {anime_id} {season} {number} -1",
                    )]]

            if len(episode.name) > 0:
                text += f"\n<b>{lang.name}</b>: <code>{episode.name}</code>"

            if episode.season > 0:
                text += f"\n<b>{lang.season}</b>: <code>{episode.season}</code>"

            episode_number = f"{episode.number}"
            if episode.unified_until > 0:
                episode_number += f"-{episode.unified_until}"
            text += f"\n<b>{lang.episode}</b>: <code>{episode_number}</code>"
            text += f" | <b>{lang.duration}</b>: <code>{episode.duration}m</code>"
            text += f"\n<b>{lang.language}</b>: <code>{lang.strings[episode.language]['LANGUAGE_NAME']}</code>"
            text += f" | <b>Diunggah oleh</b>: `{episode.added_by}`"

            #if len(episode.added_by) > 0:
            #    if not episode.added_by.isdecimal():
            #        text += f"\n<b>{lang.added_by}</b>: <b>{episode.added_by}</b>"

            if len(episode.notes) > 0:
                text += f"\n<b>{lang.notes}</b>: <i>{episode.notes}</i>"

            if is_admin:
                viewed = await Viewed.filter(item=episode.id, type="anime")
                text += f"\n\n<b>{len(viewed)}+ {lang.views.lower()}</b> - (Hanya admin yang bisa melihat)"
            text += f"\n\n┏━━━━━━━━━━━━━━━━━━━━━</code>"
            text += f"\n┣❏ <b>Profil Saya</b>: <code>{user.username}</code> - <a href='t.me/{user.username}'>{user.id}</a>"
            watcheds = await Watched.filter(user=user.id)
            text += f"\n┣❏ {lang.episodes_watched}</b>: <code>{len(watcheds)} Eps</code>"
            if is_admin:
                text += f" | <b>Status</b> : Admin"
            if is_auth:
                text += f" | <b>Status</b> : Premium (Lifetime)"
            if not is_auth and not is_admin:
                text += f" | <b>Status</b> : Free User - <a href='t.me/akuiiki'>Order Premium</a>"
            text += f"\n┗━━━━━━━━━━━━━━━━━━━━━</code>"

            previous_button = await get_previous_episode_button(
                lang, episodes, all_episodes, anime_id, season, number, language
            )
            next_button = await get_next_episode_button(
                lang, episodes, all_episodes, anime_id, season, number
            )
            if not (
                previous_button[0] == lang.dot_button
                and next_button[0] == lang.dot_button
            ):
                keyboard.append([previous_button, next_button])

            #keyboard.append(
            #    [
            #        (
            #            lang.report_button,
            #            f"report episode {anime_id} {season} {number} -1",
            #        )
            #    ]
            #)

            if anime.format.lower() == "movie":
                keyboard.append(
                    [
                        (
                            lang.back_button,
                            f"episode_global {anime_id} 0 1",
                        )
                    ]
                )
            else:
                keyboard.append(
                    [
                        (
                            lang.back_button,
                            f"episodes_global {anime_id} {season} {math.ceil(number / (5 * 3))}",
                        )
                    ]
                )

            await callback.edit_message_media(
                InputMediaVideo(
                    episode.file_id,
                    caption=text,
                    supports_streaming=True,
                ),
                reply_markup=ikb(keyboard),
                
            )


async def get_watched_button(lang, user: User, episode_id: int) -> Tuple:
    watched = await Watched.get_or_none(
        user=user.id,
        episode=episode_id,
    )
    if watched is None:
        text = lang.mark_as_watched_button
    else:
        text = lang.mark_as_unwatched_button
    return (text, f"watched {episode_id}")


@Amime.on_callback_query(filters.regex(r"^watched (?P<id>\d+)"))
async def watched_callback(bot: Amime, callback: CallbackQuery):
    episode_id = int(callback.matches[0]["id"])
    message = callback.message
    user = callback.from_user
    lang = callback._lang

    watched = await Watched.get_or_none(
        user=user.id,
        episode=episode_id,
    )

    if watched is None:
        await Watched.create(user=user.id, episode=episode_id)
    else:
        await watched.delete()

    keyboard = bki(message.reply_markup)

    for line, column in enumerate(keyboard):
        for index, button in enumerate(column):
            if button[1].startswith("watched"):
                keyboard[line][index] = await get_watched_button(
                    lang,
                    user,
                    episode_id,
                )

    await callback.edit_message_reply_markup(ikb(keyboard))


async def get_previous_episode_button(
    lang, episodes, all_episodes, anime, season, number, language
) -> Tuple:
    s = 0
    n = 0

    for episode in episodes:
        if episode.number < number:
            s = season
            n = episode.number

    if not n > 0:
        seasons = []

        for episode in all_episodes:
            if episode.season not in seasons:
                seasons.append(episode.season)

        for _s in seasons:
            episodes = await Episodes.filter(anime=anime, season=_s, language=language)
            episodes = sorted(
                episodes, key=lambda episode: episode.number, reverse=True
            )

            for episode in episodes:
                if episode.season < season:
                    s = episode.season
                    n = episode.number
                    break

            if n > 0:
                break

    if n > 0:
        return (lang.previous_button, f"episode_global {anime} {s} {n}")
    else:
        return (lang.dot_button, "noop")


async def get_next_episode_button(
    lang, episodes, all_episodes, anime, season, number
) -> Tuple:
    s = 0
    n = 0

    for episode in episodes:
        if episode.number > number:
            s = season
            n = episode.number
            break

    if not n > 0:
        for episode in all_episodes:
            if episode.season > season:
                s = episode.season
                n = episode.number
                break

    if n > 0:
        return (lang.next_button, f"episode_global {anime} {s} {n}")
    else:
        return (lang.dot_button, "noop")
