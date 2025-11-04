# bot.py

import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Bot tokeningizni shu yerga yozing
BOT_TOKEN = "8525619391:AAG4nvNZbPCEKVKXA3UAJpJObnkgGBNA9Ek"
bot = telebot.TeleBot(BOT_TOKEN)

# /start komandasi
@bot.message_handler(commands=['start'])
def start_cmd(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📍 Geolokatsiya yuborish"))
    bot.send_message(message.chat.id, "Salom! Geolokatsiya botiga xush kelibsiz.", reply_markup=kb)

# Geolokatsiya tugmasi bosilganda
@bot.message_handler(func=lambda message: message.text == "📍 Geolokatsiya yuborish")
def location_request(message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("Joylashuvni yuborish", request_location=True))
    bot.send_message(message.chat.id, "Iltimos, joylashuvingizni yuboring:", reply_markup=kb)

# Foydalanuvchi location yuborganda
@bot.message_handler(content_types=['location'])
def location_received(message):
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(message.chat.id, f"Sizning koordinatalaringiz:\nLatitude: {lat}\nLongitude: {lon}")

# Botni 24/7 ishlatish uchun polling alohida satrda
if __name__ == "__main__":
    bot.polling(none_stop=True)