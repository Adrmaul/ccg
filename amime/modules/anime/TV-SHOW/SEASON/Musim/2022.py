from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"2022_se$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^2022_se$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.musim_salju, "winter_2022"),
            (lang.musim_gugur, "spring_2022"),

        ],
        [
            (lang.musim_panas, "summer_2022"),
            (lang.musim_semi, "fall_2022"),

        ],   
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr-season")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
    )

