"""Работа с категориями расходов и доходов."""
from typing import Dict, List, NamedTuple

from database import DataBase


class Category(NamedTuple):
    """Структура категории"""
    codename: str
    name: str


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Возвращает справочник категорий из БД."""
        db = DataBase()
        categories = db.fetchall(
            "category",
            """codename
            name""".split()
        )
        categories = self._fill_categories(categories)
        return categories

    @staticmethod
    def _fill_categories(categories: List[Dict]) -> List[Category]:
        """Заполняет по каждой подкатегории aliases, то есть возможные
        названия этой категории, которые можем писать в тексте сообщения.
        Например, подкатегория «кафе» может быть написана как cafe,
        ресторан и тд."""
        categories_result = []
        for index, category in enumerate(categories):
            categories_result.append(Category(
                codename=category['codename'],
                name=category['name']
            ))
        return categories_result

    def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по названию."""
        fined = None
        other_category = None
        for category in self._categories:
            if category.name == "расходы":  # TODO: Костыль
                other_category = category
            for name in category:
                if category_name in name:
                    fined = category
        if not fined:
            fined = other_category
        return fined


class SubCategory(NamedTuple):
    """Структура подкатегории."""
    codename: str
    name: str
    category: str
    aliases: List[str]


class SubCategories:
    def __init__(self):
        self._sub_categories = self._load_sub_categories(self)

    @staticmethod
    def _load_sub_categories(self) -> List[SubCategory]:
        """Возвращает справочник подкатегорий расходов из БД."""
        db = DataBase()
        sub_categories = db.fetchall(
            "sub_categories",
            """codename
            name
            category
            aliases""".split()
        )
        sub_categories = self._fill_aliases(sub_categories)
        return sub_categories

    @staticmethod
    def _fill_aliases(sub_categories: List[Dict]) -> List[SubCategory]:
        """Заполняет по каждой подкатегории aliases, то есть возможные
        названия этой категории, которые можем писать в тексте сообщения.
        Например, подкатегория «кафе» может быть написана как cafe,
        ресторан и тд."""
        sub_categories_result = []
        for index, sub_category in enumerate(sub_categories):
            aliases = sub_category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(sub_category["codename"])
            aliases.append(sub_category["name"])
            sub_categories_result.append(SubCategory(
                codename=sub_category['codename'],
                name=sub_category['name'],
                category=sub_category['category'],
                aliases=aliases
            ))
        return sub_categories_result

    def get_all_sub_categories(self) -> List[SubCategory]:
        """Возвращает справочник подкатегорий."""
        return self._sub_categories

    def get_sub_category(self, sub_category_name: str) -> SubCategory:
        """Возвращает подкатегорию по одному из её алиасов (ассоциаций)."""
        fined = None
        other_category = None
        for sub_category in self._sub_categories:
            if sub_category.codename == "other":
                other_category = sub_category
            for alias in sub_category.aliases:
                if sub_category_name == alias:
                    fined = sub_category
        if not fined:
            fined = other_category
        return fined
