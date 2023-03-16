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
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pyromod.helpers import ikb
from pyromod.nav import Pagination
import asyncio

from amime.amime import Amime
from amime.database import A_lists
from asyncio import gather



@Amime.on_callback_query(filters.regex(r"a_lists anime (?P<page>\d+)"))
async def anime_a_lists(bot: Amime, callback: CallbackQuery):
    page = int(callback.matches[0]["page"])
    message = callback.message
    user = callback.from_user
    lang = callback._lang

    async with anilist.AsyncClient() as client:
        # hitung total jumlah data yang tersedia
        total_data = await A_lists.filter(type="anime").count()
        total_pages = ceil(total_data / 10)

        # inisialisasi list untuk menyimpan semua data anime
        anime_list = []

        # loop untuk mengambil data dari semua halaman
        for p in range(1, total_pages+1):
            a_lists = await A_lists.filter(type="anime").offset((p - 1) * 10).limit(10)

            # ambil data anime dari setiap item pada a_lists
            anime_list += await asyncio.gather(
                *[client.get(a_list.item, "anime") for a_list in a_lists]
            )

        # zip a_lists dan anime_list menjadi satu list hasil
        results = list(zip(a_lists, anime_list))

        # buat tampilan halaman menggunakan pagination
        layout = Pagination(
            results,
            item_data=lambda i, pg: f"menu {i[0].item}",
            item_title=lambda i, pg: i[1].title.romaji,
            page_data=lambda pg: f"a_lists anime {pg}",
        )

        keyboard = layout.create(page, lines=8)

    keyboard.append([(lang.back_button, "listsx")])

    await message.edit_text(lang.mylist_text, reply_markup=ikb(keyboard))