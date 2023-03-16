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



async with anilist.AsyncClient() as client:
    a_lists = await A_lists.filter(type="anime")
    total_data = len(a_lists)
    total_pages = (total_data + 7) // 8  # Menentukan jumlah halaman dengan 8 item per halaman
    offset = (page - 1) * 8
    a_lists = a_lists.order_by("-created_at").limit(8, offset=offset)

    anime_list = await asyncio.gather(
        *[client.get(a_list.item, "anime") for a_list in a_lists]
    )

    results = list(zip(a_lists, anime_list))

    layout = Pagination(
        results,
        item_data=lambda i, pg: f"menu {i[0].item}",
        item_title=lambda i, pg: i[1].title.romaji,
        page_data=lambda pg: f"a_lists anime {pg}",
    )

    keyboard = layout.create(page, lines=8)

keyboard.append([(lang.back_button, "listsx")])

await message.edit_text(lang.mylist_text, reply_markup=ikb(keyboard))