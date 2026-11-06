# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Учёт шаурмичной",
    page_icon="🌯",
    layout="wide"
)

st.title("🌯 Финансовый учёт шаурмичной")
st.caption("Расчёт выручки, себестоимости, прибыли и точки безубыточности")

# -----------------------------
# 1. НАСТРОЙКИ И РАСХОДЫ
# -----------------------------

st.header("1. Постоянные расходы")

c1, c2, c3 = st.columns(3)

with c1:
    rent = st.number_input("Аренда в месяц", 0.0, value=15000.0)
    electricity = st.number_input("Электричество", 0.0, value=3000.0)

with c2:
    water = st.number_input("Вода", 0.0, value=500.0)
    gas = st.number_input("Газ", 0.0, value=1500.0)

with c3:
    other_utilities = st.number_input("Другие коммунальные", 0.0)
    other_expenses = st.number_input("Прочие расходы", 0.0)

st.header("2. Сотрудники")

c1, c2 = st.columns(2)

with c1:
    employees = st.number_input(
        "Количество работников", 0, 100, 2
    )

with c2:
    salary = st.number_input(
        "Зарплата одного работника", 0.0, value=15000.0
    )

salary_total = employees * salary

# -----------------------------
# 3. ПРОДУКТЫ И ЗАКУПКИ
# -----------------------------

st.header("3. Закупка ингредиентов")

st.info(
    "Указывай закупочную цену за единицу измерения. "
    "Например: курица — 180 грн за кг, лаваш — 8 грн за штуку."
)

default_ingredients = pd.DataFrame([
    ["Курица", "кг", 180.0, 50.0],
    ["Лаваш", "шт", 8.0, 100.0],
    ["Капуста", "кг", 35.0, 10.0],
    ["Огурец", "кг", 70.0, 10.0],
    ["Помидор", "кг", 80.0, 10.0],
    ["Соус", "кг", 100.0, 5.0],
])

ingredients = st.data_editor(
    default_ingredients,
    num_rows="dynamic",
    use_container_width=True,
    key="ingredients",
    column_config={
        "Закупочная цена": st.column_config.NumberColumn(
            "Цена за единицу (грн)", min_value=0
        ),
        "Закуплено": st.column_config.NumberColumn(
            "Закуплено за месяц", min_value=0
        )
    }
    if False else None
)

ingredients.columns = [
    "Название", "Единица", "Цена закупки", "Закуплено"
]

ingredients["Стоимость закупки"] = (
    ingredients["Цена закупки"] * ingredients["Закуплено"]
)

st.subheader("Стоимость закупок")

st.metric(
    "Всего закуплено на",
    f"{ingredients['Стоимость закупки'].sum():,.2f} грн"
)

# -----------------------------
# 4. РЕЦЕПТЫ
# -----------------------------

st.header("4. Состав каждой шаурмы")

st.caption(
    "Количество ингредиента указывается в единицах из таблицы закупок. "
    "Например, 0.15 кг курицы или 1 шт. лаваша."
)

default_recipes = pd.DataFrame([
    ["Классическая", "Курица", 0.15],
    ["Классическая", "Лаваш", 1.0],
    ["Классическая", "Капуста", 0.08],
    ["Классическая", "Огурец", 0.04],
    ["Классическая", "Помидор", 0.04],
    ["Классическая", "Соус", 0.03],
])

recipes = st.data_editor(
    default_recipes,
    num_rows="dynamic",
    use_container_width=True,
    key="recipes",
)

recipes.columns = ["Шаурма", "Ингредиент", "Количество"]

# -----------------------------
# 5. ПРОДАЖИ
# -----------------------------

st.header("5. Меню и продажи")

default_menu = pd.DataFrame([
    ["Классическая", 150.0, 500],
    ["Сырная", 180.0, 200],
    ["Большая", 200.0, 100],
])

menu = st.data_editor(
    default_menu,
    num_rows="dynamic",
    use_container_width=True,
    key="menu",
)

menu.columns = ["Название", "Цена продажи", "Количество продаж"]

# -----------------------------
# 6. РАСХОДНИКИ
# -----------------------------

st.header("6. Расходники")

packaging = st.number_input(
    "Упаковка на одну шаурму (грн)", 0.0, value=3.0
)

napkins = st.number_input(
    "Салфетки и пакеты на одну шаурму (грн)", 0.0, value=1.0
)

waste_percent = st.number_input(
    "Потери продуктов (%)", 0.0, 100.0, 5.0
)

# -----------------------------
# 7. РАСЧЁТ СЕБЕСТОИМОСТИ
# -----------------------------

st.header("7. Финансовый результат")

valid_ingredients = ingredients.dropna(
    subset=["Название", "Цена закупки"]
)

cost_map = dict(zip(
    valid_ingredients["Название"],
    valid_ingredients["Цена закупки"]
))

recipes = recipes.dropna(
    subset=["Шаурма", "Ингредиент", "Количество"]
)

menu = menu.dropna(
    subset=["Название", "Цена продажи", "Количество продаж"]
)

recipes["Цена ингредиента"] = recipes["Ингредиент"].map(cost_map)

recipes["Стоимость"] = (
    recipes["Количество"] * recipes["Цена ингредиента"]
)

recipes["Стоимость"] = recipes["Стоимость"].fillna(0)

recipe_costs = recipes.groupby("Шаурма")["Стоимость"].sum()

menu["Продукты"] = menu["Название"].map(recipe_costs).fillna(0)

menu["Расходники"] = packaging + napkins

menu["Себестоимость"] = (
    menu["Продукты"] * (1 + waste_percent / 100)
    + menu["Расходники"]
)

menu["Выручка"] = (
    menu["Цена продажи"] * menu["Количество продаж"]
)

menu["Переменные расходы"] = (
    menu["Себестоимость"] * menu["Количество продаж"]
)

menu["Валовая прибыль"] = (
    menu["Выручка"] - menu["Переменные расходы"]
)

# -----------------------------
# 8. ОБЩИЕ ИТОГИ
# -----------------------------

revenue = menu["Выручка"].sum()
variable_costs = menu["Переменные расходы"].sum()

fixed_costs = (
    rent
    + electricity
    + water
    + gas
    + other_utilities
    + other_expenses
    + salary_total
)

profit = revenue - variable_costs - fixed_costs

total_units = menu["Количество продаж"].sum()

margin = revenue - variable_costs

# -----------------------------
# 9. ТОЧКА БЕЗУБЫТОЧНОСТИ
# -----------------------------

average_margin = (
    margin / total_units if total_units > 0 else 0
)

break_even = (
    fixed_costs / average_margin
    if average_margin > 0 else 0
)

# -----------------------------
# 10. ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ
# -----------------------------

st.subheader("Финансовые показатели")

c1, c2, c3 = st.columns(3)

c1.metric("Выручка", f"{revenue:,.2f} грн")
c2.metric("Себестоимость продаж", f"{variable_costs:,.2f} грн")
c3.metric("Постоянные расходы", f"{fixed_costs:,.2f} грн")

st.divider()

if profit > 0:
    st.success(f"ЧИСТАЯ ПРИБЫЛЬ: {profit:,.2f} грн")
elif profit < 0:
    st.error(f"УБЫТОК: {profit:,.2f} грн")
else:
    st.warning("РАБОТА В НОЛЬ")

c1, c2, c3 = st.columns(3)

c1.metric("Продано шаурмы", f"{total_units:,.0f} шт.")
c2.metric("Прибыль с продаж до постоянных расходов",
          f"{margin:,.2f} грн")
c3.metric("Рентабельность",
          f"{profit / revenue * 100:.2f}%" if revenue else "0%")

st.divider()

st.subheader("Точка безубыточности")

st.metric(
    "Нужно продать единиц меню",
    f"{break_even:,.0f} шт."
)

if total_units > 0:
    st.write(
        f"Фактически продано: {total_units:.0f} шт. "
        f"| Для безубыточности: {break_even:.0f} шт."
    )

st.subheader("Экономика каждой позиции")

st.dataframe(
    menu[[
        "Название",
        "Цена продажи",
        "Продукты",
        "Расходники",
        "Себестоимость",
        "Количество продаж",
        "Выручка",
        "Переменные расходы",
        "Валовая прибыль"
    ]],
    use_container_width=True
)

st.subheader("Расходы предприятия")

expenses_report = pd.DataFrame({
    "Статья": [
        "Аренда",
        "Электричество",
        "Вода",
        "Газ",
        "Другие коммунальные",
        "Прочие расходы",
        "Зарплаты",
        "Продукты и расходники"
    ],
    "Сумма": [
        rent,
        electricity,
        water,
        gas,
        other_utilities,
        other_expenses,
        salary_total,
        variable_costs
    ]
})

st.dataframe(expenses_report, use_container_width=True)
