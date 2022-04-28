from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

import datetime
import re
import anilist
from pyromod.helpers import array_chunk, ikb

from amime.amime import Amime
from amime.config import CHATS
from amime.database import Requests
from amime.modules.anime.view import anime_view




@Amime.on_message(filters.cmd(r"sabtu$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^sabtu$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.anime_satu, f"menu 116605"),
        ],
        [
            (lang.anime_lima, f"menu 125124"),
        ],
        [
            (lang.anime_dua, f"menu 125367"),
        ],


    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr-ongoing")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.ongoing_text,
        reply_markup=ikb(keyboard),
    )
