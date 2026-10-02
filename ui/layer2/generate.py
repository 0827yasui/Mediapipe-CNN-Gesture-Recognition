import tkinter as tk
from tkinter import messagebox

from src.main.result_generate_main import generate_result, generate_best_result


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


def open_generate(parent):
    window = tk.Toplevel(parent)

    window.title("generateコード")
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
        text="generateコード",
        font=("Segoe UI", 22, "bold"),
        bg="#1e1e1e",
        fg="white"
    )

    title.pack(pady=(0, 25))

    # ボタン作成
    def make_button(text, command):
        return tk.Button(
            main_frame,
            text=text,
            command=command,
            font=("Yu Gothic UI", 13),
            width=28,
            height=2,
            bg="#2d2d30",
            fg="white",
            activebackground="#404045",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        )

    def generate_best():
        try:
            generate_best_result()

            messagebox.showinfo(
                "generateコード",
                "最高スコアの状態にしました。",
                parent=window
            )

        except Exception as e:
            messagebox.showerror(
                "generateコード",
                str(e),
                parent=window
            )

    def generate_manual():
        input_window = tk.Toplevel(window)

        input_window.title("Result指定")
        input_window.geometry("400x250")
        input_window.configure(bg="#1e1e1e")

        # 背景
        input_background = tk.Canvas(
            input_window,
            bg="#1e1e1e",
            highlightthickness=0
        )

        input_background.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        make_background(input_background)

        input_frame = tk.Frame(
            input_window,
            bg="#1e1e1e"
        )

        input_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            input_frame,
            text="Result名を入力してください",
            font=("Yu Gothic UI", 13),
            bg="#1e1e1e",
            fg="white"
        ).pack(pady=(0, 12))

        result_entry = tk.Entry(
            input_frame,
            width=30,
            font=("Yu Gothic UI", 12),
            bg="#2d2d30",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=0
        )

        result_entry.pack(ipady=8)

        def generate():
            result_name = result_entry.get()

            if not result_name:
                messagebox.showwarning(
                    "Result指定",
                    "Result名を入力してください。",
                    parent=input_window
                )
                return

            try:
                generate_result(result_name)

                messagebox.showinfo(
                    "generateコード",
                    "指定したResultの状態にしました。",
                    parent=input_window
                )

                input_window.destroy()

            except Exception as e:
                messagebox.showerror(
                    "generateコード",
                    str(e),
                    parent=input_window
                )

        tk.Button(
            input_frame,
            text="生成",
            command=generate,
            font=("Yu Gothic UI", 12),
            width=20,
            height=2,
            bg="#2d2d30",
            fg="white",
            activebackground="#404045",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(pady=15)

        input_frame.lift()

    make_button(
        "最高スコアの状態にする",
        generate_best
    ).pack(pady=10)

    make_button(
        "自分で書いてその状態にする",
        generate_manual
    ).pack(pady=10)

    main_frame.lift()