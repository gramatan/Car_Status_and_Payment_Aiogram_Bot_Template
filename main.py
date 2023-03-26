import asyncio
import os
import sqlite3
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_polling

# <<<Enter Your Token>>>
TOKEN = "BOT_TOKEN"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Connect to SQLite database
conn = sqlite3.connect('cars_database.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS car_numbers (car_number TEXT, status TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS admin_moderators (user_id INTEGER)''')
# cursor.execute('''INSERT INTO admin_moderators VALUES('<<<ADD ADMIN ID>>>')''')
conn.commit()


async def main() -> None:
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await (await bot.get_session()).close()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Введите номер автомобиля:')


@dp.message_handler(lambda message: not message.text.startswith('/'))
async def car_number(message: types.Message):
    user_car_number = message.text.upper()
    cursor.execute('SELECT status FROM car_numbers WHERE car_number=?', (user_car_number,))
    result = cursor.fetchone()

    if result:
        status = result[0]

        keyboard = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton("Оплатить", callback_data=f'pay_{user_car_number}'),
            InlineKeyboardButton("Отказаться", callback_data='cancel')
        )

        await message.reply(f'Статус автомобиля {user_car_number}: {status}', reply_markup=keyboard)
    else:
        await message.reply('Номер автомобиля не найден в базе данных. Пожалуйста, проверьте правильность введенного номера.')


@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data.startswith('pay_'):
        car_number = data[4:]
        cursor.execute('UPDATE car_numbers SET status="Оплачено" WHERE car_number=?', (car_number,))
        conn.commit()
        await bot.answer_callback_query(callback_query.id,
                                        text=f'Статус автомобиля {car_number} успешно обновлен на "Оплачено".',
                                        show_alert=True)
    elif data == 'cancel':
        await bot.answer_callback_query(callback_query.id, text='Вы отказались от оплаты.', show_alert=True)


@dp.message_handler(commands=['add_car_number'])
async def add_car_number(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM admin_moderators WHERE user_id=?', (user_id,))
    is_moderator = cursor.fetchone()

    if is_moderator:
        args = message.get_args().split()
        if len(args) == 2:
            car_number, status = args
            car_number = car_number.upper()
            cursor.execute('INSERT INTO car_numbers (car_number, status) VALUES (?, ?)', (car_number, status))
            conn.commit()
            await message.reply(f'Автомобиль {car_number} добавлен в базу данных со статусом "{status}".')
        else:
            await message.reply(
                'Неправильное количество аргументов. Используйте /add_car_number <номер автомобиля> <статус>.'
            )
    else:
        await message.reply('У вас нет прав для выполнения этой команды.')


@dp.message_handler(commands=['change_status'])
async def change_status(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM admin_moderators WHERE user_id=?', (user_id,))
    is_moderator = cursor.fetchone()
    if is_moderator:
        args = message.get_args().split()
        if len(args) == 2:
            car_number, new_status = args
            car_number = car_number.upper()
            cursor.execute('UPDATE car_numbers SET status=? WHERE car_number=?', (new_status, car_number))
            conn.commit()
            await message.reply(f'Статус автомобиля {car_number} успешно обновлен на "{new_status}".')
        else:
            await message.reply(
                'Неправильное количество аргументов. Используйте /change_status <номер автомобиля> <новый статус>.')
    else:
        await message.reply('У вас нет прав для выполнения этой команды.')


if __name__ == '__main__':
    asyncio.run(main())
