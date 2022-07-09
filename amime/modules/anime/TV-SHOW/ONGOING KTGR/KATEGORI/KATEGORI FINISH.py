from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"ktgr-ongoing$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr-ongoing$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.ACTION, "tv_ongoing_action anime 1"),
            (lang.ADVENTURE, "tv_ongoing_adventure anime 1"),
        ],
        [
            (lang.COMEDY, "tv_ongoing_comedy anime 1"),
            (lang.DRAMA, "tv_ongoing_drama anime 1"),
        ],
        [
            (lang.ECCHI, "tv_ongoing_ecchi anime 1"),
            (lang.FANTASY, "tv_ongoing_fantasy anime 1"),
        ],
        [
            (lang.HORROR, "tv_ongoing_horror anime 1"),
            (lang.MAHOUSJ, "tv_ongoing_mahousj anime 1"),
        ],
        [
            (lang.MECHA, "tv_ongoing_mecha anime 1"),
            (lang.MUSIC, "tv_ongoing_music anime 1"),
        ],
        [
            (lang.MYSTERY, "tv_ongoing_mystery anime 1"),
            (lang.PSYCHOLOGICAL, "tv_ongoing_psychological anime 1"),
        ],
        [
            (lang.ROMANCE, "tv_ongoing_romance anime 1"),
            (lang.SCIFI, "tv_ongoing_scifi anime 1"),
        ],
        [
            (lang.SOL, "tv_ongoing_sol anime 1"),
            (lang.SPORTS, "tv_ongoing_sports anime 1"),
        ],
        [
            (lang.SUPERNATURAL, "tv_ongoing_supernatural anime 1"),
            (lang.THRILLER, "tv_ongoing_thriller anime 1"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.jadwal_button, "jadwal"), (lang.back_button, "ktgr_tvshow-menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.progress_text,
        reply_markup=ikb(keyboard),
    )
