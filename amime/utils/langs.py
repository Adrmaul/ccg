# MIT License
#
# Copyright (c) 2021 Amano Team
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

import glob
import re
import yaml

from langs import Langs

from pyrogram.types import CallbackQuery, Message, InlineQuery
from typing import Dict

from .. import log


def load():
    langs: Dict = {}

    files = glob.glob("amime/locales/*.yml")
    for file_name in files:
        language_code = re.match(r"amime/locales/(.+)\.yml$", file_name)[1]
        with open(file_name) as file:
            langs[language_code] = yaml.safe_load(file)

    lang = Langs(**langs, escape_html=True)

    CallbackQuery._lang = lang
    Message._lang = lang
    InlineQuery._lang = lang

    log.info(f"{len(langs)} language{'s' if len(langs) != 1 else ''} have been loaded.")
