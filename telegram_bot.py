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
dp = Dispatcher(bot, storage=MemoryStorage())
status = True

#Инициализация базы данных
db = SQLDatabase('userid_db.db')

#Константы ---------------------------------------------------------------------------------

#Клавиатуры --------------------------------------------------------------------------------

#1 клавиатура VIP STANDARD
ticket_keyboard = InlineKeyboardMarkup()
button1 = InlineKeyboardButton('Купить VIP билет', url="https://google.com")
button2 = InlineKeyboardButton('Купить STANDARD билет', url="https://google.com")
ticket_keyboard.add(button1, button2)

#2 клавиатура STANDARD
standard_keyboard = InlineKeyboardMarkup()
standard_keyboard.add(button2)

#3 клавиатура VIP
vip_keyboard = InlineKeyboardMarkup()
vip_keyboard.add(button1)

#4 клавиатура стать победителем
bethewinner_keyboard = InlineKeyboardMarkup()
button3 = InlineKeyboardButton('Стать победителем', callback_data = 'bethewinner')
bethewinner_keyboard.add(button3)

#5 клавиатура узнать детальнее
more_info_keyboard = InlineKeyboardMarkup()
button4 = InlineKeyboardButton('Узнать детальнее', callback_data ='more_info')
more_info_keyboard.add(button4)

#6 Клавиатура узнать про призы
know_about_prizes_keyboard = InlineKeyboardMarkup()
button5 = InlineKeyboardButton('Узнать про призы', callback_data = 'know_about_prizes')
know_about_prizes_keyboard.add(button5)

# Клавиатура выбрать
choose_keyboard = InlineKeyboardMarkup()
button6 = InlineKeyboardButton('Выбрать', callback_data = 'choose')
choose_keyboard.add(button6)

# Клавиатура ошибка фио
fail_keyboard = InlineKeyboardMarkup()
button7 = InlineKeyboardButton('Ввести заново', callback_data = 'bethewinner')
bethewinner_keyboard.add(button7)

#Клавиатуры--------------------------------------------------------------------------------

#Айди админа
admin_id = 366254199

#Сообщения ---------------------------------------------------------------------------------

#Вебхук-------------------------------------------------------------------------------------

async def on_startup(dp):
    await bot.set_webhook(congig.URL_APP)

async def on_startup(dp):
    await bot.delete_webhook()
    
#Вебхук-------------------------------------------------------------------------------------

#Регистрация пользователя-------------------------------------------------------------------
class user_add(StatesGroup):
    name = State()
    phone_number = State()
    telegram_id = State()

#Добавить ФИО
@dp.message_handler(state = user_add.name)
async def add_name(message: types.Message, state = FSMContext):
    print("add_name")
    await state.finish()
    if len(message.text.split()) <3:
        await bot.send_message(message.chat.id, "Ошибка\nВведите ФИО в формате:\n Фамилия Имя Отчество", parse_mode=ParseMode.MARKDOWN)
        await user_add.name.set()
    else:
        db.add_name(message.text, message.from_user.id)
        await bot.send_message(message.chat.id, config.third_text, parse_mode=ParseMode.MARKDOWN)
        await user_add.phone_number.set()

@dp.message_handler(state = user_add.phone_number)
async def add_phone_number(message: types.Message, state = FSMContext):
    print("add_phone")
    await state.finish()
    if 11>len(list(message.text)) <17:
        await bot.send_message(message.chat.id, "Ошибка\nВведите номер в формате:\n 89997776655", parse_mode=ParseMode.MARKDOWN)
        await user_add.phone_number.set()   
    else:
        db.add_phone_number(message.text, message.from_user.id)
        await bot.send_message(message.chat.id, config.fourth_text, parse_mode=ParseMode.MARKDOWN)
        await user_add.telegram_id.set()
    
@dp.message_handler(state = user_add.telegram_id)
async def add_telegram_id(message: types.Message, state = FSMContext):
    print("add_telegram_id")
    await state.finish()
    db.add_telegram_id(message.text, message.from_user.id)
    await bot.send_message(message.chat.id, config.sixth_text, reply_markup = more_info_keyboard, parse_mode = ParseMode.MARKDOWN)
    
#Регистрация пользователя-------------------------------------------------------------------




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

#bethewinner callback
@dp.callback_query_handler(text_contains = "bethewinner")
async def bethewinner(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, config.second_text, parse_mode=ParseMode.MARKDOWN)
    await user_add.name.set()
    
#more_info callback
@dp.callback_query_handler(text_contains = "more_info")
async def more_info(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, config.seventh_text, parse_mode=ParseMode.MARKDOWN)
    await asyncio.sleep(15)
    await bot.send_message(message_chat_id, config.eighth_text, reply_markup = know_about_prizes_keyboard,parse_mode = ParseMode.MARKDOWN)

#know_about_prizes callback
@dp.callback_query_handler(text_contains = "know_about_prizes")
async def know_about_prizes(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, config.ninth_text, reply_markup = choose_keyboard, parse_mode=ParseMode.MARKDOWN)
    
#choose callback
@dp.callback_query_handler(text_contains = "choose")
async def choose(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, config.tenth_text, reply_markup = ticket_keyboard, parse_mode=ParseMode.MARKDOWN)

#
    
    
    

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
    db.create_table1()
    db.create_table2()
    asyncio.run(main())
    
#Главная функция ---------------------------------------------------------------------------   
