import httpx
from anilist.types import Anime
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyromod.helpers import ikb
from pyromod.nav import Pagination

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

@Amime.on_callback_query(filters.regex(r"^tv_ongoing_anime anime (?P<page>\d+)"))
async def anime_suggestions(bot: Amime, callback: CallbackQuery):
    page = int(callback.matches[0]["page"])

    message = callback.message
    lang = callback._lang
    user = callback.from_user

    anime_id = int(callback.matches[0].group(1))


    async with anilist.AsyncClient() as client:
        anime = await client.get(anime_id, "anime")

    keyboard = []
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.post(
            url="https://graphql.anilist.co",
            json=dict(
                query="""
                query($page: Int, $perPage: Int) {
                    Page(page: $page, perPage: $perPage) {
                        media(type: ANIME, sort: TRENDING_DESC, status: RELEASING) {
                            id
                            title {
                                romaji
                                english
                                native
                            }
                            siteUrl
                        }
                    }
                }
                """,
                variables=dict(
                    perPage=100,
                ),
            ),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        data = response.json()
        await client.aclose()

        user_db = await Users.get(id=user.id)
        language = user_db.language_anime

        episodes1 = sorted(episodes, key=lambda episode: episode.number)
        episodes1 = await Episodes.filter(anime=anime_id, language=language)
        episodes1 = [*filter(lambda episode: len(episode.file_id) > 0, episodes)]


        if data["data"]:
            items = data["data"]["Page"]["media"]
            suggestions = [
                Anime(id=item["id"], title=item["title"], url=item["siteUrl"])
                for item in items
            ]

            if len(episodes1) > 0:
                db = f"✅"
        
            if len(episodes1) < 1:
                db = f""

            layout = Pagination(
                suggestions,
                item_data=lambda i, pg: f"menu {i.id}",
                item_title=lambda i, pg: f"{db}{i.title.romaji}",
                page_data=lambda pg: f"tv_ongoing_anime anime {pg}",
            )

            lines = layout.create(page, lines=8)

            if len(lines) > 0:
                keyboard += lines
    keyboard.append([(lang.Hapus_text, "close_data"), (lang.back_button, "jadwal")])

    await message.edit_text(
        lang.jad_text,
        reply_markup=ikb(keyboard),
    )
