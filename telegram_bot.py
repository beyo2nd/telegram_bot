import asyncio
import logging
import time
import config

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, CallbackQuery
from aiogram.utils.markdown import hlink
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import LabeledPrice
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
#     /buySTANDARD

#Константы ---------------------------------------------------------------------------------

#Инициализируем бота
bot = Bot(token = config.bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
status = True

#Инициализация базы данных
db = SQLDatabase('userid_db.db')

#Константы ---------------------------------------------------------------------------------

#Клавиатуры --------------------------------------------------------------------------------

#13 Клавиатура узнать больше
know_more_keyboard = InlineKeyboardMarkup()
button12 = InlineKeyboardButton("STANDARD", callback_data = "know_more_STANDARD")
button13 = InlineKeyboardButton("VIP", callback_data = "know_more_VIP")
know_more_keyboard.add(button12,button13)

#1 клавиатура VIP STANDARD
ticket_keyboard = InlineKeyboardMarkup()
button1 = KeyboardButton('Беру VIP', callback_data="buy_VIP_ticket")
button2 = KeyboardButton('Беру Standard', callback_data="buy_STANDARD_ticket")
ticket_keyboard.add(button1, button2)

#2 клавиатура STANDARD
STANDARD_keyboard = InlineKeyboardMarkup()
STANDARD_keyboard.add(button2, button13)

#3 клавиатура VIP
VIP_keyboard = InlineKeyboardMarkup()
VIP_keyboard.add(button1)

#4 клавиатура how
how_keyboard = InlineKeyboardMarkup()
button3 = InlineKeyboardButton('Как? 😳', callback_data = 'how')
how_keyboard.add(button3)

#5 клавиатура узнать детальнее
more_info_keyboard = InlineKeyboardMarkup()
button4 = InlineKeyboardButton('Выбрать', callback_data ='more_info')
more_info_keyboard.add(button4)

#6 Клавиатура узнать про призы
know_about_prizes_keyboard = InlineKeyboardMarkup()
button5 = InlineKeyboardButton('Узнать про призы', callback_data = 'know_about_prizes')
know_about_prizes_keyboard.add(button5)

#7 Клавиатура выбрать
choose_keyboard = InlineKeyboardMarkup()
button6 = InlineKeyboardButton('Выбрать', callback_data = 'choose')
choose_keyboard.add(button6)

#8 Клавиатура what more
what_more_keyboard = InlineKeyboardMarkup()
button7 = InlineKeyboardButton('Что еще?', callback_data = 'what_more')
what_more_keyboard.add(button7)

#9 Клавиатура хочу учавствовать
wanna_participate_keyboard = InlineKeyboardMarkup()
button8 = InlineKeyboardButton("Хочу участвовать",callback_data = 'wanna_participate')
wanna_participate_keyboard.add(button8)

#10 Клавиатура Забрать
get_prize_keyboard = InlineKeyboardMarkup()
button9 = InlineKeyboardButton("Забрать", callback_data = 'get_prize')
get_prize_keyboard.add(button9)

#11 Клавиатура pre_register
pre_register_keyboard = InlineKeyboardMarkup()
button10 = InlineKeyboardButton("Заполняю", callback_data = "pre_register")
pre_register_keyboard.add(button10)

#12 Клавиатура Заполняю!
register_keyboard = InlineKeyboardMarkup()
button11 = InlineKeyboardButton("Заполняю!", callback_data = "register")
register_keyboard.add(button11)

#14 клавиатура после оплаты
success_keyboard = InlineKeyboardMarkup()
button14 = InlineKeyboardButton("Забрать", callback_data="success")
success_keyboard.add(button14)

#Клавиатуры--------------------------------------------------------------------------------

#Айди админа
admin_id = 366254199

#Сообщения ---------------------------------------------------------------------------------

#Вебхук-------------------------------------------------------------------------------------

async def on_startup(dp):
    await bot.set_webhook(config.URL_APP)

async def on_shutdown(dp):
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

#Добавить номер
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

#Добавить телеграм айди  
@dp.message_handler(state = user_add.telegram_id)
async def add_telegram_id(message: types.Message, state = FSMContext):
    print("add_telegram_id")
    await state.finish()
    db.add_telegram_id(message.text, message.from_user.id)
    await bot.send_message(message.chat.id, config.ninth_text, reply_markup = more_info_keyboard, parse_mode = ParseMode.MARKDOWN)


#Регистрация пользователя-------------------------------------------------------------------

#Оплата-------------------------------------------------------------------------------------

#buy vip callback 
@dp.callback_query_handler(text_contains = "buy_VIP_ticket")
async def buyVIP(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    if config.payments_token.split(':')[1] == 'TEST':
        await bot.send_message(message_chat_id, "Тестовый платеж!!!")
    prices = [LabeledPrice(label='VIP билет', amount=250000)]
    await bot.send_invoice(
        chat_id=message_chat_id,
        title='Покупка билета VIP',                                        
        description="""Возможность забрать:              
1 - Changan UNI-V                                        
4 - iPhone 14                                            
10 - Подар-х карт «Золотое Яблоко»  10 000               
30 - Подар-х боксов «TITANMAN»
""",
        provider_token=config.payments_token,
        currency='rub',
        prices=prices,
        start_parameter='buyticket',
        payload=str(message_chat_id)
    )
    
#buy STANDARD callback 
@dp.callback_query_handler(text_contains = "buy_STANDARD_ticket")
async def buy(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    if config.payments_token.split(':')[1] == 'TEST':
        await bot.send_message(message_chat_id, "Тестовый платеж!!!")
    prices = [LabeledPrice(label='VIP билет', amount=100000)]
    await bot.send_invoice(
        chat_id=message_chat_id,
        title='STANDARD',
        description='Гайд «На шаг ближе к успеху»\n Участие в розыгрыше  автомобиля Changan UNI-V',
        provider_token=config.payments_token,
        currency='rub',
        prices=prices,
        start_parameter='buyticket',
        payload=str(message_chat_id)
    )
#Оплата-------------------------------------------------------------------------------------

#старт
@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    if (db.user_exists(message.from_user.id)):
        print("пользователь уже есть в базе данных")
        pass
    else:
        print("пользователь добавляется")
        db.add_user(message.from_user.id)
        print("пользователь добавлен")  
        await bot.send_message(message.from_user.id, config.first_text, reply_markup=how_keyboard , parse_mode=ParseMode.MARKDOWN)

#how callback
@dp.callback_query_handler(text_contains = "how")
async def how(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    photo = open('images/first_image.png', 'rb')
    await bot.send_photo(message_chat_id, photo = photo, caption = config.first_first_text, reply_markup = what_more_keyboard, parse_mode=ParseMode.MARKDOWN)

#what_more callback
@dp.callback_query_handler(text_contains = "what_more")
async def what_more(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, config.first_second_text, reply_markup = wanna_participate_keyboard, parse_mode=ParseMode.MARKDOWN) 

#wanna_participate callback
@dp.callback_query_handler(text_contains = "wanna_participate")
async def wanna_participate(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, config.first_third_text, reply_markup=get_prize_keyboard,  parse_mode=ParseMode.MARKDOWN)

#get_prize callback
@dp.callback_query_handler(text_contains = "get_prize")
async def get_prize(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    #with open (videos/first_video, "rb") as video:
    #    await bot.send_video(message_chat_id, config.first_fourth_text, video = video, reply_markup=get_prize)
    photo = open("images/first_image.png", "rb")
    await bot.send_photo(message_chat_id, photo = photo, caption = config.first_fifth_text, parse_mode=ParseMode.MARKDOWN)  
    
    await bot.send_message(message_chat_id, config.first_sixth_text, reply_markup=pre_register_keyboard,  parse_mode=ParseMode.MARKDOWN)

#pre_register callback
@dp.callback_query_handler(text_contains = "pre_register")
async def pre_register(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, config.first_seventh_text, reply_markup=register_keyboard,  parse_mode=ParseMode.MARKDOWN)
#register callback
@dp.callback_query_handler(text_contains = "register")
async def register(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, config.second_text, parse_mode=ParseMode.MARKDOWN)
    await user_add.name.set()
    
#Тарифы бота
@dp.callback_query_handler(text_contains = "more_info") 
async def more_info(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    await bot.send_message(message_chat_id, config.fifth_text, reply_markup = know_more_keyboard, parse_mode=ParseMode.MARKDOWN)
    
#тариф стиандарт
@dp.callback_query_handler(text_contains = "know_more_STANDARD")
async def know_more_STANDARD(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    photo = open("images/first_image.png", "rb")
    await bot.send_photo(message_chat_id, photo = photo, caption = config.seventh_text, reply_markup = STANDARD_keyboard, parse_mode=ParseMode.MARKDOWN)

    
#тариф вип
@dp.callback_query_handler(text_contains = "know_more_VIP")
async def know_more_VIP(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    photo = open("images/first_image.png", "rb")
    await bot.send_photo(message_chat_id, photo = photo, caption = config.eighth_text, reply_markup = VIP_keyboard, parse_mode=ParseMode.MARKDOWN)

#Выдача гайда
@dp.callback_query_handler(text_contains = "success")
async def give_guidecall(call: CallbackQuery):
    message_chat_id = call["from"]["id"]
    #Выдача гайда
    await bot.send_message(message_chat_id, f"""31 декабря 2023 года у нас будет розыгрыш среди тех, кто купил наш гайд, и вот твой номер: {message_chat_id}.

Не потеряй и не пропусти день розыгрыша и возможно именно ты станешь обладателем автомобиля CHANGAN UNI-V.

*Если ты хочешь увеличить шансы на победу, предложи другу приобрести билет, отправь ему ссылку на бот или купи еще один в подарок другу и жди вместе с другом день розыгрыша.*
""", parse_mode=ParseMode.MARKDOWN)
    
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
    photo = open("images/first_image.png", "rb")
    await bot.send_photo(message.chat.id, photo = photo, caption = config.twelve_text, reply_markup = success_keyboard, parse_mode=ParseMode.MARKDOWN)
    
#Получить STANDARD билет
@dp.message_handler(commands = ['buySTANDARD'])
async def buyVIP(message: types.message):
    db.add_STANDARD_ticket(message.chat.id)
    photo = open("images/first_image.png", "rb")
    await bot.send_photo(message.chat.id, photo = photo,caption = config.twelve_text, reply_markup = success_keyboard, parse_mode=ParseMode.MARKDOWN)

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
