import asyncio
import logging
import sys
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import ChatMemberAdministrator, ChatMemberMember, ChatMemberOwner, FSInputFile, Message, \
    CallbackQuery
from aiogram.filters.command import Command
from redis.asyncio import Redis

from config import *
import kb
from states import *
from db import DB

# from payments import *

db = DB()

redis = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)
storage = RedisStorage(redis)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


@dp.message(Command('start'))
async def start(message: Message):
    try:
        status = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=message.from_user.id)
        if status.model_dump()['status'] != 'left':
            if not await db.user_exists(str(message.from_user.id)):
                await db.insert_in_users(str(message.from_user.id))
            await message.answer(f'Привет, {message.from_user.first_name}.', reply_markup=kb.main_kb)
        else:
            await message.answer('Сначала нужно подписаться на наш [канал](https://t.me/test_store_blablabla)\.',
                                 parse_mode='MarkdownV2')
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'categories')
async def catalog(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Выберите категорию.',
                                    reply_markup=kb.categories_kb(await db.get_categories(),
                                                                  int(call.data.split('-')[1])))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'subcategories')
async def subcategories(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Выберите подкатегорию.',
                                    reply_markup=kb.subcategories_kb(
                                        await db.get_subcategories(int(call.data.split('-')[2])),
                                        int(call.data.split('-')[1]),
                                        int(call.data.split('-')[2])))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'products')
async def products(call: CallbackQuery):
    try:
        await call.answer()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Выберите товар.',
                                    reply_markup=kb.products_kb(
                                        await db.get_subcategories(int(call.data.split('-')[2])),
                                        int(call.data.split('-')[1]),
                                        int(call.data.split('-')[2])))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'product')
async def product(call: CallbackQuery):
    try:
        await call.answer()
        product_info = await db.get_product_info(int(call.data.split('-')[1]))
        await call.message.answer_photo(photo=FSInputFile(f'./photos/{call.data.split("-")[1]}.png'),
                                        caption=f'Название: {product_info["name"]}\n'
                                                f'Описание: {product_info["description"]}\n',
                                        reply_markup=kb.product_kb)
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.callback_query(F.data.split('-')[0] == 'add_to_basket')
async def add_to_basket(call: CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        product_info = await db.get_product_info(int(call.data.split('-')[1]))
        await call.message.answer_photo(photo=FSInputFile(f'./photos/{call.data.split("-")[1]}.png'),
                                        caption=f'Название: {product_info["name"]}\n'
                                                f'Описание: {product_info["description"]}\n',
                                        reply_markup=kb.product_kb)
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.message(Command('id'))
async def ids(message: Message):
    try:
        await message.answer(str(message.from_user.id))
    except Exception as e:
        errors.error(e, exc_info=True)


@dp.message()
async def gids(message: Message):
    try:
        print(str(message.chat.id))
    except Exception as e:
        errors.error(e, exc_info=True)


async def main():
    await db.connect()
    await dp.start_polling(bot)


if __name__ == '__main__':
    print(f'Бот запущен ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')
    asyncio.run(main())
