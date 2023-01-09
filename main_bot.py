from auth import token
from parser import parser
import asyncio
from telebot import types
from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from keyboard import kb_cmd, kb_city, kb_rooms, kb_yes_no
bot = AsyncTeleBot(token, state_storage=StateMemoryStorage())


class MyStates(StatesGroup):
    city = State()
    room = State()
    price = State()
    confirmation = State()


pull_of_city = ['Новосибирск', 'Бердск', 'Обь', 'Краснообск', 'Кольцово']

pull_of_rooms = ['Студия', 'Комната', 'Дом', 'Однокомнатная квартира',
                 'Двухкомнатная квартира', 'Трёхкомнатная квартира',
                 'Четырёхкомнатная квартира', 'Подселение']


async def reset(message):
    await bot.send_message(message.from_user.id, 'Попробуйте снова.', reply_markup=kb_cmd())
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    welcome = 'Привет!\n'\
              'Этот бот поможет найти квартиру.\n' \
              'Для начала выбери город.'
    await bot.set_state(message.from_user.id, MyStates.city)
    await bot.send_message(message.from_user.id, text=welcome, reply_markup=kb_city())


@bot.message_handler(state=MyStates.city)
async def add_rooms(message):
    if message.text in pull_of_city:
        await bot.send_message(message.from_user.id, 'Выберите количество комнат.', reply_markup=kb_rooms())
        await bot.set_state(message.from_user.id, MyStates.room)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['Город'] = message.text
    else:
        await reset(message)


@bot.message_handler(state=MyStates.room)
async def add_price(message):
    if message.text in pull_of_rooms:
        await bot.send_message(message.from_user.id, 'Введите диапазон цен через дефис без пробела.\n'
                                                     'Например:15000-25000.',
                               reply_markup=types.ReplyKeyboardRemove())
        await bot.set_state(message.from_user.id, MyStates.price)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['Комнаты'] = message.text
    else:
        await reset(message)


@bot.message_handler(state=MyStates.price)
async def complete_data(message):
    if len(message.text.split('-')) == 2 and message.text.split('-')[0] != None \
            and message.text.split('-')[0].isdigit() and message.text.split('-')[1] != None \
            and message.text.split('-')[1].isdigit():

        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['Цена_от'] = int(message.text.split('-')[0])
            data['Цена_до'] = int(message.text.split('-')[1])
        await bot.set_state(message.from_user.id, MyStates.confirmation)
        await bot.send_message(message.from_user.id,
                               f'Вы ищите в городе {data["Город"]}, {data["Комнаты"]}, по цене '
                               f'{data["Цена_от"]}-{data["Цена_до"]}?',
                               reply_markup=kb_yes_no())
    else:
        await reset(message)


@bot.message_handler(state=MyStates.confirmation)
async def get_data(message):
    if message.text == 'Да':
        await bot.send_message(message.from_user.id,
                               'Идёт поиск...',
                               reply_markup=types.ReplyKeyboardRemove())
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            result = await parser(data)

        if result:
            for link, description in result.items():
                await bot.send_message(message.from_user.id,
                                       text='<a href="{}">{}</a>'.format(link, description.strip()),
                                       parse_mode='HTML')
            await bot.delete_state(message.from_user.id, message.chat.id)
        else:
            await bot.send_message(message.from_user.id,
                                   'По вашему запросу ничего не найдено. Попробуйте снова.',
                                   reply_markup=kb_cmd())
            await bot.delete_state(message.from_user.id, message.chat.id)

    else:
        await reset(message)

if __name__ == '__main__':
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    asyncio.run(bot.polling())
