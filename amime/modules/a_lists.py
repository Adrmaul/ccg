# MIT License
#
# Copyright (c) 2021 Andriel Rodrigues for Amano Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Tuple

from pyrogram import filters
from pyrogram.types import CallbackQuery, User
from pyromod.helpers import bki, ikb

from amime.amime import Amime
from amime.database import A_lists


async def get_a_list_button(
    lang, user: User, content_type: str, content_id: int
) -> Tuple:
    a_list = await A_lists.get_or_none(
        item=content_id, type=content_type
    )
    if a_list is None:
        status = "➕"
    else:
        status = "➖"
    return (f"{status} {lang.a_list}", f"a_list {content_type} {content_id}")


@Amime.on_callback_query(filters.regex(r"^a_list (?P<type>\w+) (?P<id>\d+)"))
async def a_list_callback(bot: Amime, callback: CallbackQuery):
    content_type = callback.matches[0]["type"]
    content_id = int(callback.matches[0]["id"])
    message = callback.message
    user = callback.from_user
    lang = callback._lang

    a_list = await A_lists.get_or_none(
        item=content_id, type=content_type
    )

    if a_list is None:
        await A_lists.create(user=user.id, item=content_id, type=content_type)
        await callback.answer(lang.added_to_a_lists_alert, show_alert=True)
    else:
        await a_list.delete()
        await callback.answer(lang.removed_from_a_lists_alert, show_alert=True)

    keyboard = bki(message.reply_markup)

    for line, column in enumerate(keyboard):
        for index, button in enumerate(column):
            if button[1].startswith("a_list"):
                keyboard[line][index] = await get_a_list_button(
                    lang, user, content_type, content_id
                )

    await callback.edit_message_reply_markup(ikb(keyboard))
