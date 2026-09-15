# This file is a part of TG-FileStreamBot

import sys
import asyncio
import traceback
import logging
import logging.handlers as handlers

from aiohttp import web
from .stream_routes import routes
from .utils.keepalive import ping_server
from .utils.util import load_plugins, startup
from .clients import StreamBot, initialize_clients
from .vars import Var

logging.basicConfig(
    level=logging.DEBUG if Var.DEBUG else logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(name)s][%(levelname)s] ==> %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout),
              handlers.RotatingFileHandler("streambot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8")],)

logging.getLogger("aiohttp").setLevel(logging.DEBUG if Var.DEBUG else logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.DEBUG if Var.DEBUG else logging.ERROR)
logging.getLogger("telethon").setLevel(logging.INFO if Var.DEBUG else logging.ERROR)

app = web.Application(client_max_size=1024*8) # 8KB
app.add_routes(routes)
server = web.AppRunner(app)

async def start_services():
    logging.info("Initializing Telegram Bot")
    await StreamBot.start(bot_token=Var.BOT_TOKEN)
    await startup(StreamBot)
    try:
        peer = await StreamBot.get_entity(Var.BIN_CHANNEL)
    except ValueError:
        logging.error("Bin Channel not found. Please ensure the bot has been added to the bin channel.")
        return
    bot_info = await StreamBot.get_me()
    Var.USERNAME = bot_info.username
    Var.FIRST_NAME=bot_info.first_name
    logging.info("Initialized Telegram Bot")
    logging.info("Initializing Clients")
    await initialize_clients()
    if peer.megagroup:
        if Var.MULTI_CLIENT:
            logging.error("Bin Channel is a group. It must be a channel; multi-client won't work with groups.")
            return
        else:
            logging.warning("Bin Channel is a group. Use a channel for multi-client support.")
    if not Var.NO_UPDATE:
        logging.info('Importing plugins')
        load_plugins("WebStreamer/plugins")
        logging.info("Imported Plugins")
    if Var.KEEP_ALIVE:
        logging.info("Starting Keep Alive Service")
        asyncio.create_task(ping_server())
    logging.info("Initializing Web Server")
    await server.setup()
    await web.TCPSite(server, Var.BIND_ADDRESS, Var.PORT).start()
    logging.info("Service Started")
    logging.info("bot =>> %s", Var.FIRST_NAME)
    logging.info("DC ID =>> %s", str(StreamBot.session.dc_id))
    logging.info(" URL =>> %s", Var.URL)
    await StreamBot.run_until_disconnected()

async def main():
    try:
        await start_services()
    finally:
        await cleanup()
        logging.info("Stopped Services")

async def cleanup():
    await server.cleanup()
    await StreamBot.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception:
        logging.error(traceback.format_exc())
