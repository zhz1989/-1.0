# This file is a part of TG-FileStreamBot
# pylint: disable=relative-beyond-top-level

from telethon.extensions import html
from telethon.events import NewMessage
from .. import __version__
from ..clients import StreamBot
from ..utils.greetings import greeting
from ..vars import Var

@StreamBot.on(NewMessage(incoming=True,pattern=r"^\/start*", func=lambda e: e.is_private))
async def start(event: NewMessage.Event):
    user = await event.get_sender()
    if (Var.ALLOWED_USERS and user.id not in Var.ALLOWED_USERS) or (
        Var.BLOCKED_USERS and user.id in Var.BLOCKED_USERS):
        return await event.message.reply(
            message="抱歉，你不在允许使用本机器人的名单中。",
            link_preview=False,
            parse_mode=html
        )
    await event.message.reply(
        message=f'{greeting()} <a href="tg://user?id={user.id}">{user.first_name}</a>, 发送任意文件给我，立即获得在线播放/下载直链。',
        link_preview=False,
        parse_mode=html
    )

@StreamBot.on(NewMessage(incoming=True,pattern=r"^\/about*", func=lambda e: e.is_private))
async def about(event: NewMessage.Event):
    await event.message.reply(
        message=f"""
维护者： <a href="https://github.com/DeekshithSH">DeekshithSH</a>
源码： <a href="https://github.com/SpringsFern/TG-FileStreamBot">TG-FileStreamBot</a>
基于： [<a href="https://github.com/tulir/TGFileStream/">tg filestream</a>] [<a href="https://github.com/EverythingSuckz/TG-FileStreamBot">TG-FileStreamBot</a>]
版本： {__version__}
最后更新： 08 April 2025
""",
        link_preview=False,
        parse_mode=html
    )
