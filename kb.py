from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

to_main = InlineKeyboardButton(text='🔙 На главную', callback_data='start')
to_main_kb = InlineKeyboardBuilder().row(to_main).as_markup()


catalog = InlineKeyboardButton(text='🔍 Каталог', callback_data='categories-1')
basket = InlineKeyboardButton(text='🛒 Корзина', callback_data='basket')
faq = InlineKeyboardButton(text='❔ FAQ', callback_data='faq')
main_kb = InlineKeyboardBuilder().row(catalog).row(basket).row(faq).as_markup()


def categories_kb(categories: list[dict], page: int):
    kb = InlineKeyboardBuilder()
    pages_amount = len(categories) // 5 + 1
    for categories in categories[5 * (page - 1):page * 5]:
        kb.row(InlineKeyboardButton(text=categories["name"], callback_data=f'subcategories-1-{categories["id"]}'))
    left = InlineKeyboardButton(text='⬅️', callback_data=f'categories-{page - 1 if page != 1 else pages_amount}')
    count = InlineKeyboardButton(text=f'{page}/{pages_amount}', callback_data=f'categories-{page}')
    right = InlineKeyboardButton(text='➡️', callback_data=f'categories-{page + 1 if page != pages_amount else 1}')
    kb.row(left, count, right)
    kb.row(to_main)
    return kb.as_markup()


def subcategories_kb(subcategories: list[dict], page: int, category: int):
    kb = InlineKeyboardBuilder()
    pages_amount = len(subcategories) // 5 + 1
    for subcategories in subcategories[5 * (page - 1):page * 5]:
        kb.row(InlineKeyboardButton(text=subcategories["name"], callback_data=f'products-1-{subcategories["id"]}'))
    left = InlineKeyboardButton(text='⬅️',
                                callback_data=f'subcategories-{page - 1 if page != 1 else pages_amount}-{category}')
    count = InlineKeyboardButton(text=f'{page}/{pages_amount}', callback_data=f'subcategories-{page}-{category}')
    right = InlineKeyboardButton(text='➡️',
                                 callback_data=f'subcategories-{page + 1 if page != pages_amount else 1}-{category}')
    kb.row(left, count, right)
    kb.row(to_main)
    return kb.as_markup()


def products_kb(products: list[dict], page: int, subcategory: int):
    kb = InlineKeyboardBuilder()
    pages_amount = len(products) // 5 + 1
    for product in products[5 * (page - 1):page * 5]:
        kb.row(InlineKeyboardButton(text=product["name"], callback_data=f'product-{product["id"]}'))
    left = InlineKeyboardButton(text='⬅️',
                                callback_data=f'products-{page - 1 if page != 1 else pages_amount}-{subcategory}')
    count = InlineKeyboardButton(text=f'{page}/{pages_amount}', callback_data=f'subcategories-{page}-{subcategory}')
    right = InlineKeyboardButton(text='➡️',
                                 callback_data=f'products-{page + 1 if page != pages_amount else 1}-{subcategory}')
    kb.row(left, count, right)
    kb.row(to_main)
    return kb.as_markup()


add_to_basket = InlineKeyboardButton(text='Добавить в корзину', callback_data='add_to_basket')
product_kb = InlineKeyboardBuilder().row(add_to_basket).as_markup()
