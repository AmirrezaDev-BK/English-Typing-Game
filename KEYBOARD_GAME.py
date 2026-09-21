import math
import os
import random
import time
import tkinter as tk
import winsound
from datetime import datetime
from tkinter import messagebox, ttk

# ============================================================
# FILE PATHS
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORD_FILE = os.path.join(SCRIPT_DIR, "GAME.txt")

# ============================================================
# THEMES
# ============================================================


class ThemeManager:
    def __init__(self):
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "bg": "#0a0a0a",
                "fg": "#ffffff",
                "word_bg": "#1a1a2e",
                "word_fg": "#00ff88",
                "input_bg": "#1a1a2e",
                "input_fg": "#00ff88",
                "stats_bg": "#1a1a2e",
                "stats_fg": "#00ff88",
                "btn_bg": "#00ff88",
                "btn_fg": "#0a0a0a",
                "title_color": "#00ff88",
                "combo_color": "#ff6b35",
                "streak_color": "#ffd700",
                "correct": "#00ff88",
                "wrong": "#ff4444",
                "msg_bg": "#0a0a0a",
                "last_bg": "#1a1a2e",
                "last_fg": "#aaaaaa",
                "neon_glow": "#00ff88",
                "xp_color": "#9b59b6",
                "level_color": "#f39c12",
                "mix_color": "#9b59b6",
                "easy_color": "#00ff88",
                "medium_color": "#ffd700",
                "hard_color": "#ff4444",
            },
            "light": {
                "bg": "#f0f0f0",
                "fg": "#1a1a2e",
                "word_bg": "#ffffff",
                "word_fg": "#0066cc",
                "input_bg": "#ffffff",
                "input_fg": "#1a1a2e",
                "stats_bg": "#e8e8e8",
                "stats_fg": "#1a1a2e",
                "btn_bg": "#0066cc",
                "btn_fg": "#ffffff",
                "title_color": "#0066cc",
                "combo_color": "#d35400",
                "streak_color": "#f39c12",
                "correct": "#27ae60",
                "wrong": "#c0392b",
                "msg_bg": "#f0f0f0",
                "last_bg": "#e8e8e8",
                "last_fg": "#333333",
                "neon_glow": "#0066cc",
                "xp_color": "#8e44ad",
                "level_color": "#e67e22",
                "mix_color": "#8e44ad",
                "easy_color": "#27ae60",
                "medium_color": "#f39c12",
                "hard_color": "#c0392b",
            },
        }

    def get(self, key):
        return self.themes[self.current_theme].get(key, "#ffffff")

    def toggle(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        return self.current_theme

    def is_dark(self):
        return self.current_theme == "dark"


# ============================================================
# DIFFICULTY COLORS
# ============================================================

DIFFICULTY_COLORS = {
    "easy": "#00ff88",
    "medium": "#ffd700",
    "hard": "#ff4444",
    "mix": "#9b59b6",
}

DIFFICULTY_LABELS = {
    "easy": "🟢 Easy",
    "medium": "🟠 Medium",
    "hard": "🔴 Hard",
    "mix": "🟣 Mix",
}

WORD_LEVEL_EMOJIS = {"easy": "🟢", "medium": "🟠", "hard": "🔴"}

# ============================================================
# WORD MANAGER
# ============================================================


class WordManager:
    def __init__(self):
        self.easy_words = []
        self.medium_words = []
        self.hard_words = []
        self.load_words()

    def load_words(self):
        try:
            with open(WORD_FILE, "r", encoding="utf-8") as f:
                all_words = [line.strip() for line in f if line.strip()]

            for word in all_words:
                length = len(word)
                if length <= 3:
                    self.easy_words.append(word)
                elif length <= 8:
                    self.medium_words.append(word)
                else:
                    self.hard_words.append(word)

            print(
                f"✅ Loaded: Easy={len(self.easy_words)}, Medium={len(self.medium_words)}, Hard={len(self.hard_words)}"
            )

        except FileNotFoundError:
            print("❌ GAME.txt not found! Using default words.")
            self.use_default_words()

    def use_default_words(self):
        default = [
            "a",
            "an",
            "at",
            "be",
            "by",
            "do",
            "go",
            "he",
            "if",
            "in",
            "is",
            "it",
            "me",
            "my",
            "no",
            "of",
            "on",
            "or",
            "so",
            "to",
            "cat",
            "dog",
            "run",
            "big",
            "red",
            "blue",
            "code",
            "game",
            "key",
            "type",
            "word",
            "python",
            "computer",
            "keyboard",
        ]

        for word in default:
            length = len(word)
            if length <= 3:
                self.easy_words.append(word)
            elif length <= 8:
                self.medium_words.append(word)
            else:
                self.hard_words.append(word)

    def get_random_word(self, difficulty="medium"):
        if difficulty == "mix":
            levels = ["easy", "medium", "hard"]
            selected_level = random.choice(levels)
            if selected_level == "easy":
                words = self.easy_words
            elif selected_level == "hard":
                words = self.hard_words
            else:
                words = self.medium_words

            if not words:
                return "hello", "easy"
            return random.choice(words), selected_level

        elif difficulty == "easy":
            words = self.easy_words
        elif difficulty == "hard":
            words = self.hard_words
        else:
            words = self.medium_words

        if not words:
            return "hello", "medium"
        return random.choice(words), difficulty

    def get_word_level(self, word):
        length = len(word)
        if length <= 3:
            return "easy"
        elif length <= 8:
            return "medium"
        else:
            return "hard"


# ============================================================
# MAIN GAME (بدون ذخیره تاریخچه در فایل)
# ============================================================


class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("⌨️ Typing Game Pro")
        self.root.geometry("950x850")
        self.root.resizable(True, True)

        self.word_manager = WordManager()
        self.theme = ThemeManager()

        self.sound_enabled = True

        self.current_word = ""
        self.current_word_level = "medium"
        self.score = 0
        self.total = 0
        self.correct = 0
        self.words_typed = 0
        self.time_left = 60
        self.game_duration = 60
        self.is_running = False
        self.difficulty = "medium"
        self.mode = "timed"
        self.case_mode = "lowercase"
        self.start_time = 0
        self.word_start = 0
        self.last_words = []

        self.combo = 0
        self.max_combo = 0
        self.streak = 0
        self.best_streak = 0
        self.errors = 0
        self.max_errors = 3

        # XP (فقط در حافظه)
        self.xp = 0
        self.level = 1
        self.xp_earned = 0

        # تاریخچه (فقط در حافظه)
        self.session_history = []
        self.daily_stats = {"words": 0, "score": 0, "wpm": 0, "accuracy": 0}
        self.best_stats = {"wpm": 0, "score": 0, "streak": 0, "combo": 0}

        self.font_size = 50
        self.is_fullscreen = False
        self.animation_phase = 0
        self.animation_running = False

        self.mode_radios = []
        self.diff_radios = []
        self.font_radios = []
        self.case_radios = []

        self.setup_ui()
        self.apply_theme()
        self.update_stats_display()
        self.start_game()

        self.root.bind("<Control-s>", lambda e: self.toggle_sound())
        self.root.bind("<Control-t>", lambda e: self.toggle_theme())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ===== TOP FRAME =====
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(pady=5, fill="x")

        self.title_label = tk.Label(
            self.top_frame, text="⌨️ TYPING GAME PRO", font=("Arial", 26, "bold")
        )
        self.title_label.pack(pady=3)

        btn_frame = tk.Frame(self.top_frame)
        btn_frame.pack(pady=3)

        self.sound_btn = tk.Button(
            btn_frame,
            text="🔊 Sound",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=3,
            command=self.toggle_sound,
            cursor="hand2",
        )
        self.sound_btn.pack(side="left", padx=5)

        self.theme_btn = tk.Button(
            btn_frame,
            text="🌙 Dark",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=3,
            command=self.toggle_theme,
            cursor="hand2",
        )
        self.theme_btn.pack(side="left", padx=5)

        self.fullscreen_btn = tk.Button(
            btn_frame,
            text="⛶ Fullscreen",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=3,
            command=self.toggle_fullscreen,
            cursor="hand2",
        )
        self.fullscreen_btn.pack(side="left", padx=5)

        # ===== GAME FRAME =====
        self.game_frame = tk.Frame(self.main_frame)
        self.game_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Info bar
        self.info_frame = tk.Frame(self.game_frame)
        self.info_frame.pack(pady=5)

        self.time_label = tk.Label(
            self.info_frame, text="⏱️ 60s", font=("Arial", 13, "bold"), width=9
        )
        self.time_label.pack(side="left", padx=4)

        self.score_label = tk.Label(
            self.info_frame, text="🎯 0", font=("Arial", 13, "bold"), width=9
        )
        self.score_label.pack(side="left", padx=4)

        self.wpm_label = tk.Label(
            self.info_frame, text="⚡ 0 WPM", font=("Arial", 13, "bold"), width=10
        )
        self.wpm_label.pack(side="left", padx=4)

        self.acc_label = tk.Label(
            self.info_frame, text="✅ 0%", font=("Arial", 13, "bold"), width=9
        )
        self.acc_label.pack(side="left", padx=4)

        self.combo_label = tk.Label(
            self.info_frame, text="🔥 0x", font=("Arial", 13, "bold"), width=7
        )
        self.combo_label.pack(side="left", padx=4)

        self.streak_label = tk.Label(
            self.info_frame, text="⭐ 0", font=("Arial", 13, "bold"), width=7
        )
        self.streak_label.pack(side="left", padx=4)

        self.progress_label = tk.Label(
            self.info_frame, text="", font=("Arial", 11), width=12
        )
        self.progress_label.pack(side="left", padx=4)

        # XP Level
        xp_frame = tk.Frame(self.info_frame, bg=self.theme.get("bg"))
        xp_frame.pack(side="left", padx=10)

        self.level_label = tk.Label(
            xp_frame,
            text=f"⭐ Level {self.level}",
            font=("Arial", 11, "bold"),
            fg=self.theme.get("level_color"),
        )
        self.level_label.pack(side="left", padx=5)

        self.xp_label = tk.Label(
            xp_frame,
            text=f"⚡ {self.xp} XP",
            font=("Arial", 11, "bold"),
            fg=self.theme.get("xp_color"),
        )
        self.xp_label.pack(side="left", padx=5)

        # Word display with level indicator
        word_container = tk.Frame(self.game_frame)
        word_container.pack(pady=5)

        self.level_indicator = tk.Label(
            word_container, text="🟢", font=("Arial", 20), fg="#00ff88"
        )
        self.level_indicator.pack(side="left", padx=5)

        self.word_frame = tk.Frame(word_container, relief="ridge", bd=3)
        self.word_frame.pack(side="left", padx=5)

        self.word_display = tk.Label(
            self.word_frame, text="Start", font=("Arial", self.font_size, "bold")
        )
        self.word_display.pack(pady=15)

        # Input
        self.input_entry = tk.Entry(
            self.game_frame, font=("Arial", 18), width=30, justify="center"
        )
        self.input_entry.pack(pady=8)
        self.input_entry.bind("<Return>", self.check_word)
        self.input_entry.bind("<Key>", self.on_key_press)

        # Settings
        settings_frame = tk.Frame(self.game_frame)
        settings_frame.pack(pady=5)

        # Mode
        mode_frame = tk.Frame(settings_frame)
        mode_frame.pack(side="left", padx=10)

        tk.Label(mode_frame, text="Mode:", font=("Arial", 10, "bold")).pack(side="left")
        self.mode_var = tk.StringVar(value="timed")
        modes = [("Timed", "timed"), ("Endless", "endless"), ("Hardcore", "hardcore")]

        for text, value in modes:
            rb = tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                font=("Arial", 9),
                selectcolor="#0f3460",
                command=self.change_mode,
            )
            rb.pack(side="left", padx=5)
            self.mode_radios.append(rb)

        # Difficulty
        diff_frame = tk.Frame(settings_frame)
        diff_frame.pack(side="left", padx=10)

        tk.Label(diff_frame, text="Difficulty:", font=("Arial", 10, "bold")).pack(
            side="left"
        )
        self.diff_var = tk.StringVar(value="medium")
        difficulties = [
            ("Easy", "easy"),
            ("Medium", "medium"),
            ("Hard", "hard"),
            ("Mix", "mix"),
        ]

        for text, value in difficulties:
            rb = tk.Radiobutton(
                diff_frame,
                text=text,
                variable=self.diff_var,
                value=value,
                font=("Arial", 9),
                selectcolor="#0f3460",
                command=self.change_difficulty,
            )
            rb.pack(side="left", padx=5)
            self.diff_radios.append(rb)

        # Case
        case_frame = tk.Frame(settings_frame)
        case_frame.pack(side="left", padx=10)

        tk.Label(case_frame, text="Case:", font=("Arial", 10, "bold")).pack(side="left")
        self.case_var = tk.StringVar(value="lowercase")
        cases = [("Lowercase", "lowercase"), ("Uppercase", "uppercase")]

        for text, value in cases:
            rb = tk.Radiobutton(
                case_frame,
                text=text,
                variable=self.case_var,
                value=value,
                font=("Arial", 9),
                selectcolor="#0f3460",
                command=self.change_case,
            )
            rb.pack(side="left", padx=5)
            self.case_radios.append(rb)

        # Font size
        font_frame = tk.Frame(settings_frame)
        font_frame.pack(side="left", padx=10)

        tk.Label(font_frame, text="Font:", font=("Arial", 10, "bold")).pack(side="left")
        font_sizes = [("S", 30), ("M", 50), ("L", 70), ("XL", 90)]

        for text, value in font_sizes:
            rb = tk.Radiobutton(
                font_frame,
                text=text,
                font=("Arial", 9),
                command=lambda v=value: self.change_font_size(v),
            )
            rb.pack(side="left", padx=3)
            self.font_radios.append(rb)

        # Buttons
        btn_frame2 = tk.Frame(self.game_frame)
        btn_frame2.pack(pady=8)

        self.start_btn = tk.Button(
            btn_frame2,
            text="▶️ New Game",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5,
            command=self.start_game,
            cursor="hand2",
        )
        self.start_btn.pack(side="left", padx=5)

        self.pause_btn = tk.Button(
            btn_frame2,
            text="⏸️ Pause",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5,
            command=self.toggle_pause,
            state="disabled",
            cursor="hand2",
        )
        self.pause_btn.pack(side="left", padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.game_frame, length=400, mode="determinate")
        self.progress.pack(pady=5)

        # Message
        self.msg_label = tk.Label(self.game_frame, text="", font=("Arial", 12))
        self.msg_label.pack(pady=3)

        # Last words
        self.last_frame = tk.Frame(self.game_frame, relief="ridge", bd=2)
        self.last_frame.pack(pady=8, padx=20, fill="x")

        self.last_title = tk.Label(
            self.last_frame, text="📝 Last Words:", font=("Arial", 10, "bold")
        )
        self.last_title.pack(pady=2)

        self.last_text = tk.Text(
            self.last_frame, height=2, width=40, font=("Arial", 9), relief="flat"
        )
        self.last_text.pack(padx=10, pady=3)

        # ===== HISTORY FRAME (در حافظه) =====
        self.history_frame = tk.Frame(self.main_frame, width=320, relief="ridge", bd=2)
        self.history_frame.pack(side="right", fill="y", padx=(0, 5))
        self.history_frame.pack_propagate(False)

        tk.Label(
            self.history_frame, text="📊 SESSION STATS", font=("Arial", 14, "bold")
        ).pack(pady=5)

        # Daily stats
        daily_frame = tk.Frame(self.history_frame)
        daily_frame.pack(pady=3, fill="x")

        tk.Label(daily_frame, text="📅 This Session:", font=("Arial", 10, "bold")).pack(
            anchor="w", padx=10
        )

        self.daily_text = tk.Text(
            daily_frame, height=3, width=30, font=("Arial", 9), relief="flat"
        )
        self.daily_text.pack(padx=10, pady=2)

        # Best stats
        best_frame = tk.Frame(self.history_frame)
        best_frame.pack(pady=3, fill="x")

        tk.Label(best_frame, text="🏆 Best Records:", font=("Arial", 10, "bold")).pack(
            anchor="w", padx=10
        )

        self.best_text = tk.Text(
            best_frame, height=3, width=30, font=("Arial", 9), relief="flat"
        )
        self.best_text.pack(padx=10, pady=2)

        # Session history
        tk.Label(
            self.history_frame, text="📋 Games Played:", font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=10)

        self.history_text = tk.Text(
            self.history_frame, height=6, width=30, font=("Arial", 8), relief="flat"
        )
        self.history_text.pack(padx=10, pady=3)

        tk.Label(
            self.history_frame,
            text="⌨️ Ctrl+S (Sound) | Ctrl+T (Theme) | F11 (Fullscreen)",
            font=("Arial", 7),
            fg="#666",
        ).pack(pady=3)

        # Clear history button
        clear_btn = tk.Button(
            self.history_frame,
            text="🗑️ Clear History",
            font=("Arial", 8),
            bg="#e74c3c",
            fg="white",
            padx=10,
            pady=2,
            command=self.clear_history,
        )
        clear_btn.pack(pady=3)

    def clear_history(self):
        """پاک کردن تاریخچه در حافظه"""
        self.session_history = []
        self.best_stats = {"wpm": 0, "score": 0, "streak": 0, "combo": 0}
        self.daily_stats = {"words": 0, "score": 0, "wpm": 0, "accuracy": 0}
        self.xp = 0
        self.level = 1
        self.update_stats_display()
        self.update_xp_display()
        self.msg_label.config(text="🗑️ History cleared!", fg="#3498db")

    def apply_theme(self):
        theme = self.theme.themes[self.theme.current_theme]

        self.root.configure(bg=theme["bg"])
        self.main_frame.configure(bg=theme["bg"])
        self.top_frame.configure(bg=theme["bg"])
        self.game_frame.configure(bg=theme["bg"])
        self.history_frame.configure(bg=theme["stats_bg"])

        self.title_label.configure(fg=theme["title_color"], bg=theme["bg"])

        self.sound_btn.configure(
            bg="#2ecc71" if self.sound_enabled else "#e74c3c", fg="white"
        )
        self.theme_btn.configure(bg="#9b59b6", fg="white")
        self.fullscreen_btn.configure(bg="#3498db", fg="white")

        self.info_frame.configure(bg=theme["bg"])
        self.time_label.configure(fg=theme["fg"], bg=theme["bg"])
        self.score_label.configure(fg=theme["fg"], bg=theme["bg"])
        self.wpm_label.configure(fg=theme["fg"], bg=theme["bg"])
        self.acc_label.configure(fg=theme["fg"], bg=theme["bg"])
        self.combo_label.configure(fg=theme["combo_color"], bg=theme["bg"])
        self.streak_label.configure(fg=theme["streak_color"], bg=theme["bg"])
        self.progress_label.configure(fg=theme["fg"], bg=theme["bg"])

        self.level_label.configure(bg=theme["bg"], fg=theme["level_color"])
        self.xp_label.configure(bg=theme["bg"], fg=theme["xp_color"])

        self.word_frame.configure(bg=theme["word_bg"])
        if self.difficulty == "mix":
            if (
                hasattr(self, "current_word_level")
                and self.current_word_level in DIFFICULTY_COLORS
            ):
                self.word_display.configure(
                    bg=theme["word_bg"], fg=DIFFICULTY_COLORS[self.current_word_level]
                )
            else:
                self.word_display.configure(bg=theme["word_bg"], fg=theme["mix_color"])
        else:
            self.word_display.configure(
                bg=theme["word_bg"], fg=DIFFICULTY_COLORS[self.difficulty]
            )

        self.level_indicator.configure(bg=theme["word_bg"])
        self.level_indicator.pack(side="left", padx=5)

        self.input_entry.configure(bg=theme["input_bg"], fg=theme["input_fg"])

        for rb in self.mode_radios:
            rb.configure(bg=theme["bg"], fg=theme["fg"])
        for rb in self.diff_radios:
            rb.configure(bg=theme["bg"], fg=theme["fg"])
        for rb in self.case_radios:
            rb.configure(bg=theme["bg"], fg=theme["fg"])
        for rb in self.font_radios:
            rb.configure(bg=theme["bg"], fg=theme["fg"])

        self.start_btn.configure(
            bg="#00ff88" if self.theme.is_dark() else "#0066cc",
            fg="#0a0a0a" if self.theme.is_dark() else "white",
        )
        self.pause_btn.configure(bg="#f39c12", fg="white")

        self.msg_label.configure(bg=theme["bg"])

        self.last_frame.configure(bg=theme["stats_bg"])
        self.last_title.configure(fg=theme["stats_fg"], bg=theme["stats_bg"])
        self.last_text.configure(bg=theme["last_bg"], fg=theme["last_fg"])

        for child in self.history_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=theme["stats_bg"], fg=theme["stats_fg"])
            elif isinstance(child, tk.Frame):
                child.configure(bg=theme["stats_bg"])
                for sub in child.winfo_children():
                    if isinstance(sub, tk.Label):
                        sub.configure(bg=theme["stats_bg"], fg=theme["stats_fg"])
                    elif isinstance(sub, tk.Text):
                        sub.configure(bg=theme["last_bg"], fg=theme["last_fg"])
            elif isinstance(child, tk.Button):
                child.configure(bg="#e74c3c", fg="white")

        self.daily_text.configure(bg=theme["last_bg"], fg=theme["last_fg"])
        self.best_text.configure(bg=theme["last_bg"], fg=theme["last_fg"])
        self.history_text.configure(bg=theme["last_bg"], fg=theme["last_fg"])

        self.theme_btn.configure(text="☀️ Light" if self.theme.is_dark() else "🌙 Dark")

    def change_difficulty(self):
        self.difficulty = self.diff_var.get()
        if self.difficulty == "mix":
            self.word_display.config(fg=self.theme.get("mix_color"))
        else:
            self.word_display.config(fg=DIFFICULTY_COLORS[self.difficulty])

        self.msg_label.config(
            text=f"🎯 Difficulty: {DIFFICULTY_LABELS[self.difficulty]}",
            fg=self.theme.get("correct"),
        )

    def change_mode(self):
        self.mode = self.mode_var.get()
        if self.mode == "hardcore":
            self.max_errors = 1
            self.msg_label.config(
                text="💀 Hardcore Mode! Only 1 mistake!", fg="#ff4444"
            )
        elif self.mode == "endless":
            self.max_errors = 3
            self.msg_label.config(text="♾️ Endless Mode! 3 lives!", fg="#3498db")
        else:
            self.max_errors = 999
            self.msg_label.config(text="⏱️ Timed Mode!", fg="#2ecc71")
        self.update_progress_display()

    def change_case(self):
        self.case_mode = self.case_var.get()
        self.msg_label.config(
            text=f"🔤 Case: {self.case_mode.title()}", fg=self.theme.get("correct")
        )
        if self.is_running and self.current_word:
            self.update_word_display(self.current_word, self.current_word_level)

    def get_word_color(self, level):
        colors = {"easy": "#00ff88", "medium": "#ffd700", "hard": "#ff4444"}
        return colors.get(level, "#ffffff")

    def get_word_emoji(self, level):
        emojis = {"easy": "🟢", "medium": "🟠", "hard": "🔴"}
        return emojis.get(level, "🟣")

    def convert_case(self, word):
        if self.case_mode == "uppercase":
            return word.upper()
        else:
            return word.lower()

    def update_word_display(self, word, level):
        self.current_word = word
        self.current_word_level = level

        display_word = self.convert_case(word)

        if self.difficulty == "mix":
            color = self.get_word_color(level)
            self.word_display.config(text=display_word, fg=color)
            self.level_indicator.config(text=self.get_word_emoji(level))
        else:
            self.word_display.config(
                text=display_word, fg=DIFFICULTY_COLORS[self.difficulty]
            )
            self.level_indicator.config(text="")

    def update_xp_display(self):
        self.level_label.config(text=f"⭐ Level {self.level}")
        self.xp_label.config(text=f"⚡ {self.xp} XP")

    def add_xp(self, amount):
        self.xp += amount
        new_level = 1 + (self.xp // 100)
        if new_level > self.level:
            self.level = new_level
            self.msg_label.config(
                text=f"🎉 LEVEL UP! Level {self.level}!", fg="#f1c40f"
            )
            self.play_sound(800, 200)
            self.play_sound(1000, 200)
        self.level = new_level
        self.update_xp_display()

    def next_word(self):
        if self.mode == "endless" and self.errors >= self.max_errors:
            self.game_over()
            return

        if self.mode == "hardcore" and self.errors >= 1:
            self.game_over()
            return

        word, level = self.word_manager.get_random_word(self.difficulty)
        self.update_word_display(word, level)
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_set()
        self.word_start = time.time()

    def check_word(self, event=None):
        if not self.is_running or not self.current_word:
            return

        typed = self.input_entry.get().strip()
        self.total += 1
        time_taken = time.time() - self.word_start

        if typed.lower() == self.current_word.lower():
            self.correct += 1
            self.words_typed += 1
            self.streak += 1
            self.combo += 1

            if self.streak > self.best_streak:
                self.best_streak = self.streak
            if self.combo > self.max_combo:
                self.max_combo = self.combo

            word_bonus = len(self.current_word) * 2
            speed_bonus = max(0, int((2 - time_taken) * 3))
            combo_bonus = self.combo * 1

            points = word_bonus + speed_bonus + combo_bonus
            self.score += points

            xp_gain = max(1, int(points / 5))
            self.xp_earned += xp_gain

            if self.combo > 0 and self.combo % 5 == 0:
                self.play_sound(800, 200)
                self.msg_label.config(
                    text=f"🔥 {self.combo}x Combo! +{points} (+{xp_gain} XP)",
                    fg="#e67e22",
                )
            else:
                self.msg_label.config(
                    text=f"✅ +{points} (+{xp_gain} XP)", fg=self.theme.get("correct")
                )

            self.play_sound(1000, 100)
            self.word_display.config(fg=self.theme.get("correct"))

            emoji = self.get_word_emoji(self.current_word_level)
            display_word = self.convert_case(self.current_word)
            self.last_words.append(f"{emoji} {display_word} ✅ ({time_taken:.1f}s)")

        else:
            self.errors += 1
            self.combo = 0
            self.streak = 0
            self.score = max(0, self.score - 3)

            self.play_sound(200, 300)
            self.msg_label.config(
                text=f"❌ Wrong! Correct: {self.convert_case(self.current_word)}",
                fg=self.theme.get("wrong"),
            )
            self.word_display.config(fg=self.theme.get("wrong"))

            emoji = self.get_word_emoji(self.current_word_level)
            display_word = self.convert_case(self.current_word)
            self.last_words.append(f"{emoji} {display_word} ❌ ({time_taken:.1f}s)")

            if self.mode == "endless" or self.mode == "hardcore":
                self.update_progress_display()
                if self.errors >= self.max_errors:
                    self.game_over()
                    return

            self.root.after(800, self.next_word)
            self.update_ui()
            self.update_last_words()
            return

        self.update_ui()
        self.update_last_words()
        self.update_progress_display()
        self.next_word()

    def update_ui(self):
        self.score_label.config(text=f"🎯 {self.score}")

        elapsed = time.time() - self.start_time
        if elapsed > 0:
            wpm = (self.words_typed / elapsed) * 60
            self.wpm_label.config(text=f"⚡ {int(wpm)} WPM")

        if self.total > 0:
            acc = (self.correct / self.total) * 100
            self.acc_label.config(text=f"✅ {int(acc)}%")

        self.combo_label.config(text=f"🔥 {self.combo}x")
        self.streak_label.config(text=f"⭐ {self.streak}")

    def update_last_words(self):
        self.last_text.delete(1.0, tk.END)
        for i, word in enumerate(self.last_words[-8:], 1):
            self.last_text.insert(tk.END, f"{i}. {word}\n")

    def update_stats_display(self):
        """به‌روزرسانی نمایش آمار در صفحه اصلی (از حافظه)"""
        # Daily stats
        self.daily_text.delete(1.0, tk.END)
        self.daily_text.insert(
            tk.END,
            f"Words: {self.daily_stats['words']}\n"
            f"Score: {self.daily_stats['score']}\n"
            f"Best WPM: {self.daily_stats['wpm']}  |  Acc: {self.daily_stats['accuracy']}%",
        )

        # Best stats
        self.best_text.delete(1.0, tk.END)
        self.best_text.insert(
            tk.END,
            f"🏆 Best WPM: {self.best_stats['wpm']}\n"
            f"🎯 Best Score: {self.best_stats['score']}\n"
            f"⭐ Best Streak: {self.best_stats['streak']}  |  🔥 Max Combo: {self.best_stats['combo']}",
        )

        # Session history
        self.history_text.delete(1.0, tk.END)
        if self.session_history:
            for s in self.session_history[-8:][::-1]:  # آخرین ۸ جلسه
                self.history_text.insert(
                    tk.END,
                    f"{s['date'][5:16]} | {s['mode']} | {s['difficulty']} | "
                    f"{s['wpm']} WPM | {s['accuracy']}%\n",
                )
        else:
            self.history_text.insert(tk.END, "No games played yet!")

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        self.fullscreen_btn.config(
            text="⛶ Exit" if self.is_fullscreen else "⛶ Fullscreen"
        )

    def change_font_size(self, size):
        self.font_size = size
        self.word_display.configure(font=("Arial", size, "bold"))

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_btn.config(
            text="🔊 Sound" if self.sound_enabled else "🔇 Mute",
            bg="#2ecc71" if self.sound_enabled else "#e74c3c",
        )

    def toggle_theme(self):
        self.theme.toggle()
        self.apply_theme()
        self.msg_label.config(
            text=f"🎨 Theme: {self.theme.current_theme.title()}",
            fg=self.theme.get("correct"),
        )

    def update_progress_display(self):
        if self.mode == "endless":
            remaining = self.max_errors - self.errors
            self.progress_label.config(text=f"❤️ {remaining} lives")
        elif self.mode == "hardcore":
            if self.errors >= 1:
                self.progress_label.config(text="💀 Game Over")
            else:
                self.progress_label.config(text="💀 1 mistake = Game Over")
        else:
            self.progress_label.config(text="")

    def play_sound(self, freq, duration):
        if self.sound_enabled:
            try:
                winsound.Beep(freq, duration)
            except:
                pass

    def on_key_press(self, event):
        if self.is_running and self.sound_enabled:
            try:
                freq = random.randint(800, 1200)
                winsound.Beep(freq, 20)
            except:
                pass

    def start_game(self):
        if hasattr(self, "timer_id"):
            self.root.after_cancel(self.timer_id)

        self.is_running = True
        self.score = 0
        self.total = 0
        self.correct = 0
        self.words_typed = 0
        self.errors = 0
        self.combo = 0
        self.max_combo = 0
        self.streak = 0
        self.best_streak = 0
        self.xp_earned = 0

        if self.mode == "hardcore":
            self.max_errors = 1
        elif self.mode == "endless":
            self.max_errors = 3
        else:
            self.max_errors = 999

        if self.mode == "endless" or self.mode == "hardcore":
            self.time_left = 999
        else:
            self.time_left = self.game_duration

        self.last_words = []
        self.start_time = time.time()
        self.animation_phase = 0
        self.animation_running = True

        self.update_ui()
        self.input_entry.config(state="normal")
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_set()

        self.start_btn.config(text="🔄 New Game")
        self.pause_btn.config(state="normal")
        self.msg_label.config(text="🎯 Type the words!", fg=self.theme.get("correct"))
        self.update_progress_display()

        self.next_word()
        self.animate_word()

        if self.mode != "endless" and self.mode != "hardcore":
            self.update_timer()

    def animate_word(self):
        if not self.is_running:
            self.animation_running = False
            return

        if not hasattr(self, "animation_running") or not self.animation_running:
            return

        self.animation_phase += 0.1
        if self.theme.is_dark():
            intensity = 0.5 + 0.5 * math.sin(self.animation_phase)
            glow = int(200 + 55 * intensity)
            self.word_display.config(
                fg=f"#{glow:02x}ff{int(255 - intensity * 100):02x}"
            )

        self.root.after(100, self.animate_word)

    def toggle_pause(self):
        if self.is_running:
            self.is_running = False
            self.pause_btn.config(text="▶️ Resume")
            self.msg_label.config(text="⏸️ Paused", fg="#f39c12")
            self.animation_running = False
            if hasattr(self, "timer_id"):
                self.root.after_cancel(self.timer_id)
        else:
            self.is_running = True
            self.pause_btn.config(text="⏸️ Pause")
            self.msg_label.config(text="▶️ Resumed", fg=self.theme.get("correct"))
            self.animation_running = True
            self.animate_word()
            if self.mode != "endless" and self.mode != "hardcore":
                self.update_timer()

    def update_timer(self):
        if not self.is_running:
            return

        self.time_left -= 0.1
        self.time_label.config(text=f"⏱️ {int(self.time_left)}s")
        self.progress["value"] = (
            (self.game_duration - self.time_left) / self.game_duration
        ) * 100

        if self.time_left <= 0:
            self.game_over()
        else:
            self.timer_id = self.root.after(100, self.update_timer)

    def game_over(self):
        self.is_running = False
        self.animation_running = False
        self.input_entry.config(state="disabled")
        self.pause_btn.config(state="disabled")
        self.msg_label.config(text="🏁 Game Over!", fg=self.theme.get("wrong"))

        self.play_sound(500, 300)
        self.play_sound(300, 300)

        elapsed = time.time() - self.start_time
        wpm = (self.words_typed / elapsed) * 60 if elapsed > 0 else 0
        acc = (self.correct / self.total) * 100 if self.total > 0 else 0

        # اضافه کردن XP
        if self.xp_earned > 0:
            self.add_xp(self.xp_earned)

        # به‌روزرسانی آمار جلسه
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.daily_stats["words"] += self.words_typed
        self.daily_stats["score"] += self.score
        if wpm > self.daily_stats["wpm"]:
            self.daily_stats["wpm"] = int(wpm)
        if acc > self.daily_stats["accuracy"]:
            self.daily_stats["accuracy"] = int(acc)

        # به‌روزرسانی بهترین رکوردها
        if wpm > self.best_stats["wpm"]:
            self.best_stats["wpm"] = int(wpm)
        if self.score > self.best_stats["score"]:
            self.best_stats["score"] = self.score
        if self.best_streak > self.best_stats["streak"]:
            self.best_stats["streak"] = self.best_streak
        if self.max_combo > self.best_stats["combo"]:
            self.best_stats["combo"] = self.max_combo

        # ذخیره در تاریخچه جلسات
        self.session_history.append(
            {
                "date": today,
                "score": self.score,
                "words": self.words_typed,
                "wpm": int(wpm),
                "accuracy": int(acc),
                "difficulty": self.difficulty,
                "mode": self.mode,
                "streak": self.best_streak,
                "combo": self.max_combo,
                "xp_gained": self.xp_earned,
            }
        )

        self.update_stats_display()
        self.update_xp_display()

        messagebox.showinfo(
            "Game Over",
            f"🏆 Score: {self.score}\n"
            f"📝 Words: {self.words_typed}\n"
            f"⚡ WPM: {int(wpm)}\n"
            f"✅ Accuracy: {int(acc)}%\n"
            f"🔥 Best Streak: {self.best_streak}\n"
            f"💎 Max Combo: {self.max_combo}\n"
            f"⭐ XP Gained: {self.xp_earned}\n"
            f"📈 Level: {self.level}",
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    game = TypingGame(root)
    root.mainloop()
