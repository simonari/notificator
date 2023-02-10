from django.core.management.base import BaseCommand

from telegram import Update
from telegram.ext import Application
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from telegram.ext import filters

from .base.db import savers, get_n_save
from .base.db.getters import objects, fields, bulk

from .base import send
from .base import data

# Loading telegram bot token from .env file
from dotenv import load_dotenv, find_dotenv
from os import environ

load_dotenv(find_dotenv())
BOT_TOKEN = environ['TELEGRAM_BOT_TOKEN']


def error_handler(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:

            print(f"[!] Error occurred during work of bot!\n")
            #       f"[!] Error: {e}")

    return wrapper


async def tg_error_handler(update: Update, context: CallbackContext) -> None:
    print(context.error)
    print(context.error.__traceback__)
    await update.message.reply_text("Возникла ошибка в работе бота!")


TYPING_ID, = range(1)


@error_handler
async def cmd_help(update: Update, context: CallbackContext) -> None:
    mi = 1282

    last_update, _ = await data.get_manga_data(mi)

    await update.message.reply_text(last_update)


@error_handler
async def cmd_start(update: Update, context: CallbackContext) -> None:
    pass


@error_handler
async def cmd_link(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Введите ваш ID на MangaLib:")

    return TYPING_ID


@error_handler
async def input_link(update: Update, context: CallbackContext) -> int:
    ti = update.message.chat_id
    pi = update.message.text

    if not pi.isdecimal():
        await update.message.reply_text("ID должен содержать только числа 0-9.")
        return -1

    # TODO
    #   * On re-link:
    #   *   Deleting previous profile info

    # Saving user data
    user = await savers.user(ti, pi)
    # Saving manga data and reference between user and manga
    await get_n_save.manga_data(user)

    await update.message.reply_text(f"Ваши данные были сохранены!")

    return ConversationHandler.END


@error_handler
async def cmd_get(update: Update, context: CallbackContext) -> None:
    # Getting telegram and MangaLib profile id
    # From chat
    ti = update.message.chat_id
    # From User table by telegram id
    pi = await fields.user_pi(ti)

    print(f"tg id: {ti}")
    print(f"mangalib id: {pi}")

    mis = await bulk.mis_ref(ti)

    # Iterating through it
    bot = update.get_bot()
    async for mi in mis:
        print(f"Manga id: {mi}")
        await send.new_chapter(bot, ti, mi, pi)


class Command(BaseCommand):
    help = "Starts Telegram bot"

    def handle(self, *args, **options):
        # Creating a bot object
        application = Application.builder().token(BOT_TOKEN).build()

        # Custom conversation handlers
        profile_id_handler = ConversationHandler(
            entry_points=[CommandHandler("link", cmd_link)],
            states={
                TYPING_ID: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, input_link)
                ]
            },
            fallbacks=[]
        )

        # Adding conversation handlers
        application.add_handler(profile_id_handler)

        # Adding command handlers
        application.add_handler(CommandHandler("help", cmd_help))
        application.add_handler(CommandHandler("get", cmd_get))

        # Adding message handlers

        # Adding error handlers
        application.add_error_handler(tg_error_handler)

        # Starting bot
        print(f"[+] Starting bot...")
        application.run_polling()
