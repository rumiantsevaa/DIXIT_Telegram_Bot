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

# ID группы
GROUP_ID = bot.get_chat("-100ххх").id
PERSONAL_CHAT_ID = bot.get_chat("ххх").id
# declare global variables outside any function by using the global keyword
global player1
global player2


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


@bot.message_handler(commands=['random_photos_generator'])
def photo_generator_command(message):
    global player1
    bot.send_message(PERSONAL_CHAT_ID, message.from_user.username + ", Вы ♦️ Игрок 1 ♦️ Попросите партнера ввести /join"
                                                                    "для"
                                                                    "получения статуса ♠️ Игрок 2 ♠️")
    #    bot.forward_message(GROUP_ID, message.chat.id, message.message_id)
    player1 = message.from_user.username


def handle_join(message: types.Message):
    global player2
    if message.text in trigger_list:
        bot.send_message(GROUP_ID, message.from_user.username + " - Вы ♠️ Игрок 2 ♠️")
        player2 = message.from_user.username
        bot.send_message(GROUP_ID, message.from_user.username + " - получил статус ♠️ Игрок 2 ♠️")

    # Создаём массив айди фотографий, девять элементов
    array_of_ids = []
    for i in range(9):
        random_photo_id = random.choice(photo_file_ids)
        array_of_ids.append(random_photo_id)

    # Отправляем массив айди для общего чата с к-м элементов : 9
    bot.send_media_group(GROUP_ID, [types.InputMediaPhoto(media) for media in array_of_ids])

    # Массив теряет три элемента,  мешается и отправляется Игроку 1
    # Антихитрин
    random.shuffle(array_of_ids)
    del array_of_ids[6:9]
    random.shuffle(array_of_ids)
    bot.send_media_group(PERSONAL_CHAT_ID, [types.InputMediaPhoto(media) for media in array_of_ids])

    # Отправляем текст "Выбирайте карточку, не говорите оппоненту какую вы выбрали."
    bot.send_message(PERSONAL_CHAT_ID, player1 + "  , выбирайте карточку, не говорите оппоненту какую вы выбрали.")
    bot.send_message(GROUP_ID, player2 + " , готовьтесь слушать обьяснения ♦️ Игрока 1 ♦️")


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


# Обработка любых текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text.lower() == 'dixit: начать новую игру':
        photo_generator_command(message)
    elif message.text.lower() == 'получить telegram photo id':
        photo_save_command(message)
    elif message.text.lower() == '/join':
        handle_join(message)
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет! Чтобы начать, нажмите /start")
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю. Нажмите /start для списка команд.")


# Запуск бота
bot.polling(none_stop=True, interval=0)
