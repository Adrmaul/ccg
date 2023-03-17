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

import anilist
import asyncio
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyromod.helpers import ikb
from pyromod.nav import Pagination

from amime.amime import Amime
from amime.database import A_lists

# inisialisasi cache untuk data dari database dan API Anilist
cache = {}


@Amime.on_callback_query(filters.regex(r"a_lists anime (?P<page>\d+)"))
async def anime_a_lists(bot: Amime, callback: CallbackQuery):
    page = int(callback.matches[0]["page"])

    message = callback.message
    user = callback.from_user
    lang = callback._lang

    keyboard = []

    # mengambil data dari cache jika sudah ada
    if "a_lists" in cache:
        a_lists = cache["a_lists"]
    else:
        # menggunakan select_related untuk mengambil objek terkait dalam satu kueri
        a_lists = await A_lists.filter(type="anime").select_related("user").all()
        cache["a_lists"] = a_lists

    results = []
    # menggunakan asyncio.gather untuk memuat data dari Anilist dalam batch
    async with anilist.AsyncClient() as client:
        tasks = []
        for a_list in a_lists:
            tasks.append(client.get(a_list.item, "anime"))
        anime_list = await asyncio.gather(*tasks)

        # menggunakan prefetch_related untuk mengambil objek terkait dalam satu kueri
        for a_list, anime in zip(a_lists, anime_list):
            results.append((a_list, anime))
        cache["anime_list"] = anime_list

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

    # Mengirim jawaban callback query dengan menampilkan hasil
    await callback.answer()
    await message.edit_text(
        lang.mylist_text,
        reply_markup=ikb(keyboard),
    )
