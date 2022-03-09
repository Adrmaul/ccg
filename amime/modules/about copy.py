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
from telegram.ext import (CallbackContext,
                          run_async, Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler)


from amime.amime import Amime
from amime.config import CHANNELS, GROUPS



    # buat random waifu
@Amime.on_message(filters.cmd(r"pic$"))
@Amime.on_callback_query(filters.regex(r"^pic$"))
def get_url():
    contents = requests.get('https://arugaz.herokuapp.com/api/nekonime').json()
    url = contents['result']
    return url
def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

@run_async
@Amime.on_message(filters.cmd(r"pic$"))
@Amime.on_callback_query(filters.regex(r"^pic$"))
def pic(update, context):
    url = get_image_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

# Buat random image di folder source