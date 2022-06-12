from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"2011_se$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^2011_se$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.musim_salju, "winter_2011 anime 1"),
            (lang.musim_gugur, "spring_2011 anime 1"),

        ],
        [
            (lang.musim_panas, "summer_2011 anime 1"),
            (lang.musim_semi, "fall_2011 anime 1"),

        ],   
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr-season")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.musim_text,
        reply_markup=ikb(keyboard),
    )

