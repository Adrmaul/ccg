from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime

import httpx
from anilist.types import Anime
from pyromod.nav import Pagination

from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from pyromod.helpers import array_chunk, ikb
from amime.database import Episodes, Users
from amime.modules.favorites import get_favorite_button
from amime.modules.notify import get_notify_button



@Amime.on_message(filters.cmd(r"ktgr_progress$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr_progress$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    buttons = [
            (
                        lang.anime_satu,
                        f"menu 140960"
                    )       
        ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr-ongoing")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.ongoing_text,
        reply_markup=ikb(keyboard),
    )
