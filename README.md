# DIXIT: 9 lives mod Telegram Bot

![image](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/0755f21d-9b9b-483b-a7a1-d01c7ddf4ee3)

### Overview

[@DixitRBot](https://t.me/DixitRBot) is a Telegram bot designed for playing **DIXIT: 9 Lives Mod** — a two-player adaptation of the popular board game **DIXIT**, focused on deep associative gameplay and turn-based storytelling.


![winner-png-2](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/e7b0a204-54c4-49b4-b209-065f7634aad2)

---

### 🔧 Updates (July 2025)

#### 🚀 Hosting Migration
- Deployed to [PythonAnywhere](https://www.pythonanywhere.com/) for **24/7 availability**
- Added `pythonanywhere_starter.py` for seamless deployment on the platform

#### ⏱️ Match Limitations
- Implemented a **1 match per day per user** policy (for completed games only)
- Added `can_start_new_game(user_id)` logic to **enforce daily limits**
- Automatically **removes unfinished sessions** before starting or joining a new game
- All handlers (`/dixit_match_starter`, `handle_join_session`) updated accordingly

#### 🐛 Bug Fixes
- Fixed a critical issue where cards could **repeat in a single round**
  > Replaced `random.choice` with `random.sample` to ensure card uniqueness

#### 📁 New & Refactored Files
- `requirements.txt` — for quick setup with all dependencies
- `pythonanywhere_starter.py` — simple entry point for hosted environments
- Database schema updated to store game history and track last game time

---

### 🎮 Game Description

The game is designed for **two players** and consists of **nine rounds**. Players take turns assuming the roles of:

- ♦️ **Mysterious Narrator** — selects one card and gives an associative clue  
- ♠️ **Guesser** — tries to pick the correct card based on the clue

Points are scored based on successful guesses, and the player with the most points after 9 rounds wins.

![Снимок экрана (11)](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/a5264391-e32e-4c96-b227-a15c0ae9acd4)

---

### 💡 Features

- Fully interactive two-player card game experience in Telegram
- Persistent game state with SQLite3
- Game roles automatically assigned and swapped
- Built-in image card system with randomized delivery
- Round-based logic and scoring
- Unique stickers, buttons, and UI feedback
- **1 game per user per day** enforcement
- Automatic cleanup of abandoned sessions
- Hosted 24/7 on PythonAnywhere

---

### 🚀 Getting Started

![310162415-eaaa990f-0eb0-4798-b219-67cf7c558fe7](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/48591bc0-ec63-43de-8abb-a51bc0119e42)

1. Click the button **"💫 DIXIT: Start a new game 💫"**
2. Follow the instructions sent by the bot
3. Invite your partner to join using the `/join` command
4. The game will begin once both players are connected to the same session

![photo_2024-03-29_14-57-01](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/8a1dedf0-2c4b-497f-bf9f-71191ba41470)

---

### 📜 Game Rules

- **Roles:** Players alternate between ♦️ Mysterious Narrator and ♠️ Guesser
- **Clues:** Narrators give associative clues based on their selected card
- **Guessing:** The Guesser selects the card they believe matches the clue
- **Scoring:** Points are awarded for correct guesses; special rules apply on turn 5
- **Victory:** The player with the highest total score after 9 rounds wins

---

### 🕹️ How to Play

* Start a new game with the `/start` command  
* Use `/join` to invite your partner to join the same session  
* Wait for both players to receive card sets  
* Use intuitive buttons to mark the guesses and swap roles each round

![image](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/326b20cf-18d8-49f0-9fab-621004acdd4b)

* After 9 turns, the bot automatically announces the winner

![photo_2024-03-29_15-10-36](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/db8775d1-23a4-4c3f-b0ed-479859ab4aed)

---

### 📖 Commands

- `/start` — launches the game and displays the Start button  
- `/join` — allows the second player to connect to an existing session  
- `/help` — shows game rules and usage instructions

---


### 📂 Deployment

To run the bot yourself:

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Create the SQLite database (see `DIXIT_db.py` or `db.py` if applicable)

3. Set your API token in `config.py`

4. Launch the bot:

    ```bash
    python main.py
    ```

### 🔒 Privacy Notice

This is a non-commercial project that:

- Doesn't collect or store personal data
- Doesn't retain any messages, photos, or gameplay history after the game ends
- Stores minimal session data temporarily for gameplay purposes only
- Uses official Telegram Bot API and adheres to its privacy practices
