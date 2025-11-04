import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8525619391:AAG4nvNZbPCEKVKXA3UAJpJObnkgGBNA9Ek"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📍 Joylashuvni yuborish", request_location=True))
    bot.send_message(message.chat.id, "Salom! Men yaqin joylarni topuvchi botman.\nJoylashuvingizni yuboring 👇", reply_markup=kb)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat, lon = message.location.latitude, message.location.longitude

    rev_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10&addressdetails=1"
    resp = requests.get(rev_url, headers={'User-Agent': 'GeoBot'}).json()
    country = resp.get("address", {}).get("country", "Noma’lum mamlakat")
    display_name = resp.get("display_name", "Joy topilmadi")

    bot.send_message(
        message.chat.id,
        f"📍 Joylashuvingiz aniqlangan:\n<b>{display_name}</b>\n🌍 {country}",
        parse_mode="HTML"
    )

    kb = InlineKeyboardMarkup()
    categories = {
        "🍴 Restoran": "restaurant",
        "💊 Dorixona": "pharmacy",
        "🏧 Bankomat": "atm",
        "⛽️ Yoqilg‘i": "fuel",
        "🛍 Do‘kon": "supermarket",
        "🏫 Maktab": "school"
    }

    for k, v in categories.items():
        kb.add(InlineKeyboardButton(k, callback_data=f"{v}|{round(lat, 5)}|{round(lon, 5)}"))

    bot.send_message(message.chat.id, "Qaysi turdagi joylarni topay?", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    cat, lat, lon = call.data.split("|")
    lat, lon = float(lat), float(lon)

    bbox = f"{lon-0.02},{lat-0.02},{lon+0.02},{lat+0.02}"
    url = f"https://nominatim.openstreetmap.org/search?format=json&bounded=1&limit=5&q={cat}&viewbox={bbox}"

    resp = requests.get(url, headers={'User-Agent': 'GeoBot'})
    results = resp.json()

    if not results:
        bot.send_message(call.message.chat.id, "Hech narsa topilmadi 😕 (yaqin atrofda yo‘q)")
        return

    text = f"🗺 Eng yaqin joylar ({cat}):\n\n"
    for place in results:
        name = place.get('display_name', 'Noma’lum joy').split(',')[0]
        plat, plon = place['lat'], place['lon']
        map_link = f"https://www.google.com/maps?q={plat},{plon}"
        text += f"📍 <b>{name}</b>\n<a href='{map_link}'>Xaritada ko‘rish</a>\n\n"

    bot.send_message(call.message.chat.id, text, parse_mode="HTML")

bot.polling(none_stop=True)import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render'da o'zgaruvchi sifatida kiritamiz
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📍 Joylashuvni yuborish", request_location=True))
    bot.send_message(message.chat.id, "Salom! Men yaqin joylarni topuvchi botman.\nJoylashuvingizni yuboring 👇", reply_markup=kb)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat, lon = message.location.latitude, message.location.longitude

    rev_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10&addressdetails=1"
    resp = requests.get(rev_url, headers={'User-Agent': 'GeoBot'}).json()
    country = resp.get("address", {}).get("country", "Noma’lum mamlakat")
    display_name = resp.get("display_name", "Joy topilmadi")

    bot.send_message(
        message.chat.id,
        f"📍 Joylashuvingiz aniqlangan:\n<b>{display_name}</b>\n🌍 {country}",
        parse_mode="HTML"
    )

    kb = InlineKeyboardMarkup()
    categories = {
        "🍴 Restoran": "restaurant",
        "💊 Dorixona": "pharmacy",
        "🏧 Bankomat": "atm",
        "⛽️ Yoqilg‘i": "fuel",
        "🛍 Do‘kon": "supermarket",
        "🏫 Maktab": "school"
    }

    for k, v in categories.items():
        kb.add(InlineKeyboardButton(k, callback_data=f"{v}|{round(lat, 5)}|{round(lon, 5)}"))

    bot.send_message(message.chat.id, "Qaysi turdagi joylarni topay?", reply_markup=kb)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    cat, lat, lon = call.data.split("|")
    lat, lon = float(lat), float(lon)

    bbox = f"{lon-0.02},{lat-0.02},{lon+0.02},{lat+0.02}"
    url = f"https://nominatim.openstreetmap.org/search?format=json&bounded=1&limit=5&q={cat}&viewbox={bbox}"

    resp = requests.get(url, headers={'User-Agent': 'GeoBot'})
    results = resp.json()

    if not results:
        bot.send_message(call.message.chat.id, "Hech narsa topilmadi 😕 (yaqin atrofda yo‘q)")
        return

    text = f"🗺 Eng yaqin joylar ({cat}):\n\n"
    for place in results:
        name = place.get('display_name', 'Noma’lum joy').split(',')[0]
        plat, plon = place['lat'], place['lon']
        map_link = f"https://www.google.com/maps?q={plat},{plon}"
        text += f"📍 <b>{name}</b>\n<a href='{map_link}'>Xaritada ko‘rish</a>\n\n"

    bot.send_message(call.message.chat.id, text, parse_mode="HTML")

bot.polling(none_stop=True)