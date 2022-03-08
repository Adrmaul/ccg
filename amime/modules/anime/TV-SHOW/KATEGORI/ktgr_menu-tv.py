from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"ktgr_tv-menu$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr_tv-menu$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.ACTION, "tv_action anime 1"),
            (lang.ADVENTURE, "tv_adventure anime 1"),
        ],
        [
            (lang.COMEDY, "tv_comedy anime 1"),
            (lang.DRAMA, "tv_drama anime 1"),
        ],
        [
            (lang.ECCHI, "tv_ecchi anime 1"),
            (lang.FANTASY, "tv_fantasy anime 1"),
        ],
        [
            (lang.HORROR, "tv_horror anime 1"),
            (lang.MAHOUSJ, "tv_mahousj anime 1"),
        ],
        [
            (lang.MECHA, "tv_mecha anime 1"),
            (lang.MUSIC, "tv_music anime 1"),
        ],
        [
            (lang.MYSTERY, "tv_mystery anime 1"),
            (lang.PSYCHOLOGICAL, "tv_psychological anime 1"),
        ],
        [
            (lang.ROMANCE, "tv_romance anime 1"),
            (lang.SCIFI, "tv_scifi anime 1"),
        ],
        [
            (lang.SOL, "tv_sol anime 1"),
            (lang.SPORTS, "tv_sports anime 1"),
        ],
        [
            (lang.SUPERNATURAL, "tv_supernatural anime 1"),
            (lang.THRILLER, "tv_thriller anime 1"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "tv-menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
    )
