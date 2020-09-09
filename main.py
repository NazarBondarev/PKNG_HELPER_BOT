"""

PKNG-BOT v3.0
Date start develop: 03/09/2020
Date finish develop: -
Developer: Nazar Bondarev \ Telegram: @bonnaza

"""

import logging
import config
from aiogram import Bot, Dispatcher, executor, types, exceptions
from keyboards import Keyboards as keybs
import asyncio
from messages import MESSAGES
import re
import convertchanges

digits_pattern = re.compile(r'^[0-9]+ [0-9]+$', re.MULTILINE)


loop = asyncio.get_event_loop()
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop=loop)
logging.basicConfig(level=logging.INFO)

messages_ids = {}

@dp.message_handler(commands= ['start'])
async def starting(message: types.Message):
    name = message.from_user.first_name
    messages_ids[message.from_user.id] = message.message_id
    print(messages_ids)
    await message.answer(f'Привіт <b>{message.from_user.first_name}!</b>👋\n'
                         f'Я звичайний бот, який був розроблений спеціально для Полтавського коледжу нафти і газу\n'
                        f'"Національного університету Полтавська політехніка імені Юрія Кондратюка"'\
                        f'для зручного отримання розкладу та змін до нього!\n'\
                        f'Просто обери що тебе цікавить, нижче в меню👇\n\n'\
                        f'Контакти🔍\n'\
                        f'📍Наша адреса: вул. М.Грушевського, 2а\n'\
                        f'🕒Графік роботи коледжу: 08:00 - 17:00\n'\
                        f'🤖Бот працює 24/7\n'\
                        f'📲Контактний номер: +380997992161\n'\
                        f'📩Електронна адреса: pknghelper@ukr.net\n',
                         parse_mode='html',
                         reply_markup=general_menu_buttons)


@dp.callback_query_handler(lambda call: call.data == "help_for_dev")
async def test(call: types.CallbackQuery):
    PRICE = types.LabeledPrice(label='На мівінку розробнику', amount=500)

    await bot.send_invoice(
        call.message.chat.id,
        title=MESSAGES['tm_title'],
        description=MESSAGES['tm_description'],
        provider_token=config.PAYMENTS_PROVIDER_TOKEN,
        currency='uah',
        is_flexible=False,  # True если конечная цена зависит от способа доставки
        prices=[PRICE],
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use',
        reply_markup = payment_menu_buttons)
    print(call)

@dp.callback_query_handler(lambda call: call.data == "back_from_pay_menu")
async def back_to_general_from_payment(call: types.CallbackQuery):
    await bot.delete_message(call.message.chat.id, call.message.message_id)


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.callback_query_handler(lambda call: call.data in config.general_menu_buttons)
async def select_facult(call: types.CallbackQuery):

    if call.data == config.general_menu_buttons[0]:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="Що ж, обери свій факультет...",
                                    reply_markup = facults_menu_buttons)

    if call.data == config.general_menu_buttons[-1]:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=\
                                      f'Я звичайний бот, який був розроблений спеціально для Полтавського коледжу нафти і газу\n'
                                      f'"Національного університету Полтавська політехніка імені Юрія Кондратюка"'\
                                      f'для зручного отримання розкладу та змін до нього!\n'\
                                      f'Просто обери що тебе цікавить, нижче в меню👇\n\n'\
                                     f'Контакти🔍\n' \
                                     f'📍Наша адреса: вул. М.Грушевського, 2а\n' \
                                     f'🕒Графік роботи коледжу: 08:00 - 17:00\n' \
                                     f'🤖Бот працює 24/7\n' \
                                     f'📲Контактний номер: +380997992161\n' \
                                     f'📩Електронна адреса: pknghelper@ukr.net\n',
                                     parse_mode='html',
                                     reply_markup=general_menu_buttons)

    if call.data == config.general_menu_buttons[1]:
        changes = convertchanges.download_changes_from_site()
        changes = '\n\n'.join(changes)
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="Обери свою групу, і тут відображатимуться зміни конкретно для тебе! Також, ти будеш отримувати сповіщення якщо я знайду твою групу в змінах.\n\n"+changes,
                                    parse_mode='html',
                                    reply_markup=general_menu_buttons)
    if call.data == config.general_menu_buttons[2]:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="""
<b>Понеділок, вівторок, середа, четвер.</b>
0 пара	7.00 - 8.20
1 пара	8.30 - 9.50
2 пара	10.05 - 11.25
3 пара	12.15 - 13.35
4 пара	13.50 - 15.10
5 пара	15.25 - 16.45
6 пара	17.00 - 18.20
7 пара	18.35 - 19.55

<b>П'ятниця</b>
0 пара	7.00 - 8.20
1 пара	8.30 - 9.50
2 пара	10.05 - 11.25
3 пара	11.40 - 13.00
4 пара	13.15 - 14.35
5 пара	14.50 - 16.10
6 пара	16.25 - 17.45
7 пара	18.00 - 19.20
                        """,

                                parse_mode='html',
                                reply_markup=general_menu_buttons)







@dp.callback_query_handler(lambda call: call.data == 'В головне меню⬅'[0:10] or call.data == 'Назад⬅')
async def backs_to_menus(call: types.CallbackQuery):
    if call.data == 'В головне меню⬅'[0:10]:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="Ми знову в головному меню...\nУра?😐",
                                    reply_markup=general_menu_buttons)

    if call.data == 'Назад⬅':
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="Добре, повертаємося в меню вибору факультета...",
                                    reply_markup=facults_menu_buttons)

@dp.callback_query_handler(lambda call: call.data in facults_for_select_groups)
async def back_to_general_menu(call: types.CallbackQuery):

    groups_menu_buttons = keybs(keybs.keyboards).groups_select_menu(call.data)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="Прийшов час обрати свою групу...",
                                reply_markup=groups_menu_buttons)

@dp.callback_query_handler(lambda call: call.data)
async def view_group_menu(call: types.CallbackQuery):

    groups_menu_buttons = keybs(keybs.keyboards).groups_select_menu(call.data)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="Прийшов час обрати свою групу...",
                                reply_markup=groups_menu_buttons)


if __name__ == "__main__":
    general_menu_buttons = keybs(keybs.keyboards).upload_general_menu()
    facults_menu_buttons = keybs(keybs.keyboards).facults_select_menu()
    payment_menu_buttons = keybs(keybs.keyboards).payment_menu()

    facults_for_select_groups = [s[0:10] for s in config.facults_menu_buttons.keys()]

    executor.start_polling(dp, skip_updates=True)
