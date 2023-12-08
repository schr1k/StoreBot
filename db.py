import asyncpg

from config import *


class DB:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB
        )

    # SELECT ===========================================================================================================
    async def user_exists(self, telegram_id: str) -> bool:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT telegram_id FROM db_users WHERE telegram_id = $1', telegram_id
                )
                return False if result is None else True

    async def get_categories(self) -> list[dict]:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(
                    'SELECT id, name FROM db_categories',
                )
                return [dict(i) for i in result]

    async def get_subcategories(self, category: int) -> list[dict]:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(
                    'SELECT id, name FROM db_subcategories WHERE category_id = $1', category
                )
                return [dict(i) for i in result]

    async def get_products(self, subcategory: int) -> list[dict]:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetch(
                    'SELECT id, name FROM db_subcategories WHERE subcategory_id = $1', subcategory
                )
                return [dict(i) for i in result]

    async def get_product_info(self, product_id: int) -> dict:
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.fetchrow(
                    'SELECT name, description FROM db_products WHERE id = $1', product_id
                )
                return dict(result)

    # UPDATE ===========================================================================================================
    async def update_name(self, telegram_id: str, name: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    'UPDATE db_users SET name = $1 WHERE telegram_id = $2', name, telegram_id
                )

    # INSERT ===========================================================================================================
    async def insert_in_users(self, telegram_id: str):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    'INSERT INTO db_users (telegram_id) VALUES($1)', telegram_id
                )
