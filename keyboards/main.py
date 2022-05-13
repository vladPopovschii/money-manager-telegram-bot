from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton('/status')
b2 = KeyboardButton('/make_payment')
b3 = KeyboardButton('/history')
b4 = KeyboardButton('/make_total')

kb_client = ReplyKeyboardMarkup()

kb_client.add(b1).add(b2).add(b3).add(b4)