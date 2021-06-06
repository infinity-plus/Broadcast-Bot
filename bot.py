import os
import logging
from telegram.ext import Updater, MessageHandler, Filters


channels = map(int, os.environ.get("channels").split())


def broadcast(update, context):
    for channel in channels:
        update.message.forward(chat_id=channel)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
bot_api = str(os.environ.get("bot_api", None))
app_url = str(os.environ.get("app_url", None))
PORT = int(os.environ.get('PORT', 5000))
updater = Updater(token=bot_api)
dispatcher = updater.dispatcher

# Handler(s)
broadcast_handler = MessageHandler(
    ~Filters.update.edited_message, broadcast)

# Add Handler(s) to dispatcher
dispatcher.add_handler(broadcast_handler)

# Start bot
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=bot_api)
updater.bot.setWebhook(app_url + bot_api)