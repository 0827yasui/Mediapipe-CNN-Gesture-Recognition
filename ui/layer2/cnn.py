import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[2]
CNN_CONFIG = ROOT / "config" / "CNN_dat.yaml"

BG = "#1e1e1e"
PANEL = "#252526"
BLOCK = "#2d2d30"
BUTTON = "#3a3a3f"
BUTTON_HOVER = "#4a4a50"

TEXT = "#ffffff"
SUBTEXT = "#aaaaaa"
ACCENT = "#6ea8fe"
DELETE = "#c94f4f"


# =========================================================
# YAML
# =========================================================

def load_config():

    with open(
        CNN_CONFIG,
        "r",
        encoding="utf-8"
    ) as f:

        return yaml.safe_load(f)


def save_config(config):

    with open(
        CNN_CONFIG,
        "w",
        encoding="utf-8"
    ) as f:

        yaml.safe_dump(
            config,
            f,
            allow_unicode=True,
            sort_keys=False
        )


# =========================================================
# CNN形状計算
# =========================================================

def calculate_shapes(config):

    model = config["model"]

    channel = int(
        model["input"]["channel"]
    )

    width = int(
        model["input"]["width"]
    )

    height = int(
        model["input"]["height"]
    )

    if channel <= 0:
        raise ValueError(
            "input channel は1以上にしてください。"
        )

    if width <= 0 or height <= 0:
        raise ValueError(
            "input width / height は1以上にしてください。"
        )

    for layer in model["layers"]:

        layer_type = layer["type"]

        # ---------------------------------
        # Conv2d
        # ---------------------------------

        if layer_type == "Conv2d":

            kernel = int(
                layer["kernel_size"]
            )

            stride = int(
                layer["stride"]
            )

            output_channel = int(
                layer["output_channel"]
            )

            if kernel <= 0:
                raise ValueError(
                    "Conv2dのkernel_sizeは1以上にしてください。"
                )

            if stride <= 0:
                raise ValueError(
                    "Conv2dのstrideは1以上にしてください。"
                )

            if output_channel <= 0:
                raise ValueError(
                    "Conv2dのoutput_channelは1以上にしてください。"
                )

            # 自動計算
            layer["input_channel"] = channel

            width = (
                (width - kernel)
                // stride
            ) + 1

            height = (
                (height - kernel)
                // stride
            ) + 1

            channel = output_channel

        # ---------------------------------
        # ReLU
        # ---------------------------------

        elif layer_type == "ReLU":

            pass

        # ---------------------------------
        # MaxPool2d
        # ---------------------------------

        elif layer_type == "MaxPool2d":

            kernel = int(
                layer["kernel_size"]
            )

            padding = int(
                layer["padding"]
            )

            stride = int(
                layer["stride"]
            )

            if kernel <= 0:
                raise ValueError(
                    "MaxPool2dのkernel_sizeは1以上にしてください。"
                )

            if padding < 0:
                raise ValueError(
                    "MaxPool2dのpaddingは0以上にしてください。"
                )

            if stride <= 0:
                raise ValueError(
                    "MaxPool2dのstrideは1以上にしてください。"
                )

            width = (
                width
                + 2 * padding
                - kernel
            ) // stride + 1

            height = (
                height
                + 2 * padding
                - kernel
            ) // stride + 1

        # ---------------------------------
        # Flatten
        # ---------------------------------

        elif layer_type == "Flatten":

            pass

        # ---------------------------------
        # Linear
        # ---------------------------------

        elif layer_type == "Linear":

            output_size = int(
                layer["output_size"]
            )

            if output_size <= 0:
                raise ValueError(
                    "Linearのoutput_sizeは1以上にしてください。"
                )

            # 完全自動
            layer["input_size"] = (
                channel
                * width
                * height
            )

            channel = output_size

            width = 1
            height = 1

        # ---------------------------------
        # 不明なLayer
        # ---------------------------------

        else:

            raise ValueError(
                f"未対応のLayerです: {layer_type}"
            )

        # ---------------------------------
        # サイズが0以下になったらエラー
        # ---------------------------------

        if width <= 0 or height <= 0:

            raise ValueError(
                f"{layer_type} によって画像サイズが0以下になりました。"
            )

    return channel, width, height


# =========================================================
# CNN GUI
# =========================================================

def open_cnn(parent):

    window = tk.Toplevel(parent)

    window.title(
        "CNN MODEL BUILDER"
    )

    window.geometry(
        "950x850"
    )

    window.minsize(
        800,
        650
    )

    window.configure(
        bg=BG
    )

    config = load_config()

    # =====================================================
    # タイトル
    # =====================================================

    title_frame = tk.Frame(
        window,
        bg=BG
    )

    title_frame.pack(
        fill="x",
        padx=25,
        pady=(20, 10)
    )

    tk.Label(
        title_frame,
        text="CNN",
        font=("Segoe UI", 25, "bold"),
        bg=BG,
        fg=TEXT
    ).pack()

    tk.Label(
        title_frame,
        text="CONVOLUTIONAL NEURAL NETWORK BUILDER",
        font=("Segoe UI", 9),
        bg=BG,
        fg=SUBTEXT
    ).pack()

    # =====================================================
    # Input設定
    # =====================================================

    input_frame = tk.Frame(
        window,
        bg=PANEL
    )

    input_frame.pack(
        fill="x",
        padx=25,
        pady=10
    )

    tk.Label(
        input_frame,
        text="INPUT",
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=TEXT
    ).pack(
        side="left",
        padx=15,
        pady=12
    )

    input_vars = {}

    for key in [
        "channel",
        "width",
        "height"
    ]:

        value = tk.IntVar(
            value=config["model"]["input"][key]
        )

        input_vars[key] = value

        tk.Label(
            input_frame,
            text=key,
            bg=PANEL,
            fg=SUBTEXT,
            font=("Segoe UI", 8)
        ).pack(
            side="left",
            padx=(15, 3)
        )

        tk.Entry(
            input_frame,
            textvariable=value,
            width=7,
            justify="center",
            bg=BLOCK,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        ).pack(
            side="left"
        )

    # =====================================================
    # Layerエリア
    # =====================================================

    layer_container = tk.Frame(
        window,
        bg=PANEL
    )

    layer_container.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    canvas = tk.Canvas(
        layer_container,
        bg=PANEL,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        layer_container,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    layer_frame = tk.Frame(
        canvas,
        bg=PANEL
    )

    canvas_window = canvas.create_window(
        0,
        0,
        window=layer_frame,
        anchor="nw"
    )

    def update_scroll(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    layer_frame.bind(
        "<Configure>",
        update_scroll
    )

    def resize_canvas(event):

        canvas.itemconfigure(
            canvas_window,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        resize_canvas
    )

    # =====================================================
    # ドラッグ状態
    # =====================================================

    drag_index = None

    # =====================================================
    # Layer更新
    # =====================================================

    def refresh():

        nonlocal drag_index

        drag_index = None

        for widget in layer_frame.winfo_children():
            widget.destroy()

        # まず形状を計算
        try:

            calculate_shapes(config)

        except ValueError as e:

            messagebox.showerror(
                "CNN構造エラー",
                str(e),
                parent=window
            )

        layers = config["model"]["layers"]

        for index, layer in enumerate(layers):

            create_layer_block(
                index,
                layer
            )

        layer_frame.update_idletasks()

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    # =====================================================
    # Layerブロック
    # =====================================================

    def create_layer_block(index, layer):

        block = tk.Frame(
            layer_frame,
            bg=BLOCK,
            highlightthickness=1,
            highlightbackground="#414141"
        )

        block.pack(
            fill="x",
            padx=12,
            pady=5
        )

        # ---------------------------------
        # 上段
        # ---------------------------------

        top = tk.Frame(
            block,
            bg=BLOCK
        )

        top.pack(
            fill="x",
            padx=12,
            pady=(9, 5)
        )

        # ドラッグハンドル
        handle = tk.Label(
            top,
            text="☷",
            font=("Segoe UI", 18),
            bg=BLOCK,
            fg=SUBTEXT,
            cursor="hand2"
        )

        handle.pack(
            side="left",
            padx=(0, 10)
        )

        tk.Label(
            top,
            text=f"{index + 1:02d}",
            font=("Consolas", 11, "bold"),
            bg=BLOCK,
            fg=ACCENT
        ).pack(
            side="left",
            padx=(0, 12)
        )

        tk.Label(
            top,
            text=layer["type"],
            font=("Segoe UI", 12, "bold"),
            bg=BLOCK,
            fg=TEXT
        ).pack(
            side="left"
        )

        # ---------------------------------
        # ボタン
        # ---------------------------------

        button_frame = tk.Frame(
            top,
            bg=BLOCK
        )

        button_frame.pack(
            side="right"
        )

        def move_up():

            if index == 0:
                return

            layers = config["model"]["layers"]

            layers[index - 1], layers[index] = (
                layers[index],
                layers[index - 1]
            )

            refresh()

        def move_down():

            layers = config["model"]["layers"]

            if index >= len(layers) - 1:
                return

            layers[index], layers[index + 1] = (
                layers[index + 1],
                layers[index]
            )

            refresh()

        def delete():

            layers = config["model"]["layers"]

            if not messagebox.askyesno(
                "削除",
                f"{layer['type']} を削除しますか？",
                parent=window
            ):
                return

            layers.pop(index)

            refresh()

        tk.Button(
            button_frame,
            text="↑",
            command=move_up,
            bg=BUTTON,
            fg=TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            width=3,
            cursor="hand2"
        ).pack(
            side="left",
            padx=2
        )

        tk.Button(
            button_frame,
            text="↓",
            command=move_down,
            bg=BUTTON,
            fg=TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            width=3,
            cursor="hand2"
        ).pack(
            side="left",
            padx=2
        )

        tk.Button(
            button_frame,
            text="編集",
            command=lambda i=index: edit_layer(i),
            bg=ACCENT,
            fg="white",
            activebackground="#5788cf",
            activeforeground="white",
            relief="flat",
            width=7,
            cursor="hand2"
        ).pack(
            side="left",
            padx=4
        )

        tk.Button(
            button_frame,
            text="削除",
            command=delete,
            bg=DELETE,
            fg="white",
            activebackground="#a63e3e",
            activeforeground="white",
            relief="flat",
            width=6,
            cursor="hand2"
        ).pack(
            side="left"
        )

        # ---------------------------------
        # パラメータ
        # ---------------------------------

        parameter_frame = tk.Frame(
            block,
            bg=BLOCK
        )

        parameter_frame.pack(
            fill="x",
            padx=60,
            pady=(0, 10)
        )

        show_parameters(
            parameter_frame,
            layer
        )

        # ---------------------------------
        # ドラッグ開始
        # ---------------------------------

        def start_drag(event):

            nonlocal drag_index

            drag_index = index

            handle.configure(
                fg=ACCENT
            )

        # ---------------------------------
        # ドラッグ終了
        # ---------------------------------

        def end_drag(event):

            nonlocal drag_index

            if drag_index is None:
                return

            layers = config["model"]["layers"]

            # マウス位置をLayer全体のY座標へ変換
            y = canvas.canvasy(
                event.y_root
                - canvas.winfo_rooty()
            )

            target = 0

            blocks = layer_frame.winfo_children()

            for i, widget in enumerate(blocks):

                center = (
                    widget.winfo_y()
                    + widget.winfo_height() / 2
                )

                if y > center:
                    target = i + 1

            target = min(
                target,
                len(layers) - 1
            )

            if drag_index != target:

                moving = layers.pop(
                    drag_index
                )

                layers.insert(
                    target,
                    moving
                )

            drag_index = None

            refresh()

        handle.bind(
            "<ButtonPress-1>",
            start_drag
        )

        handle.bind(
            "<ButtonRelease-1>",
            end_drag
        )

    # =====================================================
    # パラメータ表示
    # =====================================================

    def show_parameters(parent_frame, layer):

        layer_type = layer["type"]

        if layer_type == "Conv2d":

            values = [
                (
                    "input_channel",
                    layer["input_channel"],
                    True
                ),
                (
                    "output_channel",
                    layer["output_channel"],
                    False
                ),
                (
                    "kernel_size",
                    layer["kernel_size"],
                    False
                ),
                (
                    "stride",
                    layer["stride"],
                    False
                )
            ]

        elif layer_type == "MaxPool2d":

            values = [
                (
                    "kernel_size",
                    layer["kernel_size"],
                    False
                ),
                (
                    "padding",
                    layer["padding"],
                    False
                ),
                (
                    "stride",
                    layer["stride"],
                    False
                )
            ]

        elif layer_type == "Linear":

            values = [
                (
                    "input_size",
                    layer["input_size"],
                    True
                ),
                (
                    "output_size",
                    layer["output_size"],
                    False
                )
            ]

        else:

            return

        for name, value, auto in values:

            text = (
                f"{name}: {value}"
                + ("  [AUTO]" if auto else "")
            )

            tk.Label(
                parent_frame,
                text=text,
                font=("Consolas", 9),
                bg=BLOCK,
                fg=(
                    ACCENT
                    if auto
                    else SUBTEXT
                ),
                anchor="w"
            ).pack(
                fill="x"
            )

    # =====================================================
    # Layer編集
    # =====================================================

    def edit_layer(index):

        layers = config["model"]["layers"]

        layer = layers[index]

        editor = tk.Toplevel(
            window
        )

        editor.title(
            f"EDIT / {layer['type']}"
        )

        editor.geometry(
            "430x400"
        )

        editor.resizable(
            False,
            False
        )

        editor.configure(
            bg=BG
        )

        tk.Label(
            editor,
            text=layer["type"],
            font=("Segoe UI", 22, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(
            pady=(25, 0)
        )

        tk.Label(
            editor,
            text="LAYER PARAMETERS",
            font=("Segoe UI", 9),
            bg=BG,
            fg=SUBTEXT
        ).pack(
            pady=(0, 20)
        )

        form = tk.Frame(
            editor,
            bg=BG
        )

        form.pack(
            fill="x",
            padx=40
        )

        entries = {}

        # ---------------------------------
        # Entry作成
        # ---------------------------------

        def make_entry(name, value):

            row = tk.Frame(
                form,
                bg=BG
            )

            row.pack(
                fill="x",
                pady=7
            )

            tk.Label(
                row,
                text=name,
                font=("Segoe UI", 10),
                bg=BG,
                fg=TEXT,
                anchor="w",
                width=18
            ).pack(
                side="left"
            )

            entry = tk.Entry(
                row,
                width=12,
                justify="center",
                bg=BLOCK,
                fg=TEXT,
                insertbackground=TEXT,
                relief="flat"
            )

            entry.insert(
                0,
                str(value)
            )

            entry.pack(
                side="right"
            )

            entries[name] = entry

        # ---------------------------------
        # Conv2d
        # ---------------------------------

        if layer["type"] == "Conv2d":

            make_entry(
                "output_channel",
                layer["output_channel"]
            )

            make_entry(
                "kernel_size",
                layer["kernel_size"]
            )

            make_entry(
                "stride",
                layer["stride"]
            )

            tk.Label(
                form,
                text="input_channel は自動計算",
                bg=BG,
                fg=ACCENT,
                font=("Segoe UI", 9)
            ).pack(
                pady=10
            )

        # ---------------------------------
        # MaxPool2d
        # ---------------------------------

        elif layer["type"] == "MaxPool2d":

            make_entry(
                "kernel_size",
                layer["kernel_size"]
            )

            make_entry(
                "padding",
                layer["padding"]
            )

            make_entry(
                "stride",
                layer["stride"]
            )

        # ---------------------------------
        # Linear
        # ---------------------------------

        elif layer["type"] == "Linear":

            make_entry(
                "output_size",
                layer["output_size"]
            )

            tk.Label(
                form,
                text="input_size は自動計算",
                bg=BG,
                fg=ACCENT,
                font=("Segoe UI", 9)
            ).pack(
                pady=10
            )

        # ---------------------------------
        # 適用
        # ---------------------------------

        def apply():

            try:

                for key, entry in entries.items():

                    value = int(
                        entry.get()
                    )

                    if value <= 0:

                        raise ValueError

                    layer[key] = value

                # 変更後すぐ形状確認
                calculate_shapes(
                    config
                )

                editor.destroy()

                refresh()

            except ValueError as e:

                messagebox.showerror(
                    "設定エラー",
                    str(e)
                    if str(e)
                    else "1以上の整数を入力してください。",
                    parent=editor
                )

        tk.Button(
            editor,
            text="適用",
            command=apply,
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground="#5788cf",
            activeforeground="white",
            relief="flat",
            width=20,
            height=2,
            cursor="hand2"
        ).pack(
            pady=25
        )

    # =====================================================
    # Layer追加
    # =====================================================

    add_frame = tk.Frame(
        window,
        bg=BG
    )

    add_frame.pack(
        fill="x",
        padx=25,
        pady=5
    )

    tk.Label(
        add_frame,
        text="ADD",
        font=("Segoe UI", 9, "bold"),
        bg=BG,
        fg=SUBTEXT
    ).pack(
        side="left",
        padx=(0, 10)
    )

    def add_layer(layer_type):

        layers = config["model"]["layers"]

        if layer_type == "Conv2d":

            layers.append({
                "type": "Conv2d",
                "name": f"conv{len(layers) + 1}",
                "input_channel": 0,
                "output_channel": 8,
                "kernel_size": 3,
                "stride": 1
            })

        elif layer_type == "ReLU":

            layers.append({
                "type": "ReLU",
                "name": f"relu{len(layers) + 1}"
            })

        elif layer_type == "MaxPool2d":

            layers.append({
                "type": "MaxPool2d",
                "name": f"pooling{len(layers) + 1}",
                "kernel_size": 2,
                "padding": 0,
                "stride": 2
            })

        elif layer_type == "Flatten":

            layers.append({
                "type": "Flatten",
                "name": "flatten"
            })

        elif layer_type == "Linear":

            layers.append({
                "type": "Linear",
                "name": f"linear{len(layers) + 1}",
                "input_size": 0,
                "output_size": 3
            })

        refresh()

    for layer_type in [
        "Conv2d",
        "ReLU",
        "MaxPool2d",
        "Flatten",
        "Linear"
    ]:

        tk.Button(
            add_frame,
            text=layer_type,
            command=lambda t=layer_type: add_layer(t),
            bg=BUTTON,
            fg=TEXT,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT,
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            padx=3
        )

    # =====================================================
    # Learning設定
    # =====================================================

    learning_frame = tk.Frame(
        window,
        bg=PANEL,
        highlightbackground="#414141",
        highlightthickness=1
    )

    learning_frame.pack(
        fill="x",
        padx=25,
        pady=(5, 10)
    )

    tk.Label(
        learning_frame,
        text="LEARNING SETTINGS",
        font=("Segoe UI", 11, "bold"),
        bg=PANEL,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=15,
        pady=(12, 8)
    )

    # =====================================================
    # Optimizer
    # =====================================================

    optimizer_frame = tk.Frame(
        learning_frame,
        bg=PANEL
    )

    optimizer_frame.pack(
        fill="x",
        padx=15,
        pady=5
    )

    tk.Label(
        optimizer_frame,
        text="Optimizer",
        font=("Segoe UI", 10, "bold"),
        bg=PANEL,
        fg=SUBTEXT
    ).pack(
        side="left",
        padx=(0, 15)
    )

    tk.Label(
        optimizer_frame,
        text="Type",
        bg=PANEL,
        fg=SUBTEXT
    ).pack(
        side="left",
        padx=(0, 5)
    )

    optimizer_type_var = tk.StringVar(
        value=config["learning"]["optimizer"]["type"]
    )

    tk.Entry(
        optimizer_frame,
        textvariable=optimizer_type_var,
        width=18,
        bg=BLOCK,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    ).pack(
        side="left",
        padx=(0, 20)
    )

    tk.Label(
        optimizer_frame,
        text="Learning rate",
        bg=PANEL,
        fg=SUBTEXT
    ).pack(
        side="left",
        padx=(0, 5)
    )

    optimizer_rate_var = tk.StringVar(
        value=str(
            config["learning"]["optimizer"]["learning_rate"]
        )
    )

    tk.Entry(
        optimizer_frame,
        textvariable=optimizer_rate_var,
        width=12,
        justify="center",
        bg=BLOCK,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    ).pack(
        side="left"
    )

    # =====================================================
    # Loss
    # =====================================================

    loss_frame = tk.Frame(
        learning_frame,
        bg=PANEL
    )

    loss_frame.pack(
        fill="x",
        padx=15,
        pady=(5, 15)
    )

    tk.Label(
        loss_frame,
        text="Loss",
        font=("Segoe UI", 10, "bold"),
        bg=PANEL,
        fg=SUBTEXT
    ).pack(
        side="left",
        padx=(0, 15)
    )

    tk.Label(
        loss_frame,
        text="Type",
        bg=PANEL,
        fg=SUBTEXT
    ).pack(
        side="left",
        padx=(0, 5)
    )

    loss_type_var = tk.StringVar(
        value=config["learning"]["loss"]["type"]
    )

    tk.Entry(
        loss_frame,
        textvariable=loss_type_var,
        width=25,
        bg=BLOCK,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    ).pack(
        side="left"
    )

    # =====================================================
    # 保存
    # =====================================================

    def save():

        try:

            # -------------------------
            # Inputを取得
            # -------------------------

            for key, variable in input_vars.items():

                value = int(
                    variable.get()
                )

                if value <= 0:

                    raise ValueError(
                        f"input {key} は1以上にしてください。"
                    )

                config["model"]["input"][key] = value

            # -------------------------
            # Learning設定
            # -------------------------

            optimizer_type = (
                optimizer_type_var.get().strip()
            )

            if not optimizer_type:

                raise ValueError(
                    "OptimizerのTypeを入力してください。"
                )

            loss_type = (
                loss_type_var.get().strip()
            )

            if not loss_type:

                raise ValueError(
                    "LossのTypeを入力してください。"
                )

            try:

                learning_rate = float(
                    optimizer_rate_var.get()
                )

            except ValueError:

                raise ValueError(
                    "Learning rate は数値で入力してください。"
                )

            if learning_rate <= 0:

                raise ValueError(
                    "Learning rate は0より大きい値にしてください。"
                )

            config["learning"]["optimizer"]["type"] = (
                optimizer_type
            )

            config["learning"]["optimizer"]["learning_rate"] = (
                learning_rate
            )

            config["learning"]["loss"]["type"] = (
                loss_type
            )

            # -------------------------
            # CNN形状を再計算
            # -------------------------

            calculate_shapes(
                config
            )

            # -------------------------
            # YAML保存
            # -------------------------

            save_config(
                config
            )

            # -------------------------
            # 表示更新
            # -------------------------

            refresh()

            messagebox.showinfo(
                "保存完了",
                "CNN設定をCNN_dat.yamlへ保存しました。",
                parent=window
            )

        except ValueError as e:

            messagebox.showerror(
                "保存できません",
                str(e),
                parent=window
            )

    tk.Button(
        window,
        text="SAVE  /  CNN_dat.yaml",
        command=save,
        font=("Segoe UI", 11, "bold"),
        bg=ACCENT,
        fg="white",
        activebackground="#5788cf",
        activeforeground="white",
        relief="flat",
        height=2,
        cursor="hand2"
    ).pack(
        fill="x",
        padx=25,
        pady=(5, 20)
    )

    # =====================================================
    # 初期表示
    # =====================================================

    refresh()
