import config
import telebot
import requests
from PIL import Image
import io
import os
import time


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start"])


def send_welcome(message):
    bot.send_message(message.chat.id, "Hi. I can convert any sticker in "
    "PNG image.\n Just send me a sticker.")

@bot.message_handler(commands=["help"])


def halp(message):
    bot.send_message(message.chat.id, "Just send me a sticker and "
    "I will convert it in PNG.")


@bot.message_handler(content_types = ["sticker"])


def get_sticker(message):
    start = time.time()
    id = message.sticker.file_id
    path = "result/" +id+ ".webp"
    file_info = bot.get_file(id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, "wb") as new_file:
        new_file.write(downloaded_file)
    im = Image.open(path)
    bands = im.getbands()
    if 'X' in bands:
        im = im.convert("RGBA")
        im.save("result/" + id +".png")
        im.close()
    else:
        im.save("result/" + id +".png")
        im.close()

    imgsticker = open("result/" +id+".png", "rb")
    bot.send_document(message.chat.id, imgsticker)
    imgsticker.close()
    os.remove("result/" +id+ ".webp")
    os.remove("result/" +id+ ".png")
    end = time.time() - start
    bot.send_message(message.chat.id, "It took {0} sec".format(round(end, 2)))


def listener(message):
    for m in message:
        print (m)
bot.set_update_listener(listener)


bot.polling(none_stop=True)
