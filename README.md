# ⌨️ English Typing Game Pro

A feature-rich English typing game built with **Python** and **Tkinter**.  
Test your typing speed, build combos, earn XP, and climb the levels!

---

## ✨ Features

- 🎮 **3 Game Modes**
  - ⏱️ **Timed** — 60 seconds, score as much as you can
  - ♾️ **Endless** — 3 lives, keep going until you run out
  - 💀 **Hardcore** — 1 mistake and it's game over

- 🎯 **4 Difficulty Levels**
  - 🟢 **Easy** — words with 1–3 letters
  - 🟠 **Medium** — words with 4–8 letters
  - 🔴 **Hard** — words with 9+ letters
  - 🟣 **Mix** — random selection from all levels

- 🌈 **Two Beautiful Themes**
  - **Dark** — neon glow with green accents
  - **Light** — clean and easy on the eyes

- 📊 **Detailed Statistics**
  - WPM (Words Per Minute)
  - Accuracy percentage
  - Best streak & max combo
  - Session history
  - Personal best records

- ⭐ **XP & Level System**
  - Earn XP for every correct word
  - Level up every 100 XP
  - Bonus XP for speed and combos

- 🔥 **Combo & Streak System**
  - Build combos for bonus points
  - Lose your combo when you make a mistake

- 🔊 **Sound Effects** *(Windows only)*
- 🖥️ **Fullscreen Mode**
- 🔤 **Case Toggle** — lowercase or uppercase words
- 📏 **Adjustable Font Size** — S / M / L / XL

---

## 📦 Requirements

- **Python 3.8+**
- **Tkinter** (usually included with Python)
- **Windows** *(required for sound effects — game runs fine without sound on Linux/Mac)*

No external libraries needed.

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/AmirrezaDev-BK/English-Typing-Game.git
cd English-Typing-Game

# 2. (Optional) Create a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# 3. Run the game
python KEYBOARD_GAME.py
```

---

## 🎮 How to Play

1. Launch the game with `python KEYBOARD_GAME.py`
2. Choose your settings:
   - **Mode:** Timed, Endless, or Hardcore
   - **Difficulty:** Easy, Medium, Hard, or Mix
   - **Case:** Lowercase or Uppercase
   - **Font Size:** S, M, L, or XL
3. Type the displayed word and press **Enter**
4. Build combos for bonus points
5. Beat your high score!

---

## ⌨️ Keyboard Shortcuts

| Shortcut   | Action               |
|------------|----------------------|
| `Enter`    | Submit the word      |
| `Ctrl + S` | Toggle sound         |
| `Ctrl + T` | Toggle theme         |
| `F11`      | Toggle fullscreen    |

---

## 📂 Project Structure

```
English-Typing-Game/
│
├── KEYBOARD_GAME.py    # Main game file
├── GAME.txt            # Word list
└── README.md           # Documentation
```

### Word Classification

Words from `GAME.txt` are automatically categorized by length:

| Length          | Difficulty |
|-----------------|------------|
| 1–3 characters  | 🟢 Easy    |
| 4–8 characters  | 🟠 Medium  |
| 9+ characters   | 🔴 Hard    |

If `GAME.txt` is missing, the game falls back to a built-in list of 34 default words.

---

## 🛠️ Built With

- **Python 3** — Core language
- **Tkinter** — GUI framework
- **winsound** — Sound effects (Windows only)
- **math**, **random**, **time**, **os** — Standard library

---

## 🗺️ Roadmap

- [ ] Cross-platform sound support
- [ ] Save statistics to file (JSON/SQLite)
- [ ] Custom word lists
- [ ] Achievement system
- [ ] Additional themes
- [ ] Multiplayer mode

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the project, open issues, or submit pull requests.

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some AmazingFeature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Amirreza Baqery Kahkesh**

- GitHub: [@AmirrezaDev-BK](https://github.com/AmirrezaDev-BK)
- Repository: [English-Typing-Game](https://github.com/AmirrezaDev-BK/English-Typing-Game)

---

## ⭐ Show Your Support

If you enjoy this project, please give it a ⭐ on GitHub — it really helps!

---

<div align="center">

**Made with ❤️ and Python**

</div>
