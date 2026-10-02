import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "frame_dat.yaml"

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


def open_frame(parent):
    config = load_config()

    window = tk.Toplevel(parent)
    window.title("FRAME CONFIGURATION")
    window.geometry("520x360")
    window.configure(bg=BG)
    window.resizable(False, False)

    tk.Label(
        window,
        text="FRAME",
        font=("Segoe UI", 24, "bold"),
        fg=TEXT,
        bg=BG,
    ).pack(pady=(28, 2))

    tk.Label(
        window,
        text="FRAME CONFIGURATION",
        font=("Segoe UI", 10),
        fg=SUBTEXT,
        bg=BG,
    ).pack(pady=(0, 24))

    panel = tk.Frame(window, bg=PANEL)
    panel.pack(fill="x", padx=35)

    tk.Label(
        panel,
        text="Flip",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT,
        bg=PANEL,
    ).pack(anchor="w", padx=20, pady=(18, 4))

    flip_var = tk.StringVar(value=str(config.get("flip", "horizontal")))

    flip_menu = tk.OptionMenu(
        panel,
        flip_var,
        "horizontal",
        "vertical",
        "none",
    )
    flip_menu.config(
        font=("Segoe UI", 11),
        fg=TEXT,
        bg=BUTTON,
        activebackground=BUTTON_HOVER,
        activeforeground=TEXT,
        highlightthickness=0,
        relief="flat",
    )
    flip_menu["menu"].config(
        bg=BUTTON,
        fg=TEXT,
        activebackground=BUTTON_HOVER,
        activeforeground=TEXT,
    )
    flip_menu.pack(fill="x", padx=20, pady=(0, 20))

    def save():
        config["flip"] = flip_var.get()
        save_config(config)

        messagebox.showinfo(
            "保存完了",
            "frame_dat.yaml を保存しました。",
            parent=window,
        )

    tk.Button(
        window,
        text="SAVE  /  frame_dat.yaml",
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
    ).pack(pady=25)
