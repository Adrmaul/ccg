from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime



@Amime.on_message(filters.cmd(r"ktgr_progress$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr_progress$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.anime_satu, f"menu_140960" ),
            (lang.anime_dua, f"menu_125367"),
        ],
        [
            (lang.anime_tiga, f"menu_136080"),
            (lang.anime_empat, f"menu_130586"),
        ],
        [
            (lang.anime_lima, f"menu_125124"),
            (lang.anime_enam, f"menu_116605"),
        ],
        [
            (lang.anime_tujuh, f"menu_129201"),
            (lang.anime_delapan, f"menu_111321"),
        ],

    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr-ongoing")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.ongoing_text,
        reply_markup=ikb(keyboard),
    )
