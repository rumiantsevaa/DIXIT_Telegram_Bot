import telebot
from telebot import types
from config import *
from photo_file_ids import *
from DIXIT_db import conn
from utils import *
from models import *
from handlers import help_message, start_message

import sqlite3


# Создаем бота для Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, help_message)


# Команда /start
@bot.message_handler(commands=['start'])
def start_button_handler(message):
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
    # Добавляем игроков в класс Player для определения ролей
    player1.player_id = message.from_user.id
    player1.username = message.from_user.username
    player1.chat_id = message.chat.id

    # Добавляем игроков до свапа в класс Gainer для засчитывания очков
    gainer1.player_id = player1.player_id
    gainer1.username = player1.username
    # Генерация радомного session ID и запись Gainer DB
    session_id = generate_session_id()
    gainer1.session_id = session_id

    # Добавляем исключение в фильтр входящих сообщений
    sessions[session_id] = gainer1.session_id

    # Запись в базу данных для Player1
    c = conn.cursor()
    c.execute(
        "INSERT INTO Gainers (gainer1_player_id, gainer1_username, gainer1_score, gainer1_session_id, "
        "player1_player_id, player1_username, player1_chat_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (gainer1.player_id, gainer1.username, 0, gainer1.session_id,
         player1.player_id, player1.username, player1.chat_id))
    conn.commit()

    bot.send_message(message.chat.id, "Попросите партнера ввести /join для "
                                      "получения статуса ♠️ Угадайка ♠️\n"
                                      f"Ваш ID сессии: {gainer1.session_id}.\nТакже отправьте его "
                                      f"партнеру, чтобы он смог присоединиться.")

    # По ID сессии выполняем запрос в базу данных на вывод всез данных о Gainer1 + Player1 (2 - None)
    c.execute("SELECT * FROM Gainers WHERE gainer1_session_id = ?", [gainer1.session_id])
    result = c.fetchone()
    # Проверка на наличие значений в базе данных
    if result:
        result = list(result)
        print("Row retrieved:", result)
    else:
        print("No values found in the database for session ID:", gainer1.session_id)
    bot.register_next_step_handler(message, handle_join)


# Обработка команды /join и получении данных об присоединившемся игроке
def handle_join(message: types.Message):
    if message.text.lower() == '/join':
        bot.send_message(message.chat.id, "Введите ID сессии, к которой хотите присоединиться:")


def handle_join_session(message: types.Message):
    session_id = message.text
    id_to_check = message.from_user.id

    # Query the database for the session_id
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM Gainers WHERE gainer1_session_id = ?", [session_id])
    result = c.fetchone()

    if result and result['gainer1_session_id'] == session_id:
        if result['gainer1_session_id'] and result['gainer2_session_id'] is not None:
            bot.send_message(message.chat.id,
                             "Вы не можете влезть в чужую игру. Пожалуйста, инициируйте игру заново вернувшись в меню "
                             "/start.")
            return None
        elif result['gainer1_player_id'] == id_to_check:
            bot.send_message(player1.chat_id,
                             "Вы не можете играть в одиночестве. Пожалуйста, инициируйте игру заново вернувшись в меню "
                             "/start"
                             " и следуйте инструкциям. Не забудьте попросить партнера ввести /join для "
                             "получения статуса ♠️ Угадайка ♠️ ")
            return None
        else:
            gainer2.session_id = session_id

            bot.send_message(message.chat.id, player1.username + " - Ваш оппонент и ♦️ Загадочник ♦️")
            bot.send_message(message.chat.id, message.from_user.username + " - Вы ♠️ Угадайка ♠️ ")
            bot.send_message(player1.chat_id, message.from_user.username + " - получил статус ♠️ Угадайка ♠️ ")

            player2.player_id = message.from_user.id
            player2.username = message.from_user.username
            player2.chat_id = message.chat.id

            # Добавляем игроков до свапа в глобальную переменную для засчитывания очков
            gainer2.player_id = player2.player_id
            gainer2.username = player2.username

            # Запись в бд таблицу Gainers Gainer2 + Player2 присоединившегося игрока
            c = conn.cursor()
            c.execute(
                "UPDATE Gainers SET gainer2_player_id = ?, gainer2_username = ?, gainer2_score = ?, "
                "gainer2_session_id = ?, player2_player_id = ?, player2_username = ?, player2_chat_id = ? WHERE "
                "gainer1_session_id = ?",
                (gainer2.player_id, gainer2.username, 0, gainer2.session_id,
                 player2.player_id, player2.username, player2.chat_id, session_id))
            conn.commit()

            # По ID сессии выполняем запрос в базу данных на вывод всех данных о Gainer2 + 1
            c.execute("SELECT * FROM Gainers WHERE gainer2_session_id = ?", [gainer2.session_id])
            result = c.fetchone()

            # Проверка на наличие значений в базе данных
            if result:
                result = list(result)
                print("Row retrieved:", result)
            else:
                print("No values found in the database for session ID:", gainer2.session_id)
    else:
        bot.send_message(message.chat.id, "Эта сессия не существует. Пожалуйста, инициируйте игру заново "
                                          "вернувшись в меню /start.")
        return None

    c.close()
    handle_array_of_ids(session_id)


# Генерация и отправка карточек пользователю на основе массива из айди загруженных на сервер ТГ фотографий
def handle_array_of_ids(session_id):
    # Создаём массив айди фотографий, девять элементов
    array_of_ids = []
    for i in range(9):
        random_photo_id = random.choice(photo_file_ids)
        array_of_ids.append(random_photo_id)

    # По ID сессии выполняем запрос о совпадение с данными игроков Gainers
    c = conn.cursor()
    c.execute("SELECT * FROM Gainers WHERE gainer2_session_id = ?", [session_id])
    result = c.fetchone()

    # Отправляем массив айди для Угадайки с к-м элементов : 9
    bot.send_media_group(result["player2_chat_id"], [types.InputMediaPhoto(media) for media in array_of_ids])

    # Массив теряет три элемента,  мешается и отправляется Загадочнику
    # Антихитрин для исключения закономерности порядка элементов
    random.shuffle(array_of_ids)
    del array_of_ids[6:9]
    random.shuffle(array_of_ids)
    bot.send_media_group(result["player1_chat_id"], [types.InputMediaPhoto(media) for media in array_of_ids])

    # Отправляем текст "Выбирайте карточку, не говорите оппоненту какую вы выбрали."
    bot.send_message(result["player1_chat_id"],
                     result["player1_username"] + ", выбирайте карточку, не говорите оппоненту "
                                                  "какую вы"
                                                  "выбрали.")
    bot.send_message(result["player2_chat_id"], result["player2_username"] + " , готовьтесь слушать обьяснения "
                                                                             "♦️ Загадочника ♦️")
    markup999 = types.InlineKeyboardMarkup()
    button99 = types.InlineKeyboardButton(text="ДА", callback_data="yes", one_time_keyboard=True)
    markup999.add(button99)
    bot.send_message(result["player1_chat_id"], result["player1_username"] + " , готовы 👀?",
                     reply_markup=markup999)


@bot.callback_query_handler(func=lambda call: call.data == "yes")
def call_back_query_yes(call):

    # Удаление инлайн кнопок после выбора игрока
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=None)
    # Открываем соединение и получаем курсор
    c = conn.cursor()

    # Выполняем запрос на выборку данных из таблицы Gainers
    c.execute("SELECT * FROM Gainers WHERE player1_chat_id = ?", [call.message.chat.id])
    result = c.fetchone()

    # Проверяем, что result не является None
    if result:
        bot.send_sticker(result["player1_chat_id"], cool_dogs_sticker)
        bot.send_message(result["player1_chat_id"], "Обьясните ♠️ Угадайке ♠️  какая ассоциация у вас с выбранной "
                                                    "карточкой.")
        markup34 = types.InlineKeyboardMarkup()
        button3 = types.InlineKeyboardButton(text="Угадал ☑️", callback_data="true", one_time_keyboard=True)
        button4 = types.InlineKeyboardButton(text="Не угадал 🎲", callback_data="false", one_time_keyboard=True)
        markup34.add(button3, button4)

        bot.send_message(result["player1_chat_id"], result["player1_username"] + ", угадал ли ♠️ Угадайка ♠️  вашу "
                                                                                 "карточку?",
                         reply_markup=markup34)
    else:
        pass


# Обработка нажатия inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "true":
        # Удаление инлайн кнопок после выбора игрока
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        # Открываем соединение и вытаскивая из коллбэка айдичата юзера сраниваем с player1_chat_id
        c = conn.cursor()
        c.execute("SELECT * FROM Gainers WHERE player1_chat_id = ?", [call.message.chat.id])
        # Получаем заветную строку из бд
        result = c.fetchone()

        #  Проверяем, что result не является None
        if result:
            bot.send_message(result["player1_chat_id"], " ✅ Угадал ✅ ")
            bot.send_message(result["player2_chat_id"], result["player2_username"] + " , вы угадали.")

            # Проверяем, равны ли все поля нулю
            if result["turn_in_db"] is None:
                turn, gainer1.score, gainer2.score = 1, 0, 0
            else:
                turn = int(result["turn_in_db"])
                gainer1.score = int(result["gainer1_score"])
                gainer2.score = int(result["gainer2_score"])

            # Если ход нечетный, то Gainer 2 получает очко
            if turn % 2 != 0:
                gainer2.score += 1
                c.execute("UPDATE Gainers SET gainer2_score = ? WHERE player1_chat_id = ?", (gainer2.score,
                                                                                             call.message.chat.id))
            elif turn == 5:
                gainer2.score += 1
                gainer1.score -= 1
                c.execute("UPDATE Gainers SET gainer2_score = ?, gainer1_score = ? WHERE player1_chat_id = ?",
                          (gainer2.score, gainer1.score, call.message.chat.id))
            # Если ход четный, то Gainer 1 получает очко
            else:
                gainer1.score += 1
            c.execute("UPDATE Gainers SET gainer1_score  = ? WHERE player1_chat_id = ?", (gainer1.score,
                                                                                          call.message.chat.id))
            turn += 1
            c.execute("UPDATE Gainers SET turn_in_db = ? WHERE player1_chat_id = ?", (turn, call.message.chat.id))
            session_id = result["gainer2_session_id"]
            conn.commit()

            handle_continue(session_id)

    if call.data == "false":
        # Удаление инлайн кнопок после выбора игрока
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)
        # Открываем соединение и вытаскивая из коллбэка айдичата юзера сраниваем с player1_chat_id
        c = conn.cursor()
        c.execute("SELECT * FROM Gainers WHERE player1_chat_id = ?", [call.message.chat.id])
        # Получаем заветную строку из бд
        result = c.fetchone()

        #  Проверяем, что result не является None
        if result:
            bot.send_message(result["player2_chat_id"], result["player2_username"] + " , вы не угадали.")
            bot.send_message(result["player1_chat_id"], " ❌ Не угадал ❌ ")

            # Проверяем, равны ли все поля нулю
            if result["turn_in_db"] is None:
                turn, gainer1.score, gainer2.score = 1, 0, 0
            else:
                turn = int(result["turn_in_db"])
                gainer1.score = int(result["gainer1_score"])
                gainer2.score = int(result["gainer2_score"])

            if turn == 5:
                gainer2.score -= 1
                gainer1.score += 1
                c.execute("UPDATE Gainers SET gainer2_score = ?, gainer1_score = ? WHERE player1_chat_id = ?",
                          (gainer2.score, gainer1.score, call.message.chat.id))
            else:
                gainer1.score += 0
                gainer2.score += 0
                c.execute("UPDATE Gainers SET gainer1_score = ?, gainer2_score = ? WHERE player1_chat_id = ?",
                          (gainer1.score, gainer2.score, call.message.chat.id))

            turn += 1
            c.execute("UPDATE Gainers SET turn_in_db = ? WHERE player1_chat_id = ?", (turn, call.message.chat.id))

            # Выборка данных из таблицы Gainers для отправки в следующую функцию
            session_id = result["gainer2_session_id"]
            conn.commit()
            handle_continue(session_id)
        else:
            pass


def handle_continue(session_id):
    c = conn.cursor()
    c.execute("SELECT * FROM Gainers WHERE gainer2_session_id = ?", [session_id])
    result = c.fetchone()
    turn = int(result["turn_in_db"])
    gainer1.score = int(result["gainer1_score"])
    gainer2.score = int(result["gainer2_score"])

    if turn == 10:
        winner = gainer1.score > gainer2.score
        if winner:
            bot.send_message(int(result["player1_chat_id"]), "🔥🔥" + str(result["gainer1_username"]) + "🔥🔥 - Вы "
                                                                                                      "победитель")
            bot.send_sticker(int(result["player1_chat_id"]), winner_sticker)
            bot.send_message(int(result["player2_chat_id"]), "👾" + str(result["gainer2_username"]) + "👾 - Вы проиграли")
        elif gainer1.score == gainer2.score:
            bot.send_message(int(result["player1_chat_id"]), "🤔 НИЧЬЯ 🤔")
            bot.send_sticker(int(result["player1_chat_id"]), okay_sticker)
            bot.send_message(int(result["player2_chat_id"]), "🤔 НИЧЬЯ 🤔")
            bot.send_sticker(int(result["player2_chat_id"]), okay_sticker)
        else:
            bot.send_message(int(result["player2_chat_id"]), "🔥🔥" + str(result["gainer2_username"]) + "🔥🔥 - Вы "
                                                                                                      "победитель")
            bot.send_sticker(int(result["player2_chat_id"]), winner_sticker)
            bot.send_message(int(result["player1_chat_id"]), "👾" + str(result["gainer1_username"]) + "👾 - Вы проиграли")

        bot.send_sticker(int(result["player1_chat_id"]), game_over_sticker)
        bot.send_sticker(int(result["player2_chat_id"]), game_over_sticker)
        # Запрещаем повторные запросы
        c.execute("SELECT * FROM Gainers WHERE gainer2_session_id = ?", [session_id])
        result = c.fetchone()
        if int(result["turn_in_db"]) == 10:
            bot.send_message(int(result["player1_chat_id"]), "Ваши данные будут удалены. Если желаете сыграть еще раз, "
                                                             "выберите команду /start")
            bot.send_message(int(result["player2_chat_id"]), "Ваши данные будут удалены. Если желаете сыграть еще раз, "
                                                             "выберите команду /start")
            c.execute("DELETE FROM Gainers WHERE gainer2_session_id = ?", [session_id])
            conn.commit()
    else:
        bot.send_message(int(result["player1_chat_id"]), "Теперь ваша очередь отгадывать!")

        bot.send_message(int(result["player2_chat_id"]),
                         str(result["player2_username"]) + " , ваша очередь загадывать!")

        # Свап игроков местами
        c.execute("""UPDATE Gainers SET player1_player_id = ?, player1_username = ?, player1_chat_id = ?,
                player2_player_id = ?, player2_username = ?, player2_chat_id = ? WHERE gainer2_session_id = ?
        """, (int(result["player2_player_id"]), str(result["player2_username"]), int(result["player2_chat_id"]),
              int(result["player1_player_id"]),
              str(result["player1_username"]), int(result["player1_chat_id"]), session_id))
        conn.commit()
        print(result)
        handle_array_of_ids(session_id)


# Обработка любых текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text.lower() == 'dixit: начать новую игру':
        dixit_match_starter(message)
    elif message.text.lower() == '/join':
        handle_join(message)
    elif message.text.upper() in sessions:
        handle_join_session(message)
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет! Чтобы начать, нажмите /start")
    else:
        bot.send_message(message.chat.id, "Я вас не понимаю. Нажмите /start для списка команд.")


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
