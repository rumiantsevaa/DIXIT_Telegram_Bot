# Создаем класс для хранения данных о игроках  вне свапов (Для корректного засчитывания очков и определения победы)
class Gainer:
    def __init__(self, player_id: int, username: str, score: int, session_id: str):
        self.player_id = player_id
        self.username = username
        self.score = score
        self.session_id = session_id


# Создание экземпляров класса Gainer
gainer1 = Gainer(player_id=0, username="", score=0, session_id="")
gainer2 = Gainer(player_id=0, username="", score=0, session_id="")


# Создаем класс для хранения данных о игроках(значения будут свапаться)
class Player:
    def __init__(self, player_id: int, username: str, chat_id: int):
        self.player_id = player_id
        self.username = username
        self.chat_id = chat_id


# Создание экземпляров класса Player
player1 = Player(player_id=0, username="", chat_id=0)
player2 = Player(player_id=0, username="", chat_id=0)
