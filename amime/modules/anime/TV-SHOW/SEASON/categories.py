from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"ktgr-season$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^ktgr-season$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.duatiga_button, "2023_se"),
            (lang.duadua_button, "2022_se"),

        ],
        [
            (lang.duasatu_button, "2021_se"),
            (lang.duapuluh_button, "2020_se"),

        ],   
        [
            (lang.sembilanbls_button, "2019_se"),
            (lang.delapanbls_button, "2018_se"),

        ], 
        [
            (lang.tujuhbls_button, "2017_se"),
            (lang.enambls_button, "2016_se"),

        ], 
        [
            (lang.limabls_button, "2015_se"),
            (lang.empatbls_button, "2014_se"),

        ], 
        [
            (lang.tigabls_button, "2013_se"),
            (lang.duabls_button, "2012_se"),

        ], 
        [
            (lang.sebls_button, "2011_se"),
            (lang.sepuluh_button, "2010_se"),

        ], 
        [
            (lang.sembilan_button, "2009_se"),
            (lang.delapan_button, "2008_se"),

        ], 
        [
            (lang.tujuh_button, "2007_se"),
            (lang.enam_button, "2006_se"),

        ],   
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr_tvshow-menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.anime_text,
        reply_markup=ikb(keyboard),
    )

