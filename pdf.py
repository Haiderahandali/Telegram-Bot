#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import bot_tok

BOT_TOKEN = bot_tok.tokn
cmd_convert = "convert_word_to_pdf.sh "
cmd_delete = "rm "

bot_dir = "/home/alia/bot-dir/"
outdir= "/home/alia/pdfs/"

import logging
import subprocess

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, please send me a file to convert it to pdf!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('The Bot Only convert Single files, pptx, docx, txt, HTML, Images such as PNG, JPEG and so on.')


def proc(command,fName):
    subprocess.run(command + fName,shell=True)
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def downloader_photo(update, context):
    chat_id = update.message.chat_id
    filename = update.message.photo.file_name
    filepath = outdir+filename.rsplit(".",1)[0]+".pdf"

#    print("I am downloading ------------------------\n\n ")
    update.message.photo.get_file().download(bot_dir+filename)
 #   print("\n this is the bot name and dir name  ", bot_dir+filename)
    proc(cmd_convert,r'''"'''+bot_dir+filename+r'''"''')
    filepath = outdir+filename.rsplit(".",1)[0]+".pdf"
#    print(filename)
    context.bot.send_document(chat_id=chat_id, document=open(filepath, 'rb'))
    update.message.reply_text('Done!')
    proc(cmd_delete,r'''"'''+filepath+r'''"''')
    proc(cmd_delete,r'''"'''+bot_dir+filename+r'''"''')


def downloader_document(update, context):
    chat_id = update.message.chat_id
    filename = update.message.document.file_name
    filepath = outdir+filename.rsplit(".",1)[0]+".pdf"
    ext = filename.rsplit(".",1)[1]
    if ext == "pdf":
        update.message.reply_text("The file is already pdf ")
        return

    update.message.document.get_file().download(bot_dir+filename)

    proc(cmd_convert,r'''"'''+bot_dir+filename+r'''"''')
    filepath = outdir+filename.rsplit(".",1)[0]+".pdf"

    context.bot.send_document(chat_id=chat_id, document=open(filepath, 'rb'))
    update.message.reply_text('Done!')
    proc(cmd_delete,r'''"'''+filepath+r'''"''')
    proc(cmd_delete,r'''"'''+bot_dir+filename+r'''"''')
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    ### dp.add_handler(MessageHandler(Filters.text, echo))
    # on recieve a file, download it.

    dp.add_handler(MessageHandler(Filters.document, downloader_document))

    dp.add_handler(MessageHandler(Filters.photo, downloader_photo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
