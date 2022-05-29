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

from ctypes.wintypes import SHORT
from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"menu$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^menu$"))
async def anime_start(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.tv_button, "tvshow_menu"),
            (lang.movie_button, "movie-menu"),
            (lang.tvs_button, "tvshort_menu"),
        ],
        [
            (lang.ova_button, "ova_menu"),
            (lang.ona_button, "ona_menu"),
            (lang.spesial_button, "special_menu"),
        ],
        [
            (lang.mv_button, "mv_menu"),
            (lang.search_button, "", "switch_inline_query_current_chat"),
        ],
        [
            (lang.favorites_button, "favorites anime 1"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "start")])

    await message.reply_text(
            protect_content=True,
            reply_markup=ikb(keyboard),
        )



