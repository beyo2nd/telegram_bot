import asyncio
import logging
import time
import config

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.utils.markdown import hlink

from userid_database import SQLDatabase

from datetime import datetime, timedelta


#Инициализируем бота
bot_token = "6412664411:AAG56mTNxcgGOlMOvt5AhNQpO1B0Snlu0lU"
bot = Bot(token = bot_token)
dp = Dispatcher(bot)
status = True

#Инициализация базы данных
db = SQLDatabase('podarki_bot/userid_db.db')

#Клавиатура
keyboard = InlineKeyboardMarkup()
button = InlineKeyboardButton('Instagram', url='https://www.instagram.com/podarok_format?igshid=NGVhN2U2NjQ0Yg==')
keyboard.add(button)

#Айди админа
admin_id = 366254199

#сообщения
first_text = """*Отлично! Скидка успешно закреплена за тобой. Поздравляем! 🎊🔥 *\n\nТы уже на шаг ближе к тому, чтобы стать владельцем нового Changan UNI-V! *Уже очень скоро ты получишь возможность оплатить билет, по специальным условиям! 🚘*\n\nБлагодарим за доверие и остаемся на связи! 🤝"""
second_text = """*🎫 НО ЭТО ЕЩЕ НЕ ВСЕ…*\n\nПодписывайся на наш Instagram, где тебя уже ждёт много контента с бойцами POPMMA и блогерами! \n\nТам же можно будет узнать подробнее о других призах и получить приглашение на ивенты, в которых *сможешь увидеться с бойцами - лично!* 🔥🤩\n\nКстати, тут тоже будут появляться экслюзивные кадры, поэтому советуем закрепить этот бот! ⭐️"""
sendall_text = """Сообщение для рассылки"""

#обработка команды старт
@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    if (db.user_exists(message.from_user.id)):
        print("пользователь уже есть в базе данных")
        pass
    
    else:
        #print("пользователь добавляется")
        db.add_user(message.from_user.id, status)
        print("пользователь добавлен")
        with open('podarki_bot/images/start_image.jpg', 'rb') as photo:
            await bot.send_photo(chat_id = message.from_user.id,photo = photo, caption=first_text, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(120)
        await bot.send_message(message.from_user.id, text=second_text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
            
#Рассылка
@dp.message_handler(commands = ['sendall'])
async def send_all(message: types.message):
    if message.chat.id == admin_id:
        for i in db.get_users(1):
            print(f"Рассылка отправлена {i[1]}")
            await bot.send_message(i[1],sendall_text)
            await asyncio.sleep(0.3)
        await message.answer('Готово')
    else:
        await message.answer('Сообщения отправлены не всем пользователям\nлибо вы не являетесь администратором')

#main function
async def main():
    logging.basicConfig(level = logging.INFO)
    await dp.start_polling(bot)
    print(1)

if __name__ == "__main__":
    asyncio.run(main())