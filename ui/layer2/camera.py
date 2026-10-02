import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config" / "camera_dat.yaml"

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


def open_camera(parent):
    config = load_config()

    window = tk.Toplevel(parent)
    window.title("CAMERA CONFIGURATION")
    window.geometry("520x360")
    window.configure(bg=BG)
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="CAMERA",
        font=("Segoe UI", 24, "bold"),
        fg=TEXT,
        bg=BG,
    )
    title.pack(pady=(28, 2))

    subtitle = tk.Label(
        window,
        text="CAMERA CONFIGURATION",
        font=("Segoe UI", 10),
        fg=SUBTEXT,
        bg=BG,
    )
    subtitle.pack(pady=(0, 24))

    panel = tk.Frame(window, bg=PANEL)
    panel.pack(fill="x", padx=35)

    tk.Label(
        panel,
        text="Camera Index",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT,
        bg=PANEL,
    ).pack(anchor="w", padx=20, pady=(18, 4))

    index_var = tk.StringVar(value=str(config.get("index", 0)))

    entry = tk.Entry(
        panel,
        textvariable=index_var,
        font=("Segoe UI", 12),
        bg=BUTTON,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
    )
    entry.pack(fill="x", padx=20, pady=(0, 18), ipady=7)

    def save():
        try:
            index = int(index_var.get())
            if index < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "入力エラー",
                "Camera Indexには0以上の整数を入力してください。",
                parent=window,
            )
            return

        config["index"] = index
        save_config(config)

        messagebox.showinfo(
            "保存完了",
            "camera_dat.yaml を保存しました。",
            parent=window,
        )

    button = tk.Button(
        window,
        text="SAVE  /  camera_dat.yaml",
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
    )
    button.pack(pady=25)
