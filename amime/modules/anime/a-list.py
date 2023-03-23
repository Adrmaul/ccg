import anilist
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyromod.helpers import ikb
from pyromod.nav import Pagination

from amime.amime import Amime
from amime.database import A_lists


@Amime.on_callback_query(filters.regex(r"a_lists anime (?P<page>\d+)"))
async def anime_a_lists(bot: Amime, callback: CallbackQuery):
    page = int(callback.matches[0]["page"])
    message = callback.message
    user = callback.from_user
    lang = callback._lang

    keyboard = []
    async with anilist.AsyncClient() as client:
        # Mengambil seluruh data dari A_lists dalam batch
        a_lists = await A_lists.all()
        # Menyiapkan id-item list untuk diproses bersama dengan anilist API
        item_ids = [a_list.item for a_list in a_lists]

        # Mengambil data anime dari Anilist secara bersamaan dengan A_lists
        animes = await client.get_multi(item_ids, "anime")

        # Menggabungkan data dari A_lists dan Anilist menjadi satu tuple
        results = [(a_lists[i], animes[i]) for i in range(len(a_lists))]

        layout = Pagination(
            results,
            item_data=lambda i, pg: f"menu {i[0].item}",
            item_title=lambda i, pg: i[1].title.romaji,
            page_data=lambda pg: f"a_lists anime {pg}",
        )

        # Membuat keyboard untuk pagination
        lines = layout.create(page, lines=8)
        if len(lines) > 0:
            keyboard += lines

    # Menambah tombol back
    keyboard.append([(lang.back_button, "listsx")])

    # Mengirim jawaban callback query dengan menampilkan hasil
    await callback.answer()
    await message.edit_text(
        lang.mylist_text,
        reply_markup=ikb(keyboard),
    )