"""Работа с доходами — их добавление, удаление, статистика."""
import datetime
import re
import pytz
from typing import List, NamedTuple, Optional


import exceptions
from database import DataBase
from categories import SubCategories


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом доходе."""
    amount: int
    sub_category_text: str


class Income(NamedTuple):
    """Структура добавленного в БД нового дохода."""
    id: Optional[int]
    amount: int
    sub_category_name: str


def add_income(raw_message: str) -> Income:
    """Добавляет новый доход.
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
    })
    return Income(id=None,
                  amount=parsed_message.amount,
                  sub_category_name=sub_category.name)


def get_today_income_statistics() -> str:
    """Возвращает строкой статистику доходов за сегодня."""

    db = DataBase()
    cursor = db.get_cursor()
    # Все доходы за день
    cursor.execute("select sum(amount) "
                   "from transactions where date(created)=date('now', 'localtime') "
                   "and sub_category in (select codename "
                   "from sub_categories where category='income') ")
    result = cursor.fetchone()
    if not result[0]:
        return "Сегодня ещё нет доходов"
    today_incomes = result[0]
    return (f"Доходы сегодня:\n"
            f"{today_incomes} руб. из {_get_budget_limit()} руб.\n\n"
            f"За текущий месяц: /month_incomes")


def get_month_income_statistics() -> str:
    """Возвращает строкой статистику доходов за текущий месяц."""

    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    db = DataBase()
    cursor = db.get_cursor()
    cursor.execute("select sum(amount) "
                   f"from transactions where date(created) >= '{first_day_of_month}' "
                   "and sub_category in (select codename "
                   "from sub_categories where category='income') ")
    result = cursor.fetchone()
    if not result[0]:
        return "В этом месяце ещё нет доходов"
    month_incomes = result[0]
    return (f"Доходы в текущем месяце:\n"
            f"{month_incomes} руб. из {_get_budget_limit()} руб.\n\n"
            f"За сегодня: /today_incomes")


def last_income() -> List[Income]:
    """Возвращает последние несколько доходов."""

    db = DataBase()
    cursor = db.get_cursor()
    cursor.execute(
        "select t.id, t.amount, s.name "
        "from transactions t left join sub_categories s "
        "on s.codename=t.sub_category "
        "where s.category='income' "
        "order by created desc limit 5")
    rows = cursor.fetchall()
    last_incomes = [Income(id=row[0], amount=row[1], sub_category_name=row[2]) for row in rows]
    return last_incomes


def delete_income(row_id: int) -> None:
    """Удаляет доход по его идентификатору."""

    db = DataBase()
    db.delete("transactions", row_id)


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом доходе."""

    regexp_result = re.match(r"(.*) ([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2) or not regexp_result.group(3):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\nдоход 20000 зп")
    amount = int(regexp_result.group(2).replace(" ", ""))
    sub_category_text = regexp_result.group(3).strip().lower()
    return Message(amount=amount, sub_category_text=sub_category_text)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _get_budget_limit() -> int:
    """Возвращает месячный лимит трат для основных базовых трат"""
    
    # TODO: Заменить передачу данных на словарь с лимитами
    db = DataBase()
    return db.fetchall("budgets", ["month_limit"])[4]["month_limit"]
