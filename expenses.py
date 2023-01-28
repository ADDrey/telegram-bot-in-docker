"""Работа с расходами — их добавление, удаление, статистика."""
import datetime
import re
import pytz
from typing import List, NamedTuple, Optional


import exceptions
from database import DataBase
from categories import SubCategories


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе."""
    amount: int
    sub_category_text: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода."""
    id: Optional[int]
    amount: int
    sub_category_name: str


def add_expense(raw_message: str) -> Expense:
    """Добавляет новый расход (траты).
    Принимает на вход текст сообщения, пришедшего в бот."""

    parsed_message = _parse_message(raw_message)
    sub_category = SubCategories().get_sub_category(
        parsed_message.sub_category_text)
    db = DataBase()
    db.insert("transactions", {
            "amount": parsed_message.amount,
            "created": _get_now_formatted(),
            "sub_category": sub_category.codename,
            "raw_text": raw_message
        }
    )
    return Expense(id=None,
                   amount=parsed_message.amount,
                   sub_category_name=sub_category.name)


def get_today_expense_statistics() -> str:
    """Возвращает строкой статистику расходов за сегодня."""

    db = DataBase()
    cursor = db.get_cursor()
    # Все расходы за день
    cursor.execute("select sum(amount) "
                   "from transactions where date(created)=date('now', 'localtime') "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE '%_expense') ")
    result = cursor.fetchone()
    if not result[0]:
        return "Сегодня ещё нет расходов"
    all_today_expenses = result[0]

    # Базовые расходы за день
    cursor.execute("select sum(amount) "
                   "from transactions where date(created)=date('now', 'localtime') "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'base_%') ")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0

    # Автомобильные расходы за день
    cursor.execute("select sum(amount) "
                   "from transactions where date(created)=date('now', 'localtime') "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'car_%') ")
    result = cursor.fetchone()
    car_today_expenses = result[0] if result[0] else 0

    # Долговые расходы за день
    cursor.execute("select sum(amount) "
                   "from transactions where date(created)=date('now', 'localtime') "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'debt_%') ")
    result = cursor.fetchone()
    debts_today_expenses = result[0] if result[0] else 0

    # Квартирные расходы за день
    cursor.execute("select sum(amount) "
                   "from transactions where date(created)=date('now', 'localtime') "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'flat_%') ")
    result = cursor.fetchone()
    flat_today_expenses = result[0] if result[0] else 0

    # Иные расходы за день
    cursor.execute("select sum(amount) "
                   "from transactions where date(created)=date('now', 'localtime') "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'other_%') ")
    result = cursor.fetchone()
    other_today_expenses = result[0] if result[0] else 0

    return (f"Расходы сегодня:\n"
            f"* всего — {all_today_expenses} руб.\n"
            f"* базовые — {base_today_expenses} руб.\n"
            f"* автомобильные — {car_today_expenses} руб.\n"
            f"* долговые — {debts_today_expenses} руб.\n"
            f"* квартирные — {flat_today_expenses} руб.\n"
            f"* иные — {other_today_expenses} руб.\n\n"
            f"За текущий месяц: /month_expenses")


def get_month_expense_statistics() -> str:
    """Возвращает строкой статистику расходов за текущий месяц."""

    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    db = DataBase()
    cursor = db.get_cursor()
    cursor.execute("select sum(amount) "
                   f"from transactions where date(created) >= '{first_day_of_month}' "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE '%_expense') ")
    result = cursor.fetchone()
    if not result[0]:
        return "В этом месяце ещё нет расходов"
    all_month_expenses = result[0]

    # Базовые расходы за текущий месяц
    cursor.execute("select sum(amount) "
                   f"from transactions where date(created) >= '{first_day_of_month}' "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'base_%') ")
    result = cursor.fetchone()
    base_month_expenses = result[0] if result[0] else 0

    # Автомобильные расходы за текущий месяц
    cursor.execute("select sum(amount) "
                   f"from transactions where date(created) >= '{first_day_of_month}' "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'car_%') ")
    result = cursor.fetchone()
    car_month_expenses = result[0] if result[0] else 0

    # Долговые расходы за текущий месяц
    cursor.execute("select sum(amount) "
                   f"from transactions where date(created) >= '{first_day_of_month}' "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'debt_%') ")
    result = cursor.fetchone()
    debts_month_expenses = result[0] if result[0] else 0

    # Квартирные расходы за текущий месяц
    cursor.execute("select sum(amount) "
                   f"from transactions where date(created) >= '{first_day_of_month}' "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'flat_%') ")
    result = cursor.fetchone()
    flat_month_expenses = result[0] if result[0] else 0

    # Квартирные расходы за текущий месяц
    cursor.execute("select sum(amount) "
                   f"from transactions where date(created) >= '{first_day_of_month}' "
                   "and sub_category in (select codename "
                   "from sub_categories where category LIKE 'other_%') ")
    result = cursor.fetchone()
    other_month_expenses = result[0] if result[0] else 0

    return ("Расходы в текущем месяце:\n"
            f"* всего — {all_month_expenses} руб.\n"
            f"* базовые — {base_month_expenses} руб. из {_get_budgets_limit('base')} руб.\n"
            f"* автомобильные — {car_month_expenses} руб. из {_get_budgets_limit('car')} руб.\n"
            f"* долговые — {debts_month_expenses} руб. из {_get_budgets_limit('debts')} руб.\n"
            f"* квартирные — {flat_month_expenses} руб. из {_get_budgets_limit('flat')} руб.\n"
            f"* иные — {other_month_expenses} руб. из {_get_budgets_limit('other')} руб.\n\n"
            "За сегодня: /today_expenses")


def last_expense() -> List[Expense]:
    """Возвращает последние несколько расходов."""

    db = DataBase()
    cursor = db.get_cursor()
    cursor.execute(
        "select t.id, t.amount, s.name "
        "from transactions t left join sub_categories s "
        "on s.codename=t.sub_category "
        "where s.category LIKE '%_expense' "
        "order by created desc limit 5")
    rows = cursor.fetchall()
    last_expenses = [Expense(id=row[0], amount=row[1], sub_category_name=row[2]) for row in rows]
    return last_expenses


def delete_expense(row_id: int) -> None:
    """Удаляет расход по его идентификатору."""

    db = DataBase()
    db.delete("transactions", row_id)


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""

    regexp_result = re.match(r"(.*) ([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2) or not regexp_result.group(3):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате:\n"
            "'расход 1500 метро' или 'Р 1500 метро''")
    amount = int(regexp_result.group(2).replace(" ", ""))
    sub_category_text = regexp_result.group(3).strip().lower()
    return Message(amount=amount, sub_category_text=sub_category_text)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой."""

    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""

    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _get_budgets_limit(expense_cat: str) -> int:
    """Возвращает месячный лимит трат для основных базовых трат."""
    if expense_cat == 'base':
        db = DataBase()
        limit = db.fetchall("budgets", ["month_limit"])[0]["month_limit"]
    elif expense_cat == 'flat':
        db = DataBase()
        limit = db.fetchall("budgets", ["month_limit"])[1]["month_limit"]
    elif expense_cat == 'flat':
        db = DataBase()
        limit = db.fetchall("budgets", ["month_limit"])[2]["month_limit"]
    elif expense_cat == 'debts':
        db = DataBase()
        limit = db.fetchall("budgets", ["month_limit"])[3]["month_limit"]
    elif expense_cat == 'other':
        db = DataBase()
        limit = db.fetchall("budgets", ["month_limit"])[4]["month_limit"]
    return limit
