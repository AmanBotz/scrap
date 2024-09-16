import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace with your bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a URL and I will extract video and thumbnail URLs.')

def extract_urls(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    videos = set()
    thumbnails = set()

    # Example of extracting video and thumbnail URLs
    for video in soup.find_all('video'):
        for source in video.find_all('source'):
            videos.add(source.get('src'))

    for img in soup.find_all('img'):
        thumbnails.add(img.get('src'))

    return videos, thumbnails

def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        videos, thumbnails = extract_urls(url)
        response_text = 'Videos:\n' + '\n'.join(videos) + '\n\nThumbnails:\n' + '\n'.join(thumbnails)
        update.message.reply_text(response_text)
    except Exception as e:
        logger.error(f"Error: {e}")
        update.message.reply_text('There was an error processing the URL.')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
