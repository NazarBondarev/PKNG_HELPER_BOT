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

        self.keyboards['general_menu_keyboard'].add(types.InlineKeyboardButton(text="Пожертва розробнику👨‍💻", callback_data="help_for_dev"))
        self.keyboards['general_menu_keyboard'].add(types.InlineKeyboardButton(text="Ми на мапі🗺", url="https://goo.gl/maps/4wa4ePvYPPr9JQzf7"))
        self.keyboards['general_menu_keyboard'].add(types.InlineKeyboardButton(text="Підтримка💪", url="https://t.me/bonnaza"))


        return self.keyboards["general_menu_keyboard"]

    def payment_menu(self):
        self.keyboards['payment_keyboard'] = types.InlineKeyboardMarkup()
        self.keyboards['payment_keyboard'].add(types.InlineKeyboardButton(text="Внесок 5 UAH", pay=True))
        self.keyboards['payment_keyboard'].add(types.InlineKeyboardButton(text="В головне меню⬅", callback_data="back_from_pay_menu"))

        return self.keyboards['payment_keyboard']

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








