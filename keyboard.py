from telebot import types


def kb_cmd():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    return keyboard.add('/start')


def kb_yes_no():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    return keyboard.add('Да', 'Нет')


def kb_rooms():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Подселение', 'Дом')
    keyboard.add('Студия', 'Комната')
    keyboard.add('Однокомнатная квартира', 'Двухкомнатная квартира')
    keyboard.add('Трёхкомнатная квартира', 'Четырёхкомнатная квартира')
    return keyboard


def kb_city():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    return keyboard.add('Новосибирск').add('Бердск').add('Обь').add('Краснообск').add('Кольцово')
