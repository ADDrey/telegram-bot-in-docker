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
    ("debt", 60000),
    ("car", 5000),
    ("income", 300000);

insert into categories(codename, name)
values
    ("base_expense", "расход на базовые потребности"),
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
    ("gas", "газ", "flat_expense", "газ, бытовой газ, за газ, газпром");

insert into sub_categories(codename, name, category, aliases)
values
    ("credits", "кредиты", "debts_expense", "кредит, ипотека"),
    ("debts", "долги", "debts_expense", "долг");

insert into sub_categories(codename, name, category, aliases)
values
    ("products", "продукты", "base_expense", "еда"),
    ("education", "образование", "base_expense", "образование, учеба, повышение квалификации, обучение"),
    ("health", "здоровье", "base_expense", "здоровье, лечение, лекарство, стоматолог, терапевт"),
    ("cafe", "кафе", "base_expense", "ресторан, мак, макдональдс, kfc, il patio, столовая, ланч, бизнес-ланч, бизнес ланч"),
    ("transport", "общ. транспорт", "base_expense", "метро, автобус, metro, трамвай, троллейбус"),
    ("taxi", "такси", "base_expense", "яндекс такси, yandex taxi, такси, yandex go"),
    ("connection", "связь", "base_expense", "билайн, связь, интернет, телефон"),
    ("subscriptions", "подписки", "base_expense", "подписка"),
    ("gift", "подарок", "base_expense", "подарок, подарки, презент кому"),
    ("household_goods", "хозтовары", "base_expense", "хозтовары, хозяйственные товары"),
    ("other_expenses", "прочие расходы", "base_expense", "прочие расходы");

insert into sub_categories(codename, name, category, aliases)
values
    ("car_refueling", "заправка", "car_expense", "заправка машины, заправка"),
    ("car_wash", "мойка", "car_expense", "мойка, мойка машины"),
    ("car_repairs", "ремонт", "car_expense", "ремонт машины, ремонт"),
    ("flat_expenses", "расходы на квартиру", "car_expense", "квартира, для квартиры, ремонт квартиры");
