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
            x, 400,
            fill="#252525"
        )

    for y in range(0, 400, 50):
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
        [(0, 330), (60, 330), (90, 300)],
        [(500, 320), (440, 320), (410, 290)],
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


def open_interface(parent):
    window = tk.Toplevel(parent)

    window.title("interface")
    window.geometry("500x350")
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
    tk.Label(
        main_frame,
        text="interface",
        font=("Segoe UI", 22, "bold"),
        bg="#1e1e1e",
        fg="white"
    ).pack(pady=(0, 25))

    # 起動ボタン
    tk.Button(
        main_frame,
        text="interfaceを起動",
        font=("Yu Gothic UI", 14),
        width=24,
        height=2,
        bg="#2d2d30",
        fg="white",
        activebackground="#404045",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda: subprocess.Popen(
            [
                sys.executable,
                "-m",
                "src.main.interface_main"
            ],
            cwd=ROOT
        )
    ).pack(pady=10)

    main_frame.lift()