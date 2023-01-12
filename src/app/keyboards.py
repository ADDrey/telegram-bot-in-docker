"""Встроенные клавиатуры Telegram бота, вызываются командой '/menu' или словом 'меню'"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def select_keyboard(menu_name: str) -> InlineKeyboardMarkup:
    """Выбирает меню по полученной строке, если совпадений нет, то возвращает главное меню."""

    menu_dict = {
        "/menu": main_keyboard(),
        "/main_menu": main_keyboard(),
        "/incomes_menu": incomes_keyboard(),
        "/expenses_menu": expenses_keyboard(),
    }
    keyboard = None
    for kb in menu_dict:
        if kb == menu_name or kb in menu_name:
            keyboard = menu_dict[kb]
            break
        else:
            keyboard = menu_dict["/menu"]
    return keyboard


def main_keyboard():
    inline_keyboard = InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("Доходы", callback_data="/incomes_menu"),
        InlineKeyboardButton("Расходы", callback_data="/expenses_menu"),
        InlineKeyboardButton("Отчёты", callback_data="/reports_budget_home_menu")
    )
    return inline_keyboard


def incomes_keyboard():
    inline_keyboard = InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("Добавить", callback_data="/add_income"),
        InlineKeyboardButton("Удалить", callback_data="/del_income"),
        InlineKeyboardButton("Последние", callback_data="/list_incomes"),
        InlineKeyboardButton("Сегодня", callback_data="/today_incomes"),
        InlineKeyboardButton("Месяц", callback_data="/month_incomes"),
        InlineKeyboardButton("Все", callback_data="/all_incomes"),
        InlineKeyboardButton("Назад в меню", callback_data="/main_keyboard")
    )
    return inline_keyboard


def expenses_keyboard():
    inline_keyboard = InlineKeyboardMarkup(row_width=3).add(
        InlineKeyboardButton("Добавить", callback_data="/add_expense"),
        InlineKeyboardButton("Удалить", callback_data="/del_expense"),
        InlineKeyboardButton("Последние", callback_data="/list_expenses"),
        InlineKeyboardButton("Сегодня", callback_data="/today_expenses"),
        InlineKeyboardButton("Месяц", callback_data="/month_expenses"),
        InlineKeyboardButton("Все", callback_data="/all_expenses"),
        InlineKeyboardButton("Назад в меню", callback_data="/main_keyboard")
    )
    return inline_keyboard
