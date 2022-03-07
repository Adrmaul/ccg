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


@Amime.on_message(filters.cmd(r"about$"))
@Amime.on_callback_query(filters.regex(r"^about$"))
async def about(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    kwargs: Dict = {}

    is_private = await filters.private(bot, message)
    if is_private and is_callback:
        keyboard = [
            [
                (lang.back_button, "start"),
            ],
        ]
        kwargs["reply_markup"] = ikb(keyboard)

    await (message.edit_text if is_callback else message.reply_text)(
        lang.about_text.format(
            Disclaimer untuk bot ccgnimex.
            Ada beberapa yang mungkin harus kalian pahami terkait bot ini, agar nantinya kalian memahami sepenuhnya bot ini.
            Bot ini merupakan bot yang terhubung dengan website anilist.co, yang dimana kalian bisa menggunakan bot ini untuk list, anime, manga, dan lainnya.
            adapun beberapa fitur yang kami pakai, yaitu **mendownload/streaming anime.**.
            
            Mendownload/Streaming
            Perlu kalian ketahui, mendownload/streaming video disini, merupakan tindakan ilegal/tidak dibenarkan, artinya kenapa?
            Pada dasarnya kami tidak mempunyai izin, untuk mempublish/share anime, bisa dibilang ini BAJAKAN.
            Jadi saran kami, lebih baik kalian melihat anime ke situs/app yang sudah legal, seperti MUSE INDONESIA, NETFLIX,dan lainnya.
            
            Tujuan Membuat bot ini?
            Karena ingin memudahkan admin pribadi untuk melist anime dan menonton anime, walaupun ini melanggar. tetapi kami pun jika tetap mendukung anime legal. dan menontonnya.
            
            Dapat dari mana sumber file anime?
            Kami, mendapatkan file anime dari berbagai macam website, berikut ini listnya:
            Otakudesu | Kusonime | Koenime | Samehadaku | Oplovers | Bakadame | ...
            
            Jadi kami mengucapkan terimakasih kepada mereka yang sudah memberikan anime, silahkan untuk mendukungnya, kalian bisa kunjungi website mereka.
            
            
           KESIMPULAN.
           Bot ini memang tujuannya untuk memudahkan kita, dan tentunya membantu kita khusus nya bagi para pecinta anime.
           dan jika memang ada pihak yang keberatan dengan adanya bot/konten dari kami, silahkan lapor, agar kami proses.
           intinya buat kalian, jika kalian mampu menonton yang legal, lakukan. karena, itupun merupakan salah satu support ke pembuat anime tersebut.
           
           Terimakasih. - cccgnimexTeam.
            
        ),
        disable_web_page_preview=True,
        **kwargs,
    )
