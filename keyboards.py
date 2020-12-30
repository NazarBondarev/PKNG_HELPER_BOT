from aiogram import types
import config

class Keyboards:
    keyboards = {}

    def __init__(self, keyboards):
        """Ініціалізуємо об'єкт, тобто словник для роботи з клавіатурами бота"""

        self.keyboards = keyboards

    def upload_general_menu(self):
        """Додаємо кнопки головного меню в об'єкт клавіатури та повертаємо його"""

        self.keyboards['general_menu_keyboard'] = types.InlineKeyboardMarkup()

        for button in config.general_menu_buttons:
            self.keyboards['general_menu_keyboard'].add(types.InlineKeyboardButton(text=button, callback_data=button))

        self.keyboards['general_menu_keyboard'].add(types.InlineKeyboardButton(text="Ми на мапі🗺", url="https://goo.gl/maps/4wa4ePvYPPr9JQzf7"))
        self.keyboards['general_menu_keyboard'].add(types.InlineKeyboardButton(text="Підтримка💪", url="https://t.me/bonnaza"))
        self.keyboards['general_menu_keyboard'].add(types.InlineKeyboardButton(text="COVID-19 корисна інформація🦠", url="https://t.me/COVID19_Ukraine"))




        return self.keyboards["general_menu_keyboard"]


    def facults_select_menu(self):
        """Додаємо кнопки для вибору факультету"""

        self.keyboards['facults_menu_keyboard'] = types.InlineKeyboardMarkup()

        for button in config.facults_menu_buttons.keys():
            self.keyboards['facults_menu_keyboard'].add(types.InlineKeyboardButton(text=button, callback_data=button[0:10]))

        return self.keyboards['facults_menu_keyboard']

    def groups_select_menu(self, facult):
        """Додаємо кнопки вибору групи"""

        self.facult = facult

        for item in config.facults_menu_buttons.keys():
            if item[0:10] == self.facult:
                need_group = config.facults_menu_buttons[item]

        self.keyboards[self.facult] = types.InlineKeyboardMarkup()

        for button in need_group:
            self.keyboards[self.facult].add(types.InlineKeyboardButton(text=button, callback_data=button))

        return self.keyboards[self.facult]

    def group_menu(self, group):
        """Додаємо меню групи"""

        self.group = group

        self.keyboards[self.group] = types.InlineKeyboardMarkup(row_width=3)

        today_button = types.InlineKeyboardButton(text=config.group_menu[0], callback_data=config.group_menu[0])
        tomorrow_button = types.InlineKeyboardButton(text=config.group_menu[1], callback_data=config.group_menu[1])
        weekday_button = types.InlineKeyboardButton(text=config.group_menu[2], callback_data=config.group_menu[2])
        change_group_button = types.InlineKeyboardButton(text=config.group_menu[3], callback_data=config.group_menu[3])

        self.keyboards[self.group].add(today_button, tomorrow_button, weekday_button)
        self.keyboards[self.group].add(change_group_button)



        self.keyboards[self.group].add(types.InlineKeyboardButton(text="В головне меню⬅", callback_data="back_to_general_menu"))


        return self.keyboards[self.group]









