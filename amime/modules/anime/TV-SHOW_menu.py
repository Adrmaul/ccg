from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"tvshow_menu$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^tvshow_menu$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.TOP, "top_TV-SHOW anime 1"),
            (lang.TRENDING, "trending_TV-SHOW anime 1"),
            (lang.UPCOMING, "upcoming_TV-SHOW anime 1"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
    )