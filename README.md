**🎮 Word Shutter Typing Game**

A fast-paced, interactive typing game built with Python and Pygame where words fall from the top of the screen, and players must type them accurately before they reach the bottom. The game tests typing speed, accuracy, and reflexes — all while tracking combos and high scores.

**🧠 Problem Statement**

Create an engaging terminal-based or GUI-based game where:
Words fall from the top of the screen.
Players must type them correctly before they hit the bottom.
Scoring is based on speed, accuracy, and combo streaks.

**🛠️ Tech Stack**

Language: Python 3.9+
Library: pygame, random, time, json
Platform: Windows 10/11
Data Storage: JSON file (for persistent high scores)

**🧩 Features**

📉 Dynamic Word Falling Speed

Speed increases with level and word length

🏆 Scoring System

Base: 10 points

Bonus: 2 points per letter

Combo Bonus: Extra points after 3+ streaks

🎯 Combo Mechanic

Increases points for consecutive correct typings

🕹️ Game Over Condition

If any word reaches the bottom without being typed

📊 Compact Info Display

Live updates for score, level, combo, words typed, and time

🎨 Color-Coded Words

Short words: Mint

Medium: Sky Blue

Long: Coral

⏸️ Pause/Resume Functionality

ESC pauses or resumes the game, and pauses the timer

🧠 High Score Tracking

Saves highest score, most words typed, and best time

💾 Data Persistence (High Scores)

Stored in highscores.json:

**⌨️ Controls**

Key	Action


Keyboard	Type the falling word

ENTER	Submit typed word

ESC	Pause/Resume the game

BACKSPACE	Delete current input

**✅ Sample Gameplay Flow**

Words fall from the top of the screen.

The player types "python" and hits ENTER.

Word disappears with an explosion effect.

Score increases by 10 + (2 × word length) = 22.

Combo counter increases.

If the player types 3+ words correctly, bonus points apply.
