from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"ktgr-24+$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr-24+$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.TOP, "tvshow_24+_top anime 1"),
            (lang.TRENDING, "tvshow_24+_trending anime 1"),
            (lang.UPCOMING, "tvshow_24+_upcoming anime 1"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr-episode")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
    )