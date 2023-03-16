import anilist
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyromod.helpers import ikb
from pyromod.nav import Pagination

from amime.amime import Amime
from amime.database import A_lists, Anime


@Amime.on_callback_query(filters.regex(r"a_lists anime (?P<page>\d+)"))
async def anime_a_lists(bot: Amime, callback: CallbackQuery):
    page = int(callback.matches[0]["page"])

    message = callback.message
    user = callback.from_user
    lang = callback._lang

    keyboard = []
    async with anilist.AsyncClient() as client:
        results = await A_lists.filter(type="anime").select_related("anime").all()

        layout = Pagination(
            results,
            item_data=lambda i, pg: f"menu {i.anime.id}",
            item_title=lambda i, pg: i.anime.title.romaji,
            page_data=lambda pg: f"a_lists anime {pg}",
        )

        lines = layout.create(page, lines=8)

        if len(lines) > 0:
            keyboard += lines

    keyboard.append([(lang.back_button, "listsx")])

    await message.edit_text(
        lang.mylist_text,
        reply_markup=ikb(keyboard),
    )