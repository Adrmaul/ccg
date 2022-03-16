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

from typing import Dict, Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime
from amime.config import CHANNELS, GROUPS

import anilist
from pyrogram import filters
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from pyromod.helpers import array_chunk, ikb

from amime.amime import Amime
from amime.database import Episodes, Users
from amime.modules.favorites import get_favorite_button
from amime.modules.notify import get_notify_button


@Amime.on_callback_query(filters.regex(r"^infodownload$"))
async def about(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    kwargs: Dict = {}

    is_private = await filters.private(bot, message)
    if is_private and is_callback:
        keyboard = [
            [
                (lang.back_button, "download more {anime.id} {user.id}"),
            ],
        ]
        kwargs["reply_markup"] = ikb(keyboard)

    await (message.edit_text if is_callback else message.reply_text)(
        lang.infodownload_text.format(
            bot_name=bot.me.first_name,
            playit="<a href='https://t.me/ccgXmediaUp_bot?start=Z2V0LTEyMzk0OTI0OTg1MDI2OTA2'>PlayIt</a>",

        ),
        disable_web_page_preview=True,
        **kwargs,
    )