from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"ktgr-season1$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr-season1$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.duatiga1_button, "2005_se"),
            (lang.duadua1_button, "2004_se"),

        ],
        [
            (lang.duasatu1_button, "2003_se"),
            (lang.duapuluh1_button, "2002_se"),

        ],   
        [
            (lang.sembilanbls1_button, "2001_se"),
            (lang.delapanbls1_button, "2000_se"),

        ], 
        [
            (lang.tujuhbls1_button, "1999_se"),
            (lang.enambls1_button, "1998_se"),

        ], 
        [
            (lang.limabls1_button, "1997_se"),
            (lang.empatbls1_button, "1996_se"),

        ], 
        [
            (lang.tigabls1_button, "1995_se"),
            (lang.duabls1_button, "1994_se"),

        ], 
        [
            (lang.sebelas1_button, "1993_se"),
            (lang.sepuluh1_button, "1992_se"),

        ], 
        [
            (lang.sembilan1_button, "1991_se"),
            (lang.delapan1_button, "1990_se"),

        ], 
        [
            (lang.tujuh1_button, "1989_se"),
            (lang.enam1_button, "1988_se"),

        ],   
    ]

    if is_callback:
        keyboard.append([(lang.pagesatu_button, "ktgr-season")])
        keyboard.append([(lang.back_button, "ktgr_tvshow-menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
    )

