import anilist
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyromod.helpers import ikb
from pyromod.nav import Pagination

from amime.amime import Amime
from amime.database import A_lists


RESULTS_PER_PAGE = 8


@Amime.on_callback_query(filters.regex(r"a_lists anime (?P<page>\d+)"))
async def anime_a_lists(bot: Amime, callback: CallbackQuery):
    page = int(callback.matches[0]["page"])

    message = callback.message
    user = callback.from_user
    lang = callback._lang

    async with anilist.AsyncClient() as client:
        a_lists = await A_lists.filter(type="anime")
        total_results = len(a_lists)

        # Menghitung jumlah halaman yang tersedia
        total_pages = (total_results - 1) // RESULTS_PER_PAGE + 1

        # Mengambil hanya data yang dibutuhkan pada halaman yang diminta
        start_index = (page - 1) * RESULTS_PER_PAGE
        end_index = start_index + RESULTS_PER_PAGE
        page_results = a_lists[start_index:end_index]

        # Memuat data anime untuk setiap item di halaman
        results = []
        for a_list in page_results:
            anime = await client.get(a_list.item, "anime")
            results.append((a_list, anime))

        # Membuat tampilan halaman dengan teknik pagination
        layout = Pagination(
            results,
            item_data=lambda i, pg: f"menu {i[0].item}",
            item_title=lambda i, pg: i[1].title.romaji,
            page_data=lambda pg: f"a_lists anime {pg}",
            current_page=page,
            total_pages=total_pages,
        )

        # Menampilkan halaman saat ini
        lines = layout.create(page, lines=RESULTS_PER_PAGE)

    # Menambahkan tombol navigasi ke halaman sebelumnya dan selanjutnya
    keyboard = []
    if page > 1:
        keyboard.append([(lang.previous_button, f"a_lists anime {page-1}")])
    if page < total_pages:
        keyboard.append([(lang.next_button, f"a_lists anime {page+1}")])

    # Menambahkan tombol kembali ke menu utama
    keyboard.append([(lang.back_button, "listsx")])

    # Mengirim jawaban callback query dengan menampilkan hasil
    await callback.answer()
    await message.edit_text(
        lang.mylist_text,
        reply_markup=ikb(keyboard + lines),
    )