import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
from bs4 import BeautifulSoup

# Replace with your bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send me a URL and I will extract video and thumbnail URLs.')

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

async def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        videos, thumbnails = extract_urls(url)
        response_text = 'Videos:\n' + '\n'.join(videos) + '\n\nThumbnails:\n' + '\n'.join(thumbnails)
        await update.message.reply_text(response_text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text('There was an error processing the URL.')

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
