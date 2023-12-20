import asyncio
import logging
import time

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
from aiogram.utils.markdown import hlink

from userid_database import SQLDatabase

from datetime import datetime, timedelta

#Константы ---------------------------------------------------------------------------------

#Инициализируем бота
bot_token = "6412664411:AAG56mTNxcgGOlMOvt5AhNQpO1B0Snlu0lU"
payments_token = "1832575495:TEST:4048a9aba0971711b1dae3f580b23897e6ece1f521c821378b3d785767f0dd65"
bot = Bot(token = bot_token)
dp = Dispatcher(bot)
status = True

#Инициализация базы данных
db = SQLDatabase('userid_db.db')

#Константы ---------------------------------------------------------------------------------

#Клавиатуры --------------------------------------------------------------------------------

#1 клавиатура
instagram_keyboard = InlineKeyboardMarkup()
button = InlineKeyboardButton('Instagram', url='https://www.instagram.com/podarok_format?igshid=NGVhN2U2NjQ0Yg==')
instagram_keyboard.add(button)

#2 клавиатура
info_keyboard = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Instagram', url='https://www.instagram.com/podarok_format?igshid=NGVhN2U2NjQ0Yg==')
button2 = InlineKeyboardButton('Купить VIP билет', url="https://google.com")
button3 = InlineKeyboardButton('Купить STANDART билет', url="https://google.com")
button4 = InlineKeyboardButton('Посмотреть количество билетов', callback_data = 'ticket:amount')
info_keyboard.add(button1, button2, button3, button4)

#Клавиатуры --------------------------------------------------------------------------------

#Айди админа
admin_id = 366254199

#сообщения
first_text = """*Отлично! Скидка успешно закреплена за тобой. Поздравляем! 🎊🔥 *\n\nТы уже на шаг ближе к тому, чтобы стать владельцем нового Changan UNI-V! *Уже очень скоро ты получишь возможность оплатить билет, по специальным условиям! 🚘*\n\nБлагодарим за доверие и остаемся на связи! 🤝"""
second_text = """*🎫 НО ЭТО ЕЩЕ НЕ ВСЕ…*\n\nПодписывайся на наш Instagram, где тебя уже ждёт много контента с бойцами POPMMA и блогерами! \n\nТам же можно будет узнать подробнее о других призах и получить приглашение на ивенты, в которых *сможешь увидеться с бойцами - лично!* 🔥🤩\n\nКстати, тут тоже будут появляться экслюзивные кадры, поэтому советуем закрепить этот бот! ⭐️"""
info_text = """ Инфо текст"""
othermessage = """"""
sendall_text = """Сообщение для рассылки"""


#Сообщения ---------------------------------------------------------------------------------

#обработка команды start
@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    if (db.user_exists(message.from_user.id)):
        print("пользователь уже есть в базе данных")
        pass
    
    else:
        print("пользователь добавляется")
        db.add_user(message.from_user.id)
        print("пользователь добавлен")
        with open('images/start_image.jpg', 'rb') as photo:
            await bot.send_photo(chat_id = message.from_user.id,photo = photo, caption=first_text, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(120)
        await bot.send_message(message.from_user.id, text=second_text, reply_markup=instagram_keyboard, parse_mode=ParseMode.MARKDOWN)

#Ещё одно сообщение
@dp.message_handler(commands = ['othermessage'])
async def othermessage(message: types.Message):
    with open('images/1moreimage.jpg', 'rb') as photo:
        await bot.send_photo(chat_id = message.from_user.id,photo = photo, caption=othermessage, parse_mode=ParseMode.MARKDOWN)

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
    
#Обработка команды info
@dp.message_handler(commands = ['info'])
async def info(message: types.Message):
    await bot.send_message(message.from_user.id, text=info_text, reply_markup=info_keyboard, parse_mode=ParseMode.MARKDOWN)

@dp.callback_query_handler(text_contains = "ticket:amount")
async def ticketamount(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, f"Количество ваших VIP билетов: {db.get_tickets(message_chat_id)[0][5]} \nКоличество ваших стандартных билетов : {db.get_tickets(message_chat_id)[0][6]}")

        
#Сообщения ---------------------------------------------------------------------------------

#Билеты ------------------------------------------------------------------------------------
 
#Получить VIP билет
@dp.message_handler(commands = ['buyVIP'])
async def buyVIP(message: types.message):
    db.add_VIP_ticket(message.chat.id)
    await bot.send_message(message.chat.id, "VIP билет куплен успешно!")
    
#Получить STANDART билет
@dp.message_handler(commands = ['buySTANDART'])
async def buyVIP(message: types.message):
    db.add_STANDART_ticket(message.chat.id)
    await bot.send_message(message.chat.id, "Стандартный билет куплен успешно!")

#Билеты ------------------------------------------------------------------------------------

#Главная функция ---------------------------------------------------------------------------   

#main function
async def main():
    logging.basicConfig(level = logging.INFO)
    await dp.start_polling(bot)
    print(1)

if __name__ == "__main__":
    asyncio.run(main())
    
#Главная функция ---------------------------------------------------------------------------   