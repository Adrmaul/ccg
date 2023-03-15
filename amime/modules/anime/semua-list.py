from typing import Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message
from pyromod.helpers import ikb

from amime.amime import Amime


@Amime.on_message(filters.cmd(r"listsx$") & filters.private)
@Amime.on_callback_query(filters.regex(r"^listsx$"))
async def anime_menu(bot: Amime, union: Union[CallbackQuery, Message]):
    is_callback = isinstance(union, CallbackQuery)
    message = union.message if is_callback else union
    lang = union._lang

    keyboard = [
        [
            (lang.a_button, "a_lists anime 1"),
            (lang.b_button, "b_lists anime 1"),
            (lang.c_button, "c_lists anime 1"),
            (lang.d_button, "d_lists anime 1"),
            (lang.e_button, "e_lists anime 1"),
        ],
        [
            (lang.f_button, "f_lists anime 1"),
            (lang.g_button, "g_lists anime 1"),
            (lang.h_button, "h_lists anime 1"),
            (lang.i_button, "i_lists anime 1"),
            (lang.j_button, "j_lists anime 1"),
        ],
        [
            (lang.k_button, "k_lists anime 1"),
            (lang.l_button, "l_lists anime 1"),
            (lang.m_button, "m_lists anime 1"),
            (lang.n_button, "n_lists anime 1"),
            (lang.o_button, "o_lists anime 1"),
        ],
        [
            (lang.p_button, "p_lists anime 1"),
            (lang.q_button, "q_lists anime 1"),
            (lang.r_button, "r_lists anime 1"),
            (lang.s_button, "s_lists anime 1"),
            (lang.t_button, "t_lists anime 1"),
        ],
        [
            (lang.u_button, "u_lists anime 1"),
            (lang.v_button, "v_lists anime 1"),
            (lang.w_button, "w_lists anime 1"),
            (lang.x_button, "x_lists anime 1"),
            (lang.y_button, "y_lists anime 1"),
        ], 
        [
            (lang.z_button, "z_lists anime 1"),
            (lang.0_button, "0_lists anime 1"),
        ],      
    ]

    if is_callback:
        keyboard.append([(lang.back_button, "menu")])

    await (message.edit_text if is_callback else message.reply_text)(
        lang.listsx_text,
        reply_markup=ikb(keyboard),
    )