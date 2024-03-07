import telebot
from telebot import types

from config import *
from photo_file_ids import *

# Import to generate a random session ID
import string
import random

# Создаем бота для Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Создаем класс для хранения данных о игроках(значения будут свапаться)
class Player:
    def __init__(self, player_id: int, username: str, chat_id: int):
        self.player_id = player_id
        self.username = username
        self.chat_id = chat_id


# Создание экземпляров класса Player
player1 = Player(player_id=0, username="", chat_id=0)
player2 = Player(player_id=0, username="", chat_id=0)


# Класс для хранения данных о игроках  вне свапов (Для корректного засчитывания очков и определения победы)
class Gainer:
    def __init__(self, player_id, username: str, score: int, session_id: str):
        self.player_id = player_id
        self.username = username
        self.score = score
        self.session_id = session_id


# Создание экземпляров класса Gainer
gainer1 = Gainer(player_id=0, username="", score=0, session_id="")
gainer2 = Gainer(player_id=0, username="", score=0, session_id="")

# Ход игры
global turn

# Dictionary to store game sessions
sessions = {}


# Function to generate a random session ID
def generate_session_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    help_message = (

        "Команда 💫 DIXIT: Начать новую игру 💫 позволяет начать игру в DIXIT: 9 lives mod. Мод представляет из себя "
        "версию "
        "игры для двоих, которая проходит в девять раундов 🎲\n\n"
        "♦️ ПРАВИЛА ИГРЫ в DIXIT: 9 lives mod: ♦️\n\n"
        "1️⃣ Для игры в DIXIT: 9 lives mod необходимо инициировать игру кнопкой 💫 DIXIT: Начать новую игру 💫 и "
        "предложить партнеру ввести команду"
        " /join\n"
        "2️⃣ В игре есть две роли ♦️ Загадочник ♦️ и ♠️ Угадайка ♠️. Инициирующий игрок будет первым ️ "
        "Загадочником, а его партнер будет Угадайкой. Игроки будут меняться ролями в ходе игры.\n"
        "3️⃣ В каждом ходе Загадочник будет выбирать карточку и его задачей будет не указывая на неё прямо "
        "обьяснить Угадайке путём ассоциаций какую карточку он загадал.\n"
        "4️⃣ Набор карточек у игроков отличается, но Угадайке всегда будет доступна любая загадываемая "
        "карточка.\n"
        "5️⃣ Победитель будет определяться по количеству набранных очков.\n\n"
        "♦️ ПРАВИЛА НАБОРА ОЧКОВ: ♦️\n\n"
        "1️⃣ Стандартный ход в случае угадывания карты приносит одно очко Угадайке, на Загадочника это не "
        "влияет.\n"
        "2️⃣ Поскольку приглашенный игрок, в отличии от инициатора имеет больше ходов, был введен суперход."
        "В пятом ходе смекалка Угадайки не только принесет ему очко, но и вычтет одно у Загадочника."
        "В обратном случае, невезение, напротив принесет дополнительное очко Загадочнику.\n\n"
        "Игра направлена лишь на 🚀 хорошее времяпрепровождение вместе 🚀 и не содержит ❌намеренных соревновательных "
        "критериев❌, "
        "так что не печальтесь в случае проигрыша.\n\n"
        "Если что-то пойдет не так, для перезапуска бота вы всегда можете ввести /start \n\n"
        "Больше информации обо мне вы сможете найти посетив "
        "https://github.com/rumiantsevaa/DIXIT_Telegram_Bot"
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
    markup.add(button1)

    # Отправляем клавиатуру пользователю
    bot.send_message(message.chat.id, start_message, reply_markup=markup)


# Начало новой игры, получение данных об инициализирующем игроке
@bot.message_handler(commands=['dixit_match_starter'], chat_types=['private'])
def dixit_match_starter(message):
    bot.send_message(message.chat.id,
                     message.from_user.username + ", Вы ♦️ Загадочник ♦️")

    player1.player_id = message.from_user.id
    player1.username = message.from_user.username
    player1.chat_id = message.chat.id

    # Добавляем игроков до свапа в глобальную переменную для засчитывания очков
    gainer1.player_id = player1.player_id
    gainer1.username = player1.username

    # Generate a random session ID
    session_id = generate_session_id()
    sessions[session_id] = gainer1
    gainer1.session_id = session_id

    bot.send_message(message.chat.id, "Попросите партнера ввести /join для "
                                      "получения статуса ♠️ Угадайка ♠️\n"
                                      f"Ваш ID сессии: {session_id}.\nТакже отправьте его "
                                      f"партнеру, чтобы он смог присоединиться.")

    # Проверка пользователя в консоли.Чтобы вывести содержимое объекта player,обращаемся к его атрибутам напрямую.
    print(" Игрок 1: ", player1.player_id, player1.username, player1.chat_id, gainer1.session_id)
    print(sessions)
    bot.register_next_step_handler(message, handle_join)


# Проверка наличия двух разных пользователей для корректной игры
def handle_check():
    # Проверка наличия двух пользователей для корректной игры, если всё ок, то игра продолжается
    if player1.player_id != 0 and player2.player_id != 0 and player1.player_id != player2.player_id:
        return True

    else:
        bot.send_message(player2.chat_id,
                         "Вы не можете играть в одиночестве. Пожалуйста, инициируйте игру заново вернувшись в меню "
                         "/start"
                         "и следуйте инструкциям. Не забудьте попросить партнера ввести /join для "
                         "получения статуса ♠️ Угадайка ♠️ ")


# Обработка команды /join и получении данных об присоединившемся игроке
def handle_join(message: types.Message):
    if message.text.lower() == '/join':
        bot.send_message(message.chat.id, "Введите ID сессии, к которой хотите присоединиться:")


def handle_join_session(message: types.Message):
    session_id = message.text
    if session_id in sessions and gainer1.session_id == session_id:
        bot.send_message(message.chat.id, player1.username + " - Ваш оппонент и ♦️ Загадочник ♦️")
        bot.send_message(message.chat.id, message.from_user.username + " - Вы ♠️ Угадайка ♠️ ")
        bot.send_message(player1.chat_id, message.from_user.username + " - получил статус ♠️ Угадайка ♠️ ")

        player2.player_id = message.from_user.id
        player2.username = message.from_user.username
        player2.chat_id = message.chat.id

        # Добавляем игроков до свапа в глобальную переменную для засчитывания очков
        gainer2.player_id = player2.player_id
        gainer2.username = player2.username

        # Проверка значений пользователя в консоли
        print(" Игрок 2: ", player2.player_id, player2.username, player2.chat_id, gainer2.session_id)
        if handle_check():
            handle_array_of_ids()
    else:
        bot.send_message(message.chat.id, "Неверный ID сессии или игра уже началась.")
        dixit_match_starter()


# Генерация и отправка карточек пользователю на основе массива из айди загруженных на сервер ТГ фотографий
def handle_array_of_ids():
    # Создаём массив айди фотографий, девять элементов
    array_of_ids = []
    for i in range(9):
        random_photo_id = random.choice(photo_file_ids)
        array_of_ids.append(random_photo_id)

    # Отправляем массив айди для Угадайки с к-м элементов : 9
    bot.send_media_group(player2.chat_id, [types.InputMediaPhoto(media) for media in array_of_ids])

    # Массив теряет три элемента,  мешается и отправляется Загадочнику
    # Антихитрин для исключения закономерности порядка элементов
    random.shuffle(array_of_ids)
    del array_of_ids[6:9]
    random.shuffle(array_of_ids)
    bot.send_media_group(player1.chat_id, [types.InputMediaPhoto(media) for media in array_of_ids])

    # Отправляем текст "Выбирайте карточку, не говорите оппоненту какую вы выбрали."
    bot.send_message(player1.chat_id, player1.username + ", выбирайте карточку, не говорите оппоненту "
                                                         "какую вы"
                                                         "выбрали.")
    bot.send_message(player2.chat_id, player2.username + " , готовьтесь слушать обьяснения "
                                                         "♦️ Загадочника ♦️")

    markupprep = types.InlineKeyboardMarkup()
    buttonprep = types.InlineKeyboardButton(text="да", callback_data="yes", one_time_keyboard=True)
    markupprep.add(buttonprep)
    message = bot.send_message(player1.chat_id, player1.username + " , готовы 👀?", reply_markup=markupprep)

    bot.register_next_step_handler(message, handle_answer)


# Выбор угадал ли игрок и засчитывание победы
def handle_answer(message):
    bot.send_message(message.chat.id, "Обьясните ♠️ Угадайке ♠️  какая ассоциация у вас с выбранной карточкой.")
    markup34 = types.InlineKeyboardMarkup()
    button3 = types.InlineKeyboardButton(text="Угадал ☑️", callback_data="true", one_time_keyboard=True)
    button4 = types.InlineKeyboardButton(text="Не угадал 🎲", callback_data="false", one_time_keyboard=True)
    markup34.add(button3, button4)

    bot.send_message(player1.chat_id, player1.username + " , угадал ли ♠️ Угадайка ♠️  вашу карточку?",
                     reply_markup=markup34)


# Обработка нажатия inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "yes":
        handle_answer(call.message)

    global turn

    if call.data == "true":
        bot.send_message(player2.chat_id, player2.username + " , вы угадали.")
        bot.send_message(player1.chat_id, player1.username + " , выбор принят.")
        try:
            turn, gainer1.score, gainer2.score
        except NameError:
            turn, gainer1.score, gainer2.score = 1, 0, 0

        # Если ход нечетный, то Gainer 2 получает очко
        if turn % 2 != 0:
            gainer2.score += 1
            print("Gainer 2 получает +1")
        elif turn == 5:
            gainer2.score += 1
            gainer1.score -= 1
        # Если ход четный, то Gainer 1 получает очко
        else:
            gainer1.score += 1
            print("Gainer 1 получает +1")
        print("ХОД:", turn, "СЧЕТ Gainer 1:", gainer1.score, "СЧЕТ Gainer 2:", gainer2.score)
        turn += 1
        handle_continue()

    if call.data == "false":
        bot.send_message(player2.chat_id, player2.username + " , вы не угадали")
        bot.send_message(player1.chat_id, player1.username + " , выбор принят.")
        try:
            turn, gainer1.score, gainer2.score
        except NameError:
            turn, gainer1.score, gainer2.score = 0, 0, 0
        if turn == 5:
            gainer2.score -= 1
            gainer1.score += 1
        else:
            gainer1.score += 0
            gainer2.score += 0
            turn += 1

        print("ХОД:", turn, "СЧЕТ Геймер 1:", gainer1.score, "СЧЕТ Геймер 2:", gainer2.score)
        handle_continue()


def handle_continue():
    if turn == 9:
        winner = gainer1.score > gainer2.score
        if winner:
            bot.send_message(player1.chat_id, "🔥🔥" + gainer1.username + "🔥🔥 - Вы победитель")
            bot.send_message(player2.chat_id, "👾" + gainer2.username + "👾 - Вы проиграли")
        elif gainer1.score == gainer2.score:
            bot.send_message(player1.chat_id, "🤔 НИЧЬЯ 🤔")
            bot.send_message(player2.chat_id, "🤔 НИЧЬЯ 🤔")
        else:
            bot.send_message(player1.chat_id, "🔥🔥" + gainer2.username + "🔥🔥 - Вы победитель")
            bot.send_message(player2.chat_id, "👾" + gainer1.username + "👾 - Вы проиграли")

        bot.send_message(player1.chat_id, "Игра окончена")
        bot.send_message(player2.chat_id, "Игра окончена")
    else:
        bot.send_message(player1.chat_id, "Теперь ваша очередь отгадывать!")  # Это первому игроку

        bot.send_message(player2.chat_id, player2.username + " , ваша очередь загадывать!")  # Это  игроку2
        # Свап игроков местами
        player1.player_id, player2.player_id = player2.player_id, player1.player_id
        player1.chat_id, player2.chat_id = player2.chat_id, player1.chat_id
        player1.username, player2.username = player2.username, player1.username
        handle_array_of_ids()


# Обработка любых текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text.lower() == 'dixit: начать новую игру':
        dixit_match_starter(message)
    elif message.text.lower() == '/join':
        handle_join(message)
    elif message.text.upper() in sessions:
        print("yes it fckng worked")
        handle_join_session(message)
    elif message.text.lower() == 'да':
        handle_answer(message)
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет! Чтобы начать, нажмите /start")
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю. Нажмите /start для списка команд.")


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
