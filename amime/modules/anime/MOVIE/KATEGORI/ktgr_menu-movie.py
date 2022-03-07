from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"ktgr_movie-menu$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr_movie-menu$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.ACTION, "movie_action anime 1"),
            (lang.ADVENTURE, "movie_adventure anime 1"),
        ],
        [
            (lang.COMEDY, "movie_comedy anime 1"),
            (lang.DRAMA, "movie_drama anime 1"),
        ],
        [
            (lang.ECCHI, "movie_ecchi anime 1"),
            (lang.FANTASY, "movie_fantasy anime 1"),
        ],
        [
            (lang.HORROR, "movie_horror anime 1"),
            (lang.MAHOUSJ, "movie_mahousj anime 1"),
        ],
        [
            (lang.MECHA, "movie_mecha anime 1"),
            (lang.MUSIC, "movie_music anime 1"),
        ],
        [
            (lang.MYSTERY, "movie_mystery anime 1"),
            (lang.PSYCHOLOGICAL, "movie_psychological anime 1"),
        ],
        [
            (lang.ROMANCE, "movie_romance anime 1"),
            (lang.SCIFI, "movie_scifi anime 1"),
        ],
        [
            (lang.SOL, "movie_sol anime 1"),
            (lang.SPORTS, "movie_sports anime 1"),
        ],
        [
            (lang.SUPERNATURAL, "movie_supernatural anime 1"),
            (lang.THRILLER, "movie_thriller anime 1"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "movie-menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
    )
