import os
from typing import Final
from dotenv import load_dotenv

import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import requests

# Load environment variables
load_dotenv()

print('Starting up bot...')

TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_USERNAME: Final = os.getenv("TELEGRAM_BOT_USERNAME")
RAPIDAPI_KEY: Final = os.getenv("RAPIDAPI_KEY")

if not all([TOKEN, BOT_USERNAME, RAPIDAPI_KEY]):
    raise ValueError("Missing required environment variables. Please check your .env file.")

global bot
bot = telegram.Bot(TOKEN)

# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    await update.message.reply_text("Waku waku! Hi there! I'm Anya! I'm a super special girl with telepathic powers. I can read minds, isn't that amazing? My mommy and daddy are Loid and Yor, but they're not really my real parents. We're a spy family, you see! We go on exciting missions together and try to keep our secrets hidden from the world. Oh, and I love cookies and fluffy animals! They make me go all waku waku!")
    await bot.sendMessage(chat_id = chat_id, text = "It is so nice to meet you! How can I help you today? You can type '/help' if you need help :D")


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Waku waku! Of course, I'd love to help you! What do you need assistance with?")
    await update.message.reply_text("Here are a few things Anya can do:\n- Anya can tell jokes (/random)\n \nSo, what can I do to help you today?")


# Lets us use the /random command
async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())

    joke = response.json()

    # Extract setup and punchline
    setup = joke['body'][0]['setup']
    punchline = joke['body'][0]['punchline']

    print("Setup:", setup)
    print("Punchline:", punchline)

    chat_id = update.message.chat.id
    await bot.sendMessage(chat_id=chat_id, text=setup)
    await bot.sendMessage(chat_id=chat_id, text=punchline)
    await bot.sendAnimation(chat_id=chat_id, animation="https://tenor.com/view/anya-smile-spy-x-family-anya-gif-25728724")

    # For replies, use the following
    # msg_id = update.message.message_id
    # await update.message.reply_text('Insert your joke here')


def handle_response(text: str) -> str:
    return "Waku waku! That's a bit too hard for Anya to understand :(\nPlease only type the commands starting with a '/' :D"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group' or message_type == 'supergroup':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('random', random_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling()
