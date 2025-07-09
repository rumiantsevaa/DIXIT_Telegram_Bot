import sqlite3
from config import sqlite_file

# Создание базы данных
conn = sqlite3.connect(sqlite_file, check_same_thread=False)
c = conn.cursor()

# Очистка таблиц
# c.execute('''DROP TABLE IF EXISTS Gainers''')
# c.execute('''DROP TABLE IF EXISTS GamesHistory''')
# conn.commit()

# Создание основной таблицы Gainers
c.execute('''
CREATE TABLE IF NOT EXISTS Gainers (
    gainer1_player_id INTEGER, gainer1_username TEXT, gainer1_score INTEGER, gainer1_session_id TEXT,
    gainer2_player_id INTEGER, gainer2_username TEXT, gainer2_score INTEGER, gainer2_session_id TEXT,
    turn_in_db INTEGER,
    player1_player_id INTEGER, player1_username TEXT, player1_chat_id INTEGER,
    player2_player_id INTEGER, player2_username TEXT, player2_chat_id INTEGER
)
''')

# Создание таблицы истории игр
c.execute('''
CREATE TABLE IF NOT EXISTS GamesHistory (
    gainer1_player_id INTEGER,
    gainer2_player_id INTEGER,
    game_end_time TEXT
)
''')
conn.commit()
