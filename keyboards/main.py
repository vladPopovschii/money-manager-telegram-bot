from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton('/status')
b2 = KeyboardButton('/info')
b3 = KeyboardButton('/make_payment')
b4 = KeyboardButton('/history')
b5 = KeyboardButton('/make_total')

kb_client = ReplyKeyboardMarkup()

# TODO add make_total functionality
kb_client.add(b1).add(b2).add(b3).add(b4)
