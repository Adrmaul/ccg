from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime
from amime.modules.mylists import get_mylist_button
from amime.modules.notify import get_notify_button


@Amime.on_message(filters.cmd(r"manage_list$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^manage_list$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    buttons.append(await get_mylist_button(lang, user.id, "anime", anime_id))

    if is_callback:
        keyboard.append([(lang.z_button, "z_lists anime 1"), (lang.back_button, "menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.listsx_text,
        reply_markup=ikb(keyboard),
    )