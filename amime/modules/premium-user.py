from typing import Dict, Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime
from amime.config import CHANNELS, GROUPS


@Amime.on_message(filters.cmd(r"premium$"))
@Amime.on_callback_query(filters.regex(r"^premium$"))
async def about(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    kwargs: Dict = {}

    is_private = await filters.private(bot, message)
    if is_private and is_callback:
        keyboard = [
            [
                (lang.Next, "premium1"),
            ],
            [
                (lang.back_button, "start"),
            ],
        ]
        kwargs["reply_markup"] = ikb(keyboard)

    await (message.edit_text if is_callback else message.reply_text)(
        lang.premium_text.format(
            bot_name=bot.me.first_name,
            github="<a href='t.me/Rizki_Wahyudi03'>Owner</a>",
            channel=f"<a href='https://t.me/downloadanimebatch/'>{lang.channel}</a>",
            group=f"<a href='https://t.me/c/{str(GROUPS[lang.code])[4:]}/-1'>{lang.group}</a>",
            otakudesu="<a href='https://otakudesu.io'>Otakudesu</a>",
            kusonime="<a href='https://kusonime.com/'>Kusonime</a>",
            samehadaku="<a href='https://194.163.183.129/'>Samehadaku</a>",
            oplovers="<a href='https://oploverz.asia/'>Oplovers</a>",
            bakadame="<a href='https://bakadame.com/'>Bakadame</a>",
            koenime="<a href='https://koenime.com/'>Koenime</a>",

        ),
        disable_web_page_preview=True,
        **kwargs,
    )