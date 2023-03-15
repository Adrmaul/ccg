from ctypes.wintypes import SHORT
from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"lists$"))
@Amime.on_callback_query(filters.regex(r"^lists$"))
async def anime_start(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.tv_button, "A_lists anime 1"),
            (lang.movie_button, "movie-lists"),
            (lang.tvs_button, "tvshort_lists"),
        ],
        [
            (lang.ova_button, "ova_lists"),
            (lang.ona_button, "ona_lists"),
            (lang.spesial_button, "special_lists"),
        ],
        [
            (lang.mv_button, "mv_lists"),
            (lang.garapan_button, "garapan anime 1"),
        ],
        [
            (lang.favorites_button, "favorites anime 1"),
            (lang.mylists_button, "mylists anime 1"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
     )