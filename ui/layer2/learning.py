import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "learning.yaml"

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

    for key in ("epoch", "batch"):
        row = tk.Frame(frame, bg=PANEL)
        row.pack(fill="x", padx=20, pady=4)

        tk.Label(
            row,
            text=key.capitalize(),
            font=("Segoe UI", 10),
            fg=TEXT,
            bg=PANEL,
            width=12,
            anchor="w",
        ).pack(side="left")

        var = tk.StringVar(value=str(data.get(key, 1)))
        entry = tk.Entry(
            row,
            textvariable=var,
            font=("Segoe UI", 10),
            bg=BUTTON,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
        )
        entry.pack(side="left", fill="x", expand=True, ipady=5)
        values[key] = var

    shuffle_var = tk.BooleanVar(value=bool(data.get("shuffle", True)))

    tk.Checkbutton(
        frame,
        text="Shuffle",
        variable=shuffle_var,
        font=("Segoe UI", 10),
        fg=TEXT,
        bg=PANEL,
        activebackground=PANEL,
        activeforeground=TEXT,
        selectcolor=BUTTON,
    ).pack(anchor="w", padx=20, pady=(6, 15))

    values["shuffle"] = shuffle_var
    return values


def open_learning(parent):
    config = load_config()

    window = tk.Toplevel(parent)
    window.title("LEARNING CONFIGURATION")
    window.geometry("620x620")
    window.configure(bg=BG)
    window.minsize(560, 560)

    tk.Label(
        window,
        text="LEARNING",
        font=("Segoe UI", 24, "bold"),
        fg=TEXT,
        bg=BG,
    ).pack(pady=(25, 2))

    tk.Label(
        window,
        text="LEARNING CONFIGURATION",
        font=("Segoe UI", 10),
        fg=SUBTEXT,
        bg=BG,
    ).pack(pady=(0, 15))

    content = tk.Frame(window, bg=BG)
    content.pack(fill="both", expand=True, padx=35)

    train = make_section(content, "TRAIN", config.get("train", {}))
    test = make_section(content, "TEST", config.get("test", {}))

    def read_section(values):
        epoch = int(values["epoch"].get())
        batch = int(values["batch"].get())

        if epoch <= 0 or batch <= 0:
            raise ValueError

        return {
            "epoch": epoch,
            "batch": batch,
            "shuffle": bool(values["shuffle"].get()),
        }

    def save():
        try:
            config["train"] = read_section(train)
            config["test"] = read_section(test)
        except ValueError:
            messagebox.showerror(
                "入力エラー",
                "EpochとBatchには1以上の整数を入力してください。",
                parent=window,
            )
            return

        save_config(config)

        messagebox.showinfo(
            "保存完了",
            "learning.yaml を保存しました。",
            parent=window,
        )

    tk.Button(
        window,
        text="SAVE  /  learning.yaml",
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
    ).pack(pady=20)
