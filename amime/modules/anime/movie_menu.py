from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"movie-menu$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^movie-menu$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.TOP, "top_movie anime 1"),
            (lang.TRENDING, "trending_movie anime 1"),
            (lang.UPCOMING, "upcoming_movie anime 1"),
        ],
        [
            (lang.KATEGORI, "ktgr_movie-menu"),
        ],
        
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.movie-menu_text,
        reply_markup=ikb(keyboard),
    )