import asyncio
import logging
import time
import config

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
from aiogram.utils.markdown import hlink
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from userid_database import SQLDatabase

from datetime import datetime, timedelta

# команды:
#     /start
#     /othermessage
#     /sendall
#     /info
#     /buyVIP
#     /buySTANDART

#Константы ---------------------------------------------------------------------------------

#Инициализируем бота
bot = Bot(token = config.bot_token)
dp = Dispatcher(bot)
status = True

#Инициализация базы данных
db = SQLDatabase('userid_db.db')

#Константы ---------------------------------------------------------------------------------

#Клавиатуры --------------------------------------------------------------------------------

#1 клавиатура FIGHTERS
fighters_keyboard = InlineKeyboardMarkup()
button1 = InlineKeyboardButton("Байра ba1raa_")
button2 = InlineKeyboardButton("Ислам «Джанго» Жангоразов")
button3 = InlineKeyboardButton("Шамиль «Пахан» Галимов")
button4 = InlineKeyboardButton("Артем Тарасов")
button5 = InlineKeyboardButton("Марат «Даггер» Исаев")
button6 = InlineKeyboardButton("Даниял «Т-34» Эльбаев")
fighters_keyboard.add(button1,button2,button3,button4,button5,button6)

#2 клавиатура VIP STANDARD
ticket_keyboard = InlineKeyboardMarkup()
button7 = InlineKeyboardButton('Купить VIP билет', url="https://google.com")
button8 = InlineKeyboardButton('Купить STANDARD билет', url="https://google.com")
ticket_keyboard.add(button1, button2)

#3 клавиатура STANDARD
standard_keyboard = InlineKeyboardMarkup()
standard_keyboard.add(button8)

#4 клавиатура VIP
vip_keyboard = InlineKeyboardMarkup()
vip_keyboard.add(button7)

#4 клавиатура стать победителем
bethewinner_keyboard = InlineKeyboardMarkup()
button9 = InlineKeyboardButton('Стать победителем', callback_data = 'bethewinner')
bethewinner_keyboard.add(button9)
#Клавиатуры --------------------------------------------------------------------------------

#Айди админа
admin_id = 366254199

#Сообщения ---------------------------------------------------------------------------------

#Вебхук-------------------------------------------------------------------------------------

async def on_startup(dp):
    await bot.set_webhook(congig.URL_APP)

async def on_startup(dp):
    await bot.delete_webhook()
    
#Вебхук-------------------------------------------------------------------------------------

@dp.message_handler(state = user_add_username)
async def name_add(message: types.Message):
    db.add_name(message.text, message.from_user.id)
    await bot.send_message(message_chat_id, config.third_text, parse_mode=ParseMode.MARKDOWN)
@dp.message_handler(state = user_add_phone_number)
async def phone_number_add(message: types.Message):
    db.add_phone_number(message.text, message.from_user.id)
    await bot.send_message(message_chat_id, config.fourth_text, parse_mode=ParseMode.MARKDOWN)
@dp.message_handler(state = user_add_telegram_id)
async def telegram_id_add(message: types.Message):
    db.add_telegram_id(message.text, message.from_user.id)
    await bot.send_message(message_chat_id, config.fifth_text, reply_markup = fighters_keyboard, parse_mode=ParseMode.MARKDOWN)




#
@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    if (db.user_exists(message.from_user.id)):
        print("пользователь уже есть в базе данных")
        pass
    
    else:
        print("пользователь добавляется")
        db.add_user(message.from_user.id)
        print("пользователь добавлен")  
        await bot.send_message(message.from_user.id, config.first_text, reply_markup=bethewinner_keyboard , parse_mode=ParseMode.MARKDOWN)

@dp.callback_query_handler(text_contains = "bethewinner")
async def ticketamount(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_answer(message_chat_id, config.second_text, parse_mode=ParseMode.MARKDOWN)
    

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
@dp.message_handler(commands = ['buySTANDARВ'])
async def buyVIP(message: types.message):
    db.add_STANDART_ticket(message.chat.id)
    await bot.send_message(message.chat.id, "Стандартный билет куплен успешно!")

#Билеты ------------------------------------------------------------------------------------

#Главная функция ---------------------------------------------------------------------------   

#main function
async def main():
    logging.basicConfig(level = logging.INFO)
    await dp.start_polling(bot)
    await dp.start_webhook(
        dispatcher = dp,
        webhook_path = "",
        on_startup = on_startup,
        on_shutdown = on_shutdown,
        skip_updates = True,
        host = "0.0.0.0",
        port = int(os.environ.get("PORT",5000)
        )
    )

if __name__ == "__main__":
    db.create_tables()
    asyncio.run(main())
    
#Главная функция ---------------------------------------------------------------------------   