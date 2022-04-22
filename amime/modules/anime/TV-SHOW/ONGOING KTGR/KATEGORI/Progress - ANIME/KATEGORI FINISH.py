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
            (lang.anime1_button, f"anime more 140960 {user_id}"),
            (lang.anime2_button, f"anime more 125367 {user_id}"),
        ],
        [
            (lang.anime3_button, f"anime more 142984 {user_id}"),
            (lang.anime4_button, f"anime more 137281 {user_id}"),
        ],
        [
            (lang.anime5_button, f"anime more 116605 {user_id}"),
            (lang.anime6_button, f"anime more 140457 {user_id}"),
        ],
        [
            (lang.anime7_button, f"anime more 125124 {user_id}"),
            (lang.anime8_button, f"anime more 132010 {user_id}"),
        ],
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "ktgr-ongoing")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.progress_text,
        reply_markup=ikb(keyboard),
    )
