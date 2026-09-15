# This file is a part of TG-FileStreamBot

from dataclasses import dataclass
import hashlib
from typing import Optional, Union
from datetime import datetime
from telethon import TelegramClient
from telethon.utils import get_input_location
from telethon.tl import types
from telethon.tl.patched import Message
from ..vars import Var

@dataclass
class FileInfo:
    __slots__ = ("file_size", "mime_type", "file_name", "upload_date", "id", "dc_id", "location")

    file_size: int
    mime_type: str
    file_name: str
    upload_date: datetime
    id: int
    dc_id: int
    location: Union[types.InputPhotoFileLocation, types.InputDocumentFileLocation]

class HashableFileStruct:
    def __init__(self, file_name: str, file_size: int, mime_type: str, file_id: int):
        self.file_name = file_name
        self.file_size = file_size
        self.mime_type = mime_type
        self.file_id = file_id

    def pack(self) -> str:
        hasher = hashlib.md5()
        fields = [self.file_name, str(self.file_size), self.mime_type, str(self.file_id)]

        for field in fields:
            hasher.update(field.encode())

        return hasher.hexdigest()

async def get_file_ids(client: TelegramClient, chat_id: int, message_id: int) -> Optional[FileInfo]:
    message: Message = await client.get_messages(chat_id, ids=message_id)
    if not message:
        return None
    return get_file_info(message)

def get_file_info(message: Message) -> FileInfo:
    media: Union[types.MessageMediaDocument, types.MessageMediaPhoto] = message.media
    file = getattr(media, "document", None) or getattr(media, "photo", None)
    return FileInfo(
        message.file.size,
        message.file.mime_type,
        getattr(message.file, "name", None) or "",
        message.date,
        file.id,
        *get_input_location(media)
    )

def pack_file(file_name: str, file_size: int, mime_type: str, file_id: int) -> str:
    return HashableFileStruct(file_name, file_size, mime_type, file_id).pack()

def get_short_hash(file_hash: str) -> str:
    return file_hash[:Var.HASH_LENGTH]
