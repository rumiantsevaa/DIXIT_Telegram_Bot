# DIXIT: 9 lives mod Telegram Bot

![image](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/0755f21d-9b9b-483b-a7a1-d01c7ddf4ee3)



### Overview

@DixitRBot is a Telegram bot designed for playing DIXIT: 9 lives mod for two players online. This Telegram bot built on Telebot and allows users to play a modified version of the popular card game DIXIT. 

![winner-png-2](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/e7b0a204-54c4-49b4-b209-065f7634aad2)


The game is designed for two players and consists of nine rounds. Players take turns being the "Mysterious Narrator" and the "Guesser." The goal is to accumulate the highest score by successfully conveying and guessing the chosen card through associative clues.

![Снимок экрана (11)](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/a5264391-e32e-4c96-b227-a15c0ae9acd4)

### Features

_Getting Started_


![310162415-eaaa990f-0eb0-4798-b219-67cf7c558fe7](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/48591bc0-ec63-43de-8abb-a51bc0119e42)


To start a new game, click the "💫 DIXIT: Start a new game 💫" button. Follow the on-screen instructions and invite your partner to join using the "/join" command.

![photo_2024-03-29_14-57-01](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/8a1dedf0-2c4b-497f-bf9f-71191ba41470)


_Game Rules_

* Roles: The game has two roles - "Mysterious Narrator" (♦️) and "Guesser" (♠️). Players switch roles during the game.

* Turns: The Mysterious Narrator selects a card and provides clues without directly pointing to it. The Guesser must associate the clues with the correct card.

* Scoring: Points are awarded for successful guesses. Special rules apply for the 5th turn.

* Objective: The winner is determined by the total number of points accumulated.

### How to Play

* Start a new game with the "/start" command.
* Use "/join" to invite your partner to join the game.
* Follow the instructions to choose cards and provide clues.

![image](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/326b20cf-18d8-49f0-9fab-621004acdd4b)

* Use built-in buttons to confirm guesses and continue the game.

![photo_2024-03-29_15-09-55](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/073a549a-84ca-4fc1-87a2-4d044b7b2f2a)

  
* The game ends after nine rounds, and the winner is announced.

![photo_2024-03-29_15-10-36](https://github.com/rumiantsevaa/DIXIT_Telegram_Bot/assets/89034072/db8775d1-23a4-4c3f-b0ed-479859ab4aed)


### Commands

_/help:_ Displays detailed information about the game and its rules.
_/start:_ Initiates the game and provides a button to start a new game.
_/join:_ Allows the second player to join the game.

### Note:

The implementation of gaming sessions is done, all your data stored in database to prevent session interruption only until the game is over. Moreover, anti-abuse system is enabled, so the buttons and functions will be available only if intended.
For restarting the bot, use the command /start.
For any assistance or to explore more commands, use the command /help.
