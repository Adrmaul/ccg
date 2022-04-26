from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime

import httpx
from anilist.types import Anime
from pyromod.nav import Pagination



@Amime.on_message(filters.cmd(r"ktgr_progress$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr_progress$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.anime_satu, f"menu 140960" ),
            (lang.anime_dua, f"menu 125367"),
        ],
        [
            (lang.anime_tiga, f"menu 136080"),
            (lang.anime_empat, f"menu 130586"),
        ],
        [
            (lang.anime_lima, f"menu 125124"),
            (lang.anime_enam, f"menu 116605"),
        ],
        [
            (lang.anime_tujuh, f"menu 129201"),
            (lang.anime_delapan, f"menu 111321"),
        ],
        #[
            (lang.anime_sembilan, f"menu {i.id}"),
            (lang.anime_sepuluh, f"menu {i.id}"),
        #],
        #[
            (lang.aime11, "tv_ongoing_mystery anime 1"),
            (lang.anime12, "tv_ongoing_psychological anime 1"),
        #],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr-ongoing")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.ongoing_text,
        reply_markup=ikb(keyboard),
    )
