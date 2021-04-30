"""

PKNG-BOT v3.0
Date start develop: 03/09/2020
Date finish develop: -
Developer: Nazar Bondarev \ Telegram: @bonnaza

"""


from getchanges import GetChanges as Gt
import logging
import re
import datetime
import config
import json
from aiogram import Bot, Dispatcher, executor, types, exceptions
from keyboards import Keyboards as keybs
import asyncio
import re
from json import JSONDecodeError

digits_pattern = re.compile(r'^[0-9]+ [0-9]+$', re.MULTILINE)
loop = asyncio.get_event_loop()
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop=loop)
logging.basicConfig(level=logging.INFO)
messages_ids = {}
days_associations = {
    "Monday": 'понеділок',
    "Tuesday": 'вівторок',
    "Wednesday": 'середу',
    "Thursday": 'четвер',
    "Friday":"п'ятницю"
}

months_associations = {
    'December': 'грудня',
    'January': 'січня',
    'February':'лютого',
    'March': 'березня',
    'April': 'квітня',
    'May': 'травня',
    'June': 'червня',
    'July':'липня',
    'August':'серпня',
    'September':'вересня',
    'October':'жовтня',
    'November':'листопада'
}




@dp.message_handler(commands= ['start'])
async def starting(message: types.Message):

    if str(message.from_user.id) not in users.keys():
        users[str(message.from_user.id)] = {
            "name": message.from_user.first_name,
            "surname": message.from_user.last_name,
            "username": message.from_user.username,
            "group": "pass"
        }
        await update_users_data(message, users, "new_member")

    name = message.from_user.first_name
    messages_ids[message.from_user.id] = message.message_id
    await message.answer(f'Привіт <b>{message.from_user.first_name}!</b>👋\n'
                         f'Я звичайний бот, який був розроблений спеціально для Полтавського коледжу нафти і газу\n'
                        f'"Національного університету Полтавська політехніка імені Юрія Кондратюка"'\
                        f' для зручного отримання розкладу та змін до нього!\n'\
                        f'Просто обери що тебе цікавить, нижче в меню👇\n\n'\
                        f'Контакти🔍\n'\
                        f'📍Наша адреса: вул. М.Грушевського, 2а\n'\
                        f'🕒Графік роботи коледжу: 08:00 - 17:00\n'\
                        f'🤖Бот працює 24/7\n'\
                        f'📞Контакти адміністрації: тел./факс: (0532) 63-81-48\n'\
                        f'📩Електронна адреса: pknghelper@ukr.net\n',
                         parse_mode='html',
                         reply_markup=general_menu_buttons)
@dp.message_handler(commands= ['info'])
async def info(message: types.Message):
    await bot.send_message(message.chat.id,
                        f'Чат-бот, який був розроблений спеціально для Полтавського коледжу нафти і газу\n'
                        f'"Національного університету Полтавська політехніка імені Юрія Кондратюка"'\
                        f' для зручного отримання розкладу та змін до нього!\n'\
                        f'Контакти🔍\n'\
                        f'📍Наша адреса: вул. М.Грушевського, 2а\n'\
                        f'🕒Графік роботи коледжу: 08:00 - 17:00\n'\
                        f'🤖Бот працює 24/7\n'\
                        f'📞Контакти адміністрації: тел./факс: (0532) 63-81-48\n'\
                        f'📩Електронна адреса: pknghelper@ukr.net\n')
@dp.message_handler(commands=['m'])
async def malling(message: types.Message):
    if message.from_user.id == 366954921:
        format_malling = message.text.replace("/m", "")
        i = 0
        for item in users.keys():
            try:
                await bot.send_message(int(item), format_malling)
                i+=1
            except (exceptions.BotBlocked, exceptions.UserDeactivated):
                continue
        await bot.send_message(366954921, f"Рассылку получили {i} пользователей")
@dp.callback_query_handler(lambda call: call.data in config.general_menu_buttons)
async def select_facult(call: types.CallbackQuery):
    global group_changes
    try:
        if call.data == config.general_menu_buttons[0] and users[str(call.from_user.id)]['group'] == 'pass':
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text="Що ж, обери свій факультет...",
                                        reply_markup = facults_menu_buttons)
    except KeyError:
        users[str(call.from_user.id)] = {
            "name": call.from_user.first_name,
            "surname": call.from_user.last_name,
            "username": call.from_user.username,
            "group": "pass"
        }
        await update_users_data(call, users, "new_member")
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="Що ж, обери свій факультет...",
                                    reply_markup=facults_menu_buttons)



    if call.data == config.general_menu_buttons[0] and users[str(call.from_user.id)]['group'] != 'pass':
        group_menu_keyboard = keybs(keybs.keyboards).group_menu(users[str(call.from_user.id)]['group'])

        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=
                                    f"Меню групи: <b>{users[str(call.from_user.id)]['group']}</b>\n\n"
                                    f"👇 Дізнайся розклад своєї групи який тебе цікавить за допомогою меню нижче",
                                    parse_mode='html', reply_markup=group_menu_keyboard)

    if call.data == config.general_menu_buttons[-1]:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=\
                                      f'Я звичайний чат-бот, який був розроблений спеціально для Полтавського коледжу нафти і газу\n'
                                      f'"Національного університету Полтавська політехніка імені Юрія Кондратюка" '\
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
        result = Gt().get_changes()
        if result:
            await bot.send_photo(chat_id = call.message.chat.id, photo=open("./data/zm.jpg", "rb"))



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
async def select_group(call: types.CallbackQuery):

    groups_menu_buttons = keybs(keybs.keyboards).groups_select_menu(call.data)
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text="Прийшов час обрати свою групу...",
                                reply_markup=groups_menu_buttons)

@dp.callback_query_handler(lambda call: call.data in groups_list or call.data == "back_to_general_menu" and call.data != "Назад⬅")
async def save_user_group_and_view_group_menu(call: types.CallbackQuery):


    if call.data in groups_list:
        users[str(call.from_user.id)]['group'] = call.data
        await update_users_data(call, users, "new_group_select")
        group_menu_keyboard = keybs(keybs.keyboards).group_menu(call.data)

        await bot.edit_message_text(chat_id=call.message.chat.id,
                                   message_id = call.message.message_id,
                                   text=
                                   f"😑 Ми тебе запам'ятали\n\n"
                                   f"🥳 Вітаю в меню групи <b>{call.data}</b>\n"
                                   f"👇 Дізнайся розклад своєї групи який тебе цікавить за допомогою меню нижче",
                                   parse_mode='html', reply_markup=group_menu_keyboard)

    if call.data == "back_to_general_menu":
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="Ми знову в головному меню...\nУра?😐",
                                    reply_markup=general_menu_buttons)



async def update_users_data(user, users, status):
    try:
        with open("./data/users.json", 'w', encoding='UTF-8') as update_data:
            json.dump(users, update_data, ensure_ascii=False, indent=4)

            if status == "new_member":
                await bot.send_message(config.admin, f"""Додано нового користувача:
<b>
Ім'я: {user.from_user.first_name}  
Фамілія: {user.from_user.last_name}
Юзернейм: @{user.from_user.username}
id: {user.from_user.id}
</b>
        """, parse_mode='html')
            elif status == "new_group_select":
                await bot.send_message(config.admin, f"""Користувач обрав групу {users[str(user.from_user.id)]['group']}:
<b>
Ім'я: {user.from_user.first_name}  
Фамілія: {user.from_user.last_name}
Юзернейм: @{user.from_user.username}
id: {user.from_user.id}
</b>
        """, parse_mode='html')

    except JSONDecodeError as e:
        await bot.send_message(config.admin,f"Не вдалося записати нові дані про користувача. Помилка: \n <code>{e}</code>", parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data in config.group_menu)
async def group_menu_func(call: types.CallbackQuery):
    group_menu_keyboard = keybs(keybs.keyboards).group_menu(call.data)
    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days=1)

    try:
        if call.data == config.group_menu[0]:
            print(timetable[users[str(call.from_user.id)]['group']]['Monday'])
            await bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text=f"Розклад на <b>{days_associations[today.strftime('%A')]}</b> "\
                                             f"{today.strftime('%d')} {months_associations[today.strftime('%B')]} {today.strftime('%Y')} року\n\n"+
                                             '\n'.join(timetable[users[str(call.from_user.id)]['group']][today.strftime("%A")]),
                                        parse_mode='html',reply_markup=group_menu_keyboard)

        elif call.data == config.group_menu[1]:
            await bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text=f"Розклад на <b>{days_associations[tomorrow.strftime('%A')]}</b> "\
                                             f"{tomorrow.strftime('%d')} {months_associations[tomorrow.strftime('%B')]} {today.strftime('%Y')} року\n\n"+
                                                           '\n'.join(timetable[users[str(call.from_user.id)]['group']][tomorrow.strftime("%A")]),
                                        parse_mode='html', reply_markup=group_menu_keyboard)

        elif call.data == config.group_menu[2]:
            group = timetable[users[str(call.from_user.id)]['group']]
            week_timetable = """
Розклад на тиждень:\n
<b>Понеділок</b>
{0}\n\n
<b>Вівторок</b>
{1}\n\n
<b>Середа</b>
{2}\n\n
<b>Четвер</b>
{3}\n\n
<b>П`ятниця</b>
{4}\n\n""".format('\n'.join(group['Monday']),
                  '\n'.join(group['Tuesday']),
                  '\n'.join(group['Wednesday']),
                  '\n'.join(group['Thursday']),
                  '\n'.join(group['Friday']))

            await bot.edit_message_text(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        text=week_timetable,
                                        parse_mode='html', reply_markup=group_menu_keyboard)
        elif call.data == config.group_menu[3]:
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text="Що ж, обери свій факультет...",
                                        reply_markup=facults_menu_buttons)


    except exceptions.MessageNotModified:
        pass




if __name__ == "__main__":
    group_changes = ''

    general_menu_buttons = keybs(keybs.keyboards).upload_general_menu()
    facults_menu_buttons = keybs(keybs.keyboards).facults_select_menu()

    facults_for_select_groups = [s[0:10] for s in config.facults_menu_buttons.keys()]

    #Збираємо групи поодинично для обробника вибора своєї групи
    groups_list = []
    for groups_lists in config.facults_menu_buttons.values():
        for groups in groups_lists:
            groups_list.append(groups)
   
    with open('./data/users.json', 'r', encoding='UTF-8') as read_users:
        users = json.load(read_users)

    with open('./data/data.json', 'r', encoding='UTF-8') as read_timetable:
        timetable = json.load(read_timetable)

    executor.start_polling(dp, skip_updates=True)
