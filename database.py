""" Работа с Базой Данный содержащей информацию о транзакциях"""

import os
import sqlite3

from typing import Dict, List


class DataBase:
    """Класс реализующий подключение к Базе Данных и управление данными в ней."""

    def __init__(self):
        self.con = sqlite3.connect(os.path.join("db", "finance.db"))
        self.cursor = self.con.cursor()
        self.check_db_exists()

    def insert(self, table: str, column_values: Dict):
        """Метод отвечающий за внесение данных в указанную таблицу Базы Данных"""

        columns = ', '.join(column_values.keys())
        values = [tuple(column_values.values())]
        placeholders = ", ".join("?" * len(column_values.keys()))
        self.cursor.executemany(
            f"INSERT INTO {table} "
            f"({columns}) "
            f"VALUES ({placeholders})",
            values)
        self.con.commit()

    def fetchall(self, table: str, columns: List[str]) -> List[Dict]:
        """Метод отвечающий за получение полной выборки данных из указанной таблицы Базы Данных"""

        columns_joined = ", ".join(columns)
        self.cursor.execute(f"SELECT {columns_joined} FROM {table}")
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result

    def delete(self, table: str, row_id: int) -> None:
        """Метод отвечающий за удаление данных из указанной таблицы Базы Данных"""

        row_id = int(row_id)
        self.cursor.execute(f"DELETE FROM {table} WHERE id={row_id}")
        self.con.commit()

    def get_cursor(self):
        """
        Метод отвечающий за передачу указателя на открытую Базу Данных.
        Предназначен для обращения к параметру "cursor" данного класса.
        """

        return self.cursor

    def _init_db(self):
        """Инициализирует БД"""

        with open("createdb.sql", "r") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.con.commit()

    def check_db_exists(self):
        """Проверяет, инициализирована ли БД, если нет — инициализирует"""

        self.cursor.execute("SELECT name FROM sqlite_master "
                            "WHERE type='table' AND name='transactions'")
        table_exists = self.cursor.fetchall()
        if table_exists:
            return
        else:
            self._init_db()
