import os
import logging
import time
from telegram.ext import Updater, MessageHandler, Filters


channels = map(int, os.environ.get("channels").split())
main_channel = int(os.environ.get("main_channel", 0))


def broadcast(update, context):
    logger.info("Broadcast Triggered!")
    logger.info(f"Forwarding to {list(channels)}")
    for channel in channels:
        logger.info(f"Forwarding to {channel}")
        update.effective_message.forward(chat_id=channel)
        time.sleep(1.0)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
bot_api = str(os.environ.get("bot_api", None))
app_url = str(os.environ.get("app_url", None))
PORT = int(os.environ.get('PORT', 5000))
updater = Updater(token=bot_api)
dispatcher = updater.dispatcher

# Handler(s)
broadcast_handler = MessageHandler(
    ~Filters.update.edited_message & Filters.chat(main_channel), broadcast)

# Add Handler(s) to dispatcher
dispatcher.add_handler(broadcast_handler)

# Start bot
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=bot_api,
                      webhook_url=app_url + bot_api)
logger.info("Using Webhooks")
