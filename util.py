# This file is a part of TG-FileStreamBot

import logging
import importlib.util
from collections import defaultdict
from pathlib import Path
from aiohttp import web

from telethon import TelegramClient
from telethon.tl import functions
from ..vars import Var

ongoing_requests: dict[str, int] = defaultdict(lambda: 0)

def load_plugins(folder_path: str):
    folder = Path(folder_path)
    package_prefix = ".".join(folder.parts)
    for file in folder.glob("*.py"):
        module_name = f"{package_prefix}.{file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, str(file))
        module = importlib.util.module_from_spec(spec)
        module.__package__ = package_prefix
        spec.loader.exec_module(module)
        logging.info("Imported %s", module_name)


def get_requester_ip(req: web.Request) -> str:
    if Var.TRUST_HEADERS:
        try:
            return req.headers["X-Forwarded-For"].split(", ")[0]
        except KeyError:
            pass
    peername = req.transport.get_extra_info('peername')
    if peername is not None:
        return peername[0]

def allow_request(ip: str) -> None:
    return ongoing_requests[ip] < Var.REQUEST_LIMIT

def increment_counter(ip: str) -> None:
    ongoing_requests[ip] += 1

def decrement_counter(ip: str) -> None:
    ongoing_requests[ip] -= 1


# Moved from utils/time_format.py
def get_readable_time(seconds: int) -> str:
    count = 0
    readable_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", " days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        readable_time += time_list.pop() + ", "
    time_list.reverse()
    readable_time += ": ".join(time_list)
    return readable_time

async def startup(client: TelegramClient):
    config = await client(functions.help.GetConfigRequest())
    for option in config.dc_options:
        if option.ip_address == client.session.server_address:
            if client.session.dc_id != option.id:
                logging.warning("Fixed DC ID in session from %s to %s",client.session.dc_id,option.id)
            client.session.set_dc(option.id, option.ip_address, option.port)
            client.session.save()
            break
    # transfer.post_init()
