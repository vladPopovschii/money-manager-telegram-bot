from aiogram import Bot, Dispatcher, executor, types
import logging
import config

import mongo_client
import models.user as user
import models.chat as chat
import models.payment as payment
import models.total as total

import keyboards.main
from utils import calc_totals, generate_history_markup, generate_loans, generate_markup, populate_username

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

client = mongo_client.init_mongo_client(config.MONGO_URI)
db = client.get_database('money_manager')

logging.info('Connected to database!')

users = user.User(db.get_collection('users'))
chats = chat.Chat(db.get_collection('chats'))
payments = payment.Payment(db.get_collection('payments'))
totals = total.Total(db.get_collection('totals'))


@dp.message_handler(commands='start')
async def start(message: types.Message):
    logging.info(message.from_user.id)
    if (users.user_exists(message.from_user.id) is False):
        users.register_user(message.from_user.id, message.from_user.full_name)

    if (chats.chat_exists(message.chat.id, message.from_user.id) is False):
        chats.register_chat(message.chat.id, message.from_user.id)

    try:
        await bot.send_message(message.chat.id, 'Menu', reply_markup=keyboards.main.kb_client)
        await message.delete()
    except:
        await bot.send_message(message.chat.id, 'Korvus blade, ' + message.from_user.full_name)


@dp.message_handler(commands='status')
async def add_payment(message: types.Message):

    paymentsList = payments.get_opened_payments(message.chat.id)
    totalMap = calc_totals(paymentsList)

    user_ids = []

    for user in totalMap:
        user_ids.append(user)

    populated_map = populate_username(totalMap, users.get_users_by_ids(user_ids))

    markup = generate_markup(populated_map)

    loans_markup = generate_loans(populated_map)

    payload = (markup + "\n\n" + loans_markup).strip()

    print(payload)

    text = payload if payload != '' else 'No data'

    await bot.send_message(message.chat.id, text, parse_mode='html')

@dp.message_handler(commands='make_payment')
async def make_payment(message: types.Message):
    args = message.get_args()

    if(args == ''):
        return await message.reply('Provide amount and/or description')

    arrayArgs = args.split(' ')

    if(len(arrayArgs) > 2):
        return await message.reply('Provide only amount and/or description')

    try:
        amount = float(arrayArgs[0])
        description = arrayArgs[1] if len(arrayArgs) == 2 else ''

        if (amount <= 0):
            return await message.reply('Invalid amount for ' + amount + ', should be positive number')

        payments.create_payment(
            message.chat.id,
            message.from_user.id,
            amount,
            description
        )

        return await message.reply('Payment successfully added')
            
    except:
        return await message.reply('Invalid amount, should be positive number')

@dp.message_handler(commands='history')
async def history(message: types.Message):
    payments_list = payments.get_payments(message.chat.id)
    user_ids_raw = set([])

    for payment in payments_list:
        user_ids_raw.add(payment["user_id"])

    user_ids = list(user_ids_raw)

    markup = generate_history_markup(payments_list, users.get_users_by_ids(user_ids))

    await bot.send_message(message.chat.id, "<b>Global history</b>\n" + markup, parse_mode='html')

@dp.message_handler(commands='make_total')
async def make_total(message: types.Message):
    total_id = totals.create_total(message.chat.id, payments.get_opened_payments(message.chat.id))
    payments.close_payments(message.chat.id)

    total_map = totals.get_total(message.chat.id, total_id)
    print(total_map)

    await bot.send_message(message.chat.id, "Total registered!", parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
