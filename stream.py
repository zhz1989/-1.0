# This file is a part of TG-FileStreamBot
# pylint: disable=relative-beyond-top-level

import logging
from telethon import Button, errors
from telethon.events import NewMessage
from telethon.extensions import html
from ..clients import StreamBot
from ..utils.file_properties import get_file_info, pack_file, get_short_hash
from ..vars import Var

MEDIA={"video", "audio"} # we can expand it to include more media types

@StreamBot.on(NewMessage(func=lambda e: True if e.message.file and e.is_private else False))
async def media_receive_handler(event: NewMessage.Event):
    user = await event.get_sender()
    if (Var.ALLOWED_USERS and user.id not in Var.ALLOWED_USERS) or (
        Var.BLOCKED_USERS and user.id in Var.BLOCKED_USERS):
        return await event.message.reply(
            message="抱歉，你不在允许使用本机器人的名单中。",
            link_preview=False,
            parse_mode=html
        )
    try:
        log_msg=await event.message.forward_to(Var.BIN_CHANNEL)
        file_info=get_file_info(log_msg)
        full_hash = pack_file(
            file_info.file_name,
            file_info.file_size,
            file_info.mime_type,
            file_info.id
        )
        file_hash=get_short_hash(full_hash)
        stream_link = f"{Var.URL}stream/{log_msg.id}?hash={file_hash}"
        is_media = bool(set(file_info.mime_type.split("/")) & MEDIA)
        buttons=[[Button.url("📥 下载", url=stream_link)]]
        message=f"<code>{stream_link}</code>"
        if is_media:
            buttons.append([Button.url("▶️ 在线播放", url=stream_link+"&s=1")])
            message+=f"<a href='{stream_link}&s=1'>（在线播放）</a>"
        await event.message.reply(
            message=message,
            link_preview=False,
            buttons=buttons,
            parse_mode=html
        )
    except errors.FloodWaitError as e:
        logging.error(e)
