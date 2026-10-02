import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "mediapipe_dat.yaml"

BG = "#1e1e1e"
PANEL = "#252526"
BUTTON = "#3a3a3f"
BUTTON_HOVER = "#4a4a50"
TEXT = "#ffffff"
SUBTEXT = "#aaaaaa"
ACCENT = "#6ea8fe"


def load_config():
    with open(CONFIG, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config):
    with open(CONFIG, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)


def make_section(parent, title, data):
    frame = tk.Frame(parent, bg=PANEL)
    frame.pack(fill="x", pady=7)

    tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 12, "bold"),
        fg=ACCENT,
        bg=PANEL,
    ).pack(anchor="w", padx=20, pady=(14, 8))

    values = {}

    fields = [
        ("Number_of_" + title.lower() + "s_", int, 1),
        ("min_" + title.lower() + "_detection_confidence_", float, 0.5),
        ("min_" + title.lower() + "_presence_confidence_", float, 0.5),
        ("min_tracking_confidence_", float, 0.5),
    ]

    for key, value_type, default in fields:
        current = data.get(key, default)

        row = tk.Frame(frame, bg=PANEL)
        row.pack(fill="x", padx=20, pady=3)

        tk.Label(
            row,
            text=key,
            font=("Segoe UI", 9),
            fg=TEXT,
            bg=PANEL,
            width=34,
            anchor="w",
        ).pack(side="left")

        var = tk.StringVar(value=str(current))
        entry = tk.Entry(
            row,
            textvariable=var,
            font=("Segoe UI", 9),
            bg=BUTTON,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
        )
        entry.pack(side="left", fill="x", expand=True, ipady=4)

        values[key] = (var, value_type)

    return values


def open_mediapipe(parent):
    config = load_config()

    window = tk.Toplevel(parent)
    window.title("MEDIAPIPE CONFIGURATION")
    window.geometry("820x680")
    window.configure(bg=BG)
    window.minsize(720, 620)

    tk.Label(
        window,
        text="MEDIAPIPE",
        font=("Segoe UI", 24, "bold"),
        fg=TEXT,
        bg=BG,
    ).pack(pady=(22, 2))

    tk.Label(
        window,
        text="MEDIAPIPE CONFIGURATION",
        font=("Segoe UI", 10),
        fg=SUBTEXT,
        bg=BG,
    ).pack(pady=(0, 12))

    content = tk.Frame(window, bg=BG)
    content.pack(fill="both", expand=True, padx=35)

    hand = make_section(content, "HAND", config.get("hand", {}))
    face = make_section(content, "FACE", config.get("face", {}))

    def read_section(values):
        result = {}

        for key, (var, value_type) in values.items():
            try:
                value = value_type(var.get())
            except ValueError:
                raise ValueError(key)

            if value_type is int:
                if value <= 0:
                    raise ValueError(key)
            else:
                if not 0.0 <= value <= 1.0:
                    raise ValueError(key)

            result[key] = value

        return result

    def save():
        try:
            config["hand"] = read_section(hand)
            config["face"] = read_section(face)
        except ValueError as error:
            messagebox.showerror(
                "入力エラー",
                f"入力値を確認してください。\n{error}",
                parent=window,
            )
            return

        save_config(config)

        messagebox.showinfo(
            "保存完了",
            "mediapipe_dat.yaml を保存しました。",
            parent=window,
        )

    tk.Button(
        window,
        text="SAVE  /  mediapipe_dat.yaml",
        command=save,
        font=("Segoe UI", 10, "bold"),
        fg=TEXT,
        bg=BUTTON,
        activebackground=BUTTON_HOVER,
        activeforeground=TEXT,
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=10,
    ).pack(pady=18)
