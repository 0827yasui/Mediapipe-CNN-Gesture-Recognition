import tkinter as tk
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def make_background(canvas):
    # グリッド
    for x in range(0, 500, 50):
        canvas.create_line(
            x, 0,
            x, 500,
            fill="#252525"
        )

    for y in range(0, 500, 50):
        canvas.create_line(
            0, y,
            500, y,
            fill="#252525"
        )

    # 回路風装飾
    circuits = [
        [(0, 60), (60, 60), (90, 90)],
        [(0, 110), (40, 110), (70, 140)],
        [(400, 0), (400, 50), (360, 90)],
        [(500, 100), (450, 100), (420, 130)],
        [(0, 390), (60, 390), (90, 360)],
        [(500, 380), (440, 380), (410, 350)],
        [(100, 500), (100, 450), (140, 410)],
        [(400, 500), (400, 450), (360, 410)],
    ]

    for points in circuits:
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            canvas.create_line(
                x1, y1,
                x2, y2,
                fill="#303030",
                width=2
            )

        x, y = points[-1]

        canvas.create_rectangle(
            x - 3,
            y - 3,
            x + 3,
            y + 3,
            fill="#3b3b3b",
            outline=""
        )


def open_data(parent):
    window = tk.Toplevel(parent)

    window.title("データを撮る")
    window.geometry("500x400")
    window.configure(bg="#1e1e1e")

    # 背景
    background = tk.Canvas(
        window,
        bg="#1e1e1e",
        highlightthickness=0
    )

    background.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    make_background(background)

    # 中央UI
    main_frame = tk.Frame(
        window,
        bg="#1e1e1e"
    )

    main_frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    # タイトル
    title = tk.Label(
        main_frame,
        text="データを撮る",
        font=("Segoe UI", 22, "bold"),
        bg="#1e1e1e",
        fg="white"
    )

    title.pack(pady=(0, 25))

    # ボタン
    def make_button(text, command):
        return tk.Button(
            main_frame,
            text=text,
            command=command,
            font=("Yu Gothic UI", 14),
            width=24,
            height=2,
            bg="#2d2d30",
            fg="white",
            activebackground="#404045",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        )

    train_button = make_button(
        "train",
        lambda: subprocess.Popen(
            [
                sys.executable,
                "-m",
                "src.main.data_train_make_main"
            ],
            cwd=ROOT
        )
    )

    test_button = make_button(
        "test",
        lambda: subprocess.Popen(
            [
                sys.executable,
                "-m",
                "src.main.data_test_make_main"
            ],
            cwd=ROOT
        )
    )

    train_button.pack(pady=10)
    test_button.pack(pady=10)

    main_frame.lift()