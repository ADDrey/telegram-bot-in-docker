"""Сервер Telegram бота, запускаемый непосредственно"""

# import packages
import logging
import os

# import personal modules
import exceptions
import expenses
import incomes
import keyboards

# import classes
from aiogram import Bot, Dispatcher, executor, types
from categories import SubCategories
from middlewares import AccessMiddleware

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ACCESS_ID = os.getenv("TELEGRAM_ACCESS_ID")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


'''
Bot Menu:
help - Справка по боту
sub_categories - Список категорий
list_expenses - Последние изменения
today_expenses - Расходы за сегодня
month_expenses - Расходы за месяц
list_incomes - Последние доходы
today_incomes - Доходы за сегодня
month_incomes - Доходы за месяц
'''


# Message Handlers
@dp.message_handler(commands=['помощь', 'start', 'запуск'])
@dp.message_handler(lambda message: message.text.startswith('помощь'))
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Привет! Я - Бот для учёта финансов.\n\n"
        "Добавить расход: расход 250 продукты\n"
        "Добавить доход: доход 20000 зп\n"
        "Открыть Меню: /меню\n"
        "Посмотреть данную справку: /помощь")


@dp.message_handler(commands=['меню'])
@dp.message_handler(lambda message: message.text.startswith('Меню'))
async def first_menu(message: types.Message):
    """Выводит главное меню бота"""
    await message.answer("Выберете пункт меню", reply_markup=keyboards.select_keyboard("/main_menu"))


@dp.callback_query_handler(lambda call: call.data.endswith('_menu'))
async def second_menu(call: types.CallbackQuery):
    """Выводит главное меню бота"""
    # await call.message.answer("Выберете пункт меню", reply_markup=keyboards.select_keyboard(call.data))
    await call.message.edit_reply_markup(reply_markup=keyboards.select_keyboard(call.data))


@dp.callback_query_handler(lambda call: call.data == '/list_incomes')
async def q_list_incomes(call: types.CallbackQuery):
    """Отправляет последние несколько записей о доходах"""
    last_incomes = incomes.last_income()
    if not last_incomes:
        await call.message.answer("Доходы ещё не заведены")
        return

    last_incomes_rows = [
        f"{income.amount} руб. - {income.sub_category_name} — нажми "
        f"/del_income{income.id} для удаления"
        for income in last_incomes]
    answer_message = "Последние сохранённые доходы:\n\n* " + "\n\n* " \
        .join(last_incomes_rows)
    await call.message.answer(answer_message)


@dp.callback_query_handler(lambda call: call.data == '/list_expenses')
async def q_list_expense(call: types.CallbackQuery):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last_expense()
    if not last_expenses:
        await call.message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. - {expense.sub_category_name} — нажми "
        f"/del_expense{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые расходы:\n\n* " + "\n\n* " \
        .join(last_expenses_rows)
    await call.message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/del_expense'))
async def del_expense(message: types.Message):
    """Удаляет одну запись о расходе по её идентификатору"""
    row_id = int(message.text[12:])
    expenses.delete_expense(row_id)
    answer_message = "Удалил запись о расходе"
    await message.answer(answer_message)


@dp.message_handler(lambda message: message.text.startswith('/del_income'))
async def del_income(message: types.Message):
    """Удаляет одну запись о доходе по её идентификатору"""
    row_id = int(message.text[11:])
    incomes.delete_income(row_id)
    answer_message = "Удалил запись о доходе"
    await message.answer(answer_message)


@dp.message_handler(commands=['sub_categories'])
async def sub_categories_list(message: types.Message):
    """Отправляет список категорий операций с финансами"""
    sub_categories = SubCategories().get_all_sub_categories()
    answer_message = "Категории операций:\n\n* " + \
                     ("\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in sub_categories]))
    await message.answer(answer_message)


@dp.message_handler(commands=['today_expenses'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику расходов"""
    answer_message = expenses.get_today_expense_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_expenses'])
async def month_statistics(message: types.Message):
    """Отправляет статистику расходов текущего месяца"""
    answer_message = expenses.get_month_expense_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['today_incomes'])
async def today_statistics(message: types.Message):
    """Отправляет сегодняшнюю статистику доходов"""
    answer_message = incomes.get_today_income_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month_incomes'])
async def month_statistics(message: types.Message):
    """Отправляет статистику доходов текущего месяца"""
    answer_message = incomes.get_month_income_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['list_expenses'])
async def list_expenses(message: types.Message):
    """Отправляет последние несколько записей о расходах"""
    last_expenses = expenses.last_expense()
    if not last_expenses:
        await message.answer("Расходы ещё не заведены")
        return

    last_expenses_rows = [
        f"{expense.amount} руб. на {expense.sub_category_name} — нажми "
        f"/del_expense{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Последние сохранённые расходы:\n\n* " + "\n\n* " \
        .join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler(commands=['list_incomes'])
async def list_incomes(message: types.Message):
    """Отправляет последние несколько записей о доходах"""
    last_incomes = incomes.last_income()
    if not last_incomes:
        await message.answer("Доходы ещё не заведены")
        return

    last_incomes_rows = [
        f"{income.amount} руб. на {income.sub_category_name} — нажми "
        f"/del_income{income.id} для удаления"
        for income in last_incomes]
    answer_message = "Последние сохранённые доходы:\n\n* " + "\n\n* " \
        .join(last_incomes_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def get_text_messages(message: types.Message):
    """Обрабатывает текстовые обращения пользователя в главном меню"""
    if 'привет' in message.text.lower():
        await message.answer('Привет!')
    elif 'д' in message.text.lower() or 'доход' in message.text.lower() or '+' in message.text.lower():
        """Добавляет новый доход"""
        try:
            income = incomes.add_income(message.text)
        except exceptions.NotCorrectMessage as e:
            await message.answer(str(e))
            return
        answer_message = (
            f"Добавлены доходы {income.amount} руб. источник - {income.sub_category_name}.\n\n"
            f"{incomes.get_today_income_statistics()}")
        await message.answer(answer_message)
    elif 'р' in message.text.lower() or 'расход' in message.text.lower() or '-' in message.text.lower():
        """Добавляет новый расход"""
        try:
            expense = expenses.add_expense(message.text)
        except exceptions.NotCorrectMessage as e:
            await message.answer(str(e))
            return
        answer_message = (
            f"Добавлены расходы {expense.amount} руб на {expense.sub_category_name}.\n\n"
            f"{expenses.get_today_expense_statistics()}")
        await message.answer(answer_message)
    else:
        await message.answer('Не понимаю, что это значит.\n Нажми /help для просмотра справки. ')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
