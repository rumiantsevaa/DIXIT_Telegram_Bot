import telebot
from telebot import types

from config import *
from photo_file_ids import *

import random

# Создаем бота для Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# URL для отправки изображения
url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto'

# Множество для хранения обработанных идентификаторов файлов
processed_photo_ids = set()


# declare global variables outside any function by using the global keyword
# ИД Роли Игрок1
global player1id
global player1username
global player1chat_id

# ИД Роли Игрок2
global player2id
global player2username
global player2chat_id

# Постоянная переменная для хранения ИД и назначения счета
global gainer1
global gainer2

# Счет
global score

# Ход
global turn


# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    help_message = (

        "Команда 💫 DIXIT: Начать новую игру 💫 позволяет начать игру в DIXIT: 9 lives mod. Мод представляет из себя "
        "версию"
        "игры для двоих, которая проходит в девять раундов 🎲\n\n"
        "♦️ ПРАВИЛА ИГРЫ в DIXIT: 9 lives mod: ♦️\n"
        "Тут будет МНОГА БУКАФФ\n\n"
        "Команда 💫 Получить Telegram Photo ID 💫 реализует загрузку фотографии на сервер Telegram и получение "
        "идентификатора.\n\n"
        "Для перезапуска бота вы всегда можете ввести /start \n\n"
        "Больше информации обо мне вы сможете найти посетив.."
    )
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['start'])
def start_button_handler(message):
    # Приветствие пользователя
    start_message = ("Здраствуйте! Я бот для игры в DIXIT: 9 lives mod. Мне кажется мы уже где-то виделись🤔 Но, "
                     "я совсем этого не помню. Чтобы начать игру,"
                     "нажмите кнопку 💫 DIXIT: Начать новую игру 💫 или узнайте больше обо мне по команде /help.")

    # Создаем клавиатуру с кнопкой "Старт"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("DIXIT: Начать новую игру")
    button2 = types.KeyboardButton("Получить Telegram Photo ID")
    markup.add(button1, button2)

    # Отправляем клавиатуру пользователю
    bot.send_message(message.chat.id, start_message, reply_markup=markup)


@bot.message_handler(commands=['random_photos_generator'], chat_types=['private'])
def photo_generator_command(message):
    global player1id
    global player1username
    global player1chat_id

    bot.send_message(message.chat.id,
                     message.from_user.username + ", Вы ♦️ Игрок 1 ♦️ Попросите партнера ввести /join"
                                                  " для "
                                                  "получения статуса ♠️ Игрок 2 ♠️")
    player1id = message.from_user.id
    player1username = message.from_user.username
    player1chat_id = message.chat.id

    # Проверка значений пользователя в консоли
    print(" Игрок 1: ", player1id, player1username, player1chat_id)


def handle_join(message: types.Message):
    global player2id
    global player2username
    global player2chat_id

    if message.text.lower() == '/join':
        bot.send_message(message.chat.id, player1username + " - Ваш оппонент и ♦️ Игрок 1 ♦️")
        bot.send_message(message.chat.id, message.from_user.username + " - Вы ♠️ Игрок 2 ♠️")
        bot.send_message(player1chat_id, message.from_user.username + " - получил статус ♠️ Игрок 2 ♠️")

        player2id = message.from_user.id
        player2username = message.from_user.username
        player2chat_id = message.chat.id

    # Проверка значений пользователя в консоли
    print(" Игрок 2: ", player2id, player2username, player2chat_id)

    # Проверка наличия двух пользователей для корректной игры, если всё ок, то используем pass (ничего не делает)
    if player1id != player2id and player1id is not None and player2id is not None:
        pass
    else:
        bot.send_message(player2chat_id,
                         "Что-то пошло не так.Пожалуйста, инициируйте игру заново вернувшись в меню "
                         "и следуйте инструкциям. Не забудьте попросить партнера ввести /join для "
                         "получения статуса ♠️ Игрок 2 ♠️")

    # Создаём массив айди фотографий, девять элементов
    array_of_ids = []
    for i in range(9):
        random_photo_id = random.choice(photo_file_ids)
        array_of_ids.append(random_photo_id)

    # Отправляем массив айди для общего чата с к-м элементов : 9
    bot.send_media_group(player2chat_id, [types.InputMediaPhoto(media) for media in array_of_ids])

    # Массив теряет три элемента,  мешается и отправляется Игроку 1
    # Антихитрин
    random.shuffle(array_of_ids)
    del array_of_ids[6:9]
    random.shuffle(array_of_ids)
    bot.send_media_group(player1chat_id, [types.InputMediaPhoto(media) for media in array_of_ids])

    # Отправляем текст "Выбирайте карточку, не говорите оппоненту какую вы выбрали."
    bot.send_message(player1chat_id, player1username + ", выбирайте карточку, не говорите оппоненту какую вы "
                                                       "выбрали.")
    bot.send_message(player2chat_id, player2username + " , готовьтесь слушать обьяснения ♦️ Игрока 1 ♦️")

    markupprep = types.InlineKeyboardMarkup()
    buttonprep = types.InlineKeyboardButton(text="да", callback_data="yes", one_time_keyboard=True)
    markupprep.add(buttonprep)
    bot.send_message(player1chat_id, player1username + " , готовы 👀?", reply_markup=markupprep)

    bot.register_next_step_handler(message, handle_answer)


# Выбор угадал ли игрок и засчитывание победы


def handle_answer(message):
    bot.send_message(message.chat.id, "Обьясните ♠️ Игроку 2 ♠️ какая ассоциация у вас с выбранной карточкой.")
    markup34 = types.InlineKeyboardMarkup()
    button3 = types.InlineKeyboardButton(text="Угадал ☑️", callback_data="true", one_time_keyboard=True)
    button4 = types.InlineKeyboardButton(text="Не угадал 🎲", callback_data="false", one_time_keyboard=True)
    markup34.add(button3, button4)

    bot.send_message(player1chat_id, player1username + " , угадал ли ♠️ Игрок 2 ♠️ вашу карточку?",
                     reply_markup=markup34)


# def scores_update(message):


@bot.message_handler(commands=['photo_save'])
def photo_save_command(message):
    bot.send_message(chat_id=message.chat.id, text="Пожалуйста, отправьте мне фотографии, ID которых вы хотите "
                                                   "сохранить.")
    bot.register_next_step_handler(message, handle_photos)


# Обработка фотографий
def handle_photos(message):
    # Выбираем максимальное разрешение
    photo = max(message.photo, key=lambda x: x.width * x.height)
    file_id = photo.file_id

    # Проверка наличия идентификатора в множестве
    if file_id not in processed_photo_ids:
        processed_photo_ids.add(file_id)
        bot.send_message(chat_id=message.chat.id, text=f"Идентификатор вашей фотографии: {file_id}")
    else:
        bot.send_message(chat_id=message.chat.id,
                         text=f"Идентификатор {file_id} уже обработан. Дубликаты не выводятся.")


# Обработка нажатия inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "yes":
        handle_answer(call.message)

    global score
    global turn

    if call.data == "true":
        bot.send_message(player2chat_id, player2username + " , вы угадали.")
        bot.send_message(player1chat_id, player1username + " , выбор принят.")
        try:
            turn, score
        except NameError:
            turn, score = 0, 0

        score += 1
        turn += 1

        print("ХОД:", turn, "СЧЕТ:", score)
        handle_continue(call.message)

    if call.data == "false":
        bot.send_message(player2chat_id, player2username + " , вы не угадали")
        bot.send_message(player1chat_id, player1username + " , выбор принят.")
        try:
            turn, score
        except NameError:
            turn, score = 0, 0
        score += 0
        turn += 1

        print("ХОД:", turn, "СЧЕТ:", score)
        handle_continue(call.message)

    if call.data == "continue":
        photo_generator_command(call.message)


def handle_continue(message):
    bot.send_message(message.chat.id, "Теперь ваша очередь отгадывать!")  # Это первому игроку
    markup5 = types.InlineKeyboardMarkup()
    button5 = types.InlineKeyboardButton(text="ПРОДОЛЖИТЬ", callback_data="continue", one_time_keyboard=True)
    markup5.add(button5)
    bot.send_message(player2chat_id, player2username + " , ваша очередь загадывать!",
                     reply_markup=markup5)  # Это  игроку2 как и кнопка продолжить


# Обработка любых текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text.lower() == 'dixit: начать новую игру':
        photo_generator_command(message)
    elif message.text.lower() == 'получить telegram photo id':
        photo_save_command(message)
    elif message.text.lower() == '/join':
        handle_join(message)
    elif message.text.lower() == 'да':
        handle_answer(message)
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет! Чтобы начать, нажмите /start")
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю. Нажмите /start для списка команд.")


# Запуск бота
bot.polling(none_stop=True, interval=0)
