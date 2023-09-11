import asyncio
import logging
import sys


from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import Message
import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')



dp = Dispatcher()


@dp.message(CommandStart())
async def command_start(message: Message):
    conn = None

    """ Connect to the PostgreSQL database server """
    try:
        print('Connecting to the PostgreSQL database...')
        await message.answer(f'Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER,password=DB_PASSWORD)


        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECTed version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        await message.answer(f'PostgreSQL database version: {db_version}')
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        await message.answer(f'{error}')
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            await message.answer(f'Database connection closed.')




@dp.message(Command('id'))
async def user_id(message: Message):
    await message.answer(f'You telegram id :  {message.from_user.id}')


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())