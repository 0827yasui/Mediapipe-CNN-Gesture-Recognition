import tkinter as tk

from ui.layer2.camera import open_camera
from ui.layer2.frame import open_frame
from ui.layer2.learning import open_learning
from ui.layer2.mediapipe import open_mediapipe
from ui.layer2.cnn import open_cnn


BG = "#1e1e1e"
PANEL = "#252526"
BUTTON = "#3a3a3f"
BUTTON_HOVER = "#4a4a50"

TEXT = "#ffffff"
SUBTEXT = "#aaaaaa"
ACCENT = "#6ea8fe"


def make_button(parent, text, command):
    button = tk.Button(
        parent,
        text=text,
        command=command,
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

    button.bind(
        "<Enter>",
        lambda event: button.configure(bg=BUTTON_HOVER),
    )
    button.bind(
        "<Leave>",
        lambda event: button.configure(bg=BUTTON),
    )

    return button


def open_setting(parent):
    window = tk.Toplevel(parent)
    window.title("SYSTEM CONFIGURATION")
    window.geometry("700x720")
    window.configure(bg=BG)
    window.minsize(620, 650)

    tk.Label(
        window,
        text="設定",
        font=("Segoe UI", 26, "bold"),
        fg=TEXT,
        bg=BG,
    ).pack(pady=(28, 2))

    tk.Label(
        window,
        text="SYSTEM CONFIGURATION",
        font=("Segoe UI", 10),
        fg=SUBTEXT,
        bg=BG,
    ).pack(pady=(0, 25))

    panel = tk.Frame(window, bg=PANEL)
    panel.pack(
        fill="both",
        expand=True,
        padx=45,
        pady=(0, 30),
    )

    tk.Label(
        panel,
        text="CONFIGURATION",
        font=("Segoe UI", 11, "bold"),
        fg=ACCENT,
        bg=PANEL,
    ).pack(anchor="w", padx=25, pady=(22, 15))

    make_button(
        panel,
        "CAMERA  /  camera_dat.yaml",
        lambda: open_camera(window),
    ).pack(fill="x", padx=25, pady=5)

    make_button(
        panel,
        "FRAME  /  frame_dat.yaml",
        lambda: open_frame(window),
    ).pack(fill="x", padx=25, pady=5)

    make_button(
        panel,
        "LEARNING  /  learning.yaml",
        lambda: open_learning(window),
    ).pack(fill="x", padx=25, pady=5)

    make_button(
        panel,
        "MEDIAPIPE  /  mediapipe_dat.yaml",
        lambda: open_mediapipe(window),
    ).pack(fill="x", padx=25, pady=5)

    make_button(
        panel,
        "CNN  /  MODEL BUILDER",
        lambda: open_cnn(window),
    ).pack(fill="x", padx=25, pady=5)
