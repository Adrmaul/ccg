from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"ktgr-51plus$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr-51plus$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.TOP, "tvshow_51plus_top anime 1"),
            (lang.TRENDING, "tvshow_51plus_trending anime 1"),
            (lang.UPCOMING, "tvshow_51plus_upcoming anime 1"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr-episode")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
    )