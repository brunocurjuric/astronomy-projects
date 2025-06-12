# Constellations Quizzes

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)](https://www.python.org/)

## 📘 Overview

The constellations quizzes help you learn the names of stars and their corresponding constellations across different regions of the night sky, north (declinations of 40° and above), equator (declinations from -40° to 40°) and south (declinations of -40° and below). They feature multiple difficulty levels, primarily based on stellar brightness. There are different modes:

- **Single Player** (`constellations_quiz_SP.py`) – Practice identifying stars and constellations on your own. Highscores available.
- **Multiplayer** (`constellations_quiz_MP.py`) – Compete with friends in local hot-seat mode.
- **Arcade Mode** (`constellations_quiz_ARC.py`) – Begin on easy mode and progress through increasing difficulties all the way to veteran level.
- **Gauntlet Mode** (`constellations_quiz_G.py`) – Five levels of play with one question from each difficulty. Highscores available.


## 🔮 Upcoming features

Future updates will include new modes and enhancements:

- **Survival Mode** – Test how long you can last as the challenge increases.
- **Tournament Mode** – Compete in structured rounds against other players, with increasing difficulty each round.
- **Arcade Mode Enhancements** - High scores
  and multiplayer support.
- **Combined Difficulties** – Mix different difficulty levels in one session.




## 🛠️ How to Play

Open your terminal and use the following commands:

### 👤 Single Player Mode
```bash
python3 constellations_quiz_SP.py
```
To see the highscores, type:
```bash
python3 constellations_quiz_SP.py -score difficulty region
```
where difficulty can be E (easy), M (medium), H (hard), V (veteran) or A (all difficulties), and region N (north), E (equator), S (south), NE (north and equator), SE (south and equator) or A (the whole sky).

### 👥 Multiplayer Mode
```bash
python3 constellations_quiz_MP.py
```

### 🕹️ Arcade Mode
```bash
python3 constellations_quiz_ARC.py
```

### 🎮 Gauntlet Mode
```bash
python3 constellations_quiz_G.py
```
