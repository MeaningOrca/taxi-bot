from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Поделиться своим номером телефона', request_contact=True)
)
location = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Отправить свою геопозицию", request_location=True)
)
