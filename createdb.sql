create table budgets(
    codename varchar(255) primary key,
    month_limit integer
);

create table categories(
    codename varchar(255) primary key,
    name varchar(255)
);

create table sub_categories(
    codename varchar(255) primary key,
    name varchar(255),
    category varchar(255),
    aliases text,
    FOREIGN KEY(category) REFERENCES categories(codename)
);

create table transactions(
    id integer primary key,
    amount integer,
    created datetime,
    sub_category varchar(255),
    raw_text text,
    FOREIGN KEY(sub_category) REFERENCES sub_categories(codename)
);

insert into budgets(codename, month_limit)
values
    ("base", 20000),
    ("flat", 10000),
    ("debt", 75000),
    ("car", 10000),
    ("other", 20000),
    ("income", 150000);

insert into categories(codename, name)
values
    ("base_expense", "расход на базовые потребности"),
    ("other_expense", "другие расходы"),
    ("flat_expense", "расход на квартиру"),
    ("debt_expense", "расход на долг"),
    ("car_expense", "расход на машину"),
    ("income", "доход");

insert into sub_categories(codename, name, category, aliases)
values
    ("dividends", "дивиденды", "income", "дивиденды"),
    ("salary", "зарплата", "income", "зарплата, зп, аванс"),
    ("salary_bonus", "премия", "income", "премия, премии"),
    ("surprise", "сюрприз", "income", "подарок мне, сюрприз"),
    ("lend", "заём", "income", "заём, заем"),
    ("other_incomes", "прочие доходы", "income", "прочие доходы");

insert into sub_categories(codename, name, category, aliases)
values
    ("books", "книги", "flat_expense", "литература, литра, лит-ра"),
    ("jsk", "ЖСК", "flat_expense", "жск, коммуналка, тсж, жкх, квартира, за квартиру, квартплата"),
    ("electricity", "электричество", "flat_expense", "электричество, электроэнергия, свет, за свет, за электричество, за электроэнергию"),
    ("gas", "газ", "flat_expense", "газ, бытовой газ, за газ, газпром"),
    ("flat_internet", "интернет", "flat_expense", "интернет, инет"),
    ("flat_expenses", "расходы на квартиру", "flat_expense", "квартира, для квартиры, ремонт квартиры");

insert into sub_categories(codename, name, category, aliases)
values
    ("credits", "кредиты", "debts_expense", "кредит, ипотека"),
    ("debts", "долги", "debts_expense", "долг");

insert into sub_categories(codename, name, category, aliases)
values
    ("products", "продукты", "base_expense", "еда"),
    ("education", "образование", "base_expense", "образование, учеба, повышение квалификации, обучение"),
    ("health", "здоровье", "base_expense", "здоровье, лечение, лекарство, стоматолог, терапевт"),
    ("cafe", "кафе", "base_expense", "ресторан, столовая, питание"),
    ("sport", "спорт", "base_expense", "фитнес, тренажерка, тренажёрка, спортинвентарь");

insert into sub_categories(codename, name, category, aliases)
values
    ("transport", "общ. транспорт", "other_expense", "метро, автобус, metro, трамвай, троллейбус, транспорт"),
    ("taxi", "такси", "other_expense", "яндекс такси, yandex taxi, такси, yandex go"),
    ("connection", "связь", "other_expense", "билайн, связь, телефон"),
    ("subscriptions", "подписки", "other_expense", "подписка"),
    ("gift", "подарок", "other_expense", "подарок, подарки, презент кому"),
    ("household_goods", "хозтовары", "other_expense", "хозтовары, хозяйственные товары, хоз, уход, косметика"),
    ("clothes", "одежда", "other_expense", "одежда, шмотки"),
    ("technique", "техника", "other_expense", "электронника"),
    ("other_expenses", "прочие расходы", "other_expense", "прочие расходы, другие расходы");

insert into sub_categories(codename, name, category, aliases)
values
    ("car_refueling", "заправка", "car_expense", "заправка машины, заправка"),
    ("car_wash", "мойка", "car_expense", "мойка, мойка машины"),
    ("car_parking", "парковка", "car_expense", "парковка, стоянка"),
    ("car_fine", "автоштраф", "car_expense", "автомобильный штраф, автоштраф"),
    ("car_repairs", "ремонт", "car_expense", "ремонт машины, техническое обслуживание, техобслуживание, ТО, шиномонтаж");
