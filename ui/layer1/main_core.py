import tkinter as tk

from ui.layer2.learning import open_learning
from ui.layer2.data import open_data
from ui.layer2.interface import open_interface
from ui.layer2.generate import open_generate
from ui.layer2.setting import open_setting


def make_background(canvas):
    # グリッド
    for x in range(0, 800, 50):
        canvas.create_line(
            x, 0,
            x, 700,
            fill="#252525"
        )

    for y in range(0, 700, 50):
        canvas.create_line(
            0, y,
            800, y,
            fill="#252525"
        )

    # 回路基板風の装飾
    circuits = [
        # 左上
        [(0, 80), (80, 80), (110, 110)],
        [(0, 130), (50, 130), (80, 160)],
        [(120, 0), (120, 55), (160, 95)],

        # 右上
        [(580, 0), (580, 55), (540, 95)],
        [(700, 100), (640, 100), (610, 130)],
        [(800, 160), (730, 160), (700, 190)],

        # 左下
        [(0, 470), (70, 470), (100, 440)],
        [(0, 530), (45, 530), (80, 495)],
        [(160, 600), (160, 550), (200, 510)],

        # 右下
        [(800, 470), (730, 470), (700, 440)],
        [(800, 530), (755, 530), (720, 495)],
        [(640, 600), (640, 550), (600, 510)],
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

        # 終点に小さな端子
        x, y = points[-1]

        canvas.create_rectangle(
            x - 3,
            y - 3,
            x + 3,
            y + 3,
            fill="#3b3b3b",
            outline=""
        )

    # 角に薄いフレーム
    canvas.create_rectangle(
        20,
        20,
        780,
        680,
        outline="#292929",
        width=1
    )


def make_first_window():
    window = tk.Tk()

    window.title("MediaPipe CNN")
    window.geometry("700x600")
    window.configure(bg="#1e1e1e")

    # 背景Canvas
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

    # UIを前面に置く
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
        text="MediaPipe CNN",
        font=("Segoe UI", 28, "bold"),
        bg="#1e1e1e",
        fg="white"
    )

    title.pack(pady=(0, 5))

    # サブタイトル
    subtitle = tk.Label(
        main_frame,
        text="Hand Recognition System",
        font=("Segoe UI", 12),
        bg="#1e1e1e",
        fg="#aaaaaa"
    )

    subtitle.pack(pady=(0, 30))

    # ボタン用Frame
    button_frame = tk.Frame(
        main_frame,
        bg="#1e1e1e"
    )

    button_frame.pack()

    # ボタン作成
    def make_button(text, command):
        return tk.Button(
            button_frame,
            text=text,
            command=command,
            font=("Yu Gothic UI", 14),
            width=22,
            height=2,
            bg="#2d2d30",
            fg="white",
            activebackground="#404045",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2"
        )

    button_study = make_button(
        "学習",
        lambda: open_learning(window)
    )

    button_data = make_button(
        "データを撮る",
        lambda: open_data(window)
    )

    button_interface = make_button(
        "interface",
        lambda: open_interface(window)
    )

    button_generate = make_button(
        "generateコード",
        lambda: open_generate(window)
    )

    button_setting = make_button(
        "設定",
        lambda: open_setting(window)
    )

    # 2 × 2
    button_study.grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    button_data.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    button_interface.grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )

    button_generate.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    # 設定
    button_setting.grid(
        row=2,
        column=0,
        columnspan=2,
        padx=10,
        pady=10
    )

    # CanvasがUIより前に出ないようにする
    main_frame.lift()

    window.mainloop()


if __name__ == "__main__":
    make_first_window()