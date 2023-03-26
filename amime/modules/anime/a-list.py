import asyncio
import anilist
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyromod.helpers import ikb
from pyromod.nav import Pagination
from aiocache import cached, SimpleMemoryCache

from amime.amime import Amime
from amime.database import A_lists

a_lists_cache = SimpleMemoryCache()


async def fetch_anime_data(anime_ids):
    async with anilist.AsyncClient() as client:
        tasks = [client.get(anime_id, "anime") for anime_id in anime_ids]
        return await asyncio.gather(*tasks)


@cached(ttl=3600, cache=a_lists_cache, key="a_lists")
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

    results = [(a_list, anime) for a_list, anime in zip(a_lists, anime_data)]

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