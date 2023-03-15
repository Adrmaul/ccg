from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"listsx$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^listsx$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.a_button, "a_lists anime 1"),
            (lang.b_button, "b_lists anime 1"),
            (lang.c_button, "c_lists anime 1"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.listsx_text,
        reply_markup=ikb(keyboard),
    )