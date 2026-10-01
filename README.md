# MediaPipe × CNN 手認識システム

カメラに映した手の形を認識し、**グー・チョキ・パー**の3種類を判定する画像認識システムです。

MediaPipeで手のランドマークを取得し、その情報を画像として処理したうえでCNNによる分類を行います。

---

## 📌 できること

* カメラから手の映像を取得
* 手のランドマークを検出
* グー・チョキ・パーの画像データを作成
* 作成したデータを使ってCNNを学習
* 学習したモデルでリアルタイムに手の形を認識
* 認識結果と信頼度を画面に表示

---

## 💻 動作環境

以下の環境を想定しています。

* Python 3.x
* OpenCV
* MediaPipe
* PyTorch
* NumPy
* PyYAML

カメラを使用するため、PCにカメラを接続してください。

---

## 📁 プロジェクト構成

利用者が主に扱う部分は以下です。

```text
test0.7/
├─ config/
│  ├─ CNN_dat.yaml
│  ├─ camera_dat.yaml
│  ├─ frame_dat.yaml
│  ├─ learning.yaml
│  └─ mediapipe_dat.yaml
│
├─ data/
│  ├─ train_data/
│  │  ├─ images/
│  │  └─ labels.csv
│  │
│  └─ test_data/
│     ├─ images/
│     └─ labels.csv
│
├─ model/
│  ├─ cnn.pth
│  ├─ hand_landmarker.task
│  └─ face_landmarker.task
│
└─ src/
   └─ ...
```

`src` 以下はシステム本体です。

通常の利用では、内部のプログラムを直接変更する必要はありません。

---

# 🚀 使い方

基本的な流れは次の通りです。

```text
データ作成
   ↓
学習
   ↓
テスト
   ↓
リアルタイム認識
```

## 1. 学習データを作成する

以下を実行します。

```bash
python -m src.main.data_train_make_main
```

カメラの映像が表示されます。

画面を確認しながら手の形を作り、キーを押して画像を保存します。

| キー    | ラベル |
| ----- | --- |
| `g`   | グー  |
| `c`   | チョキ |
| `p`   | パー  |
| `ESC` | 終了  |

保存された画像は学習用データとして使用されます。

---

## 2. テストデータを作成する

テスト用の画像を作成する場合は、

```bash
python -m src.main.data_test_make_main
```

を実行します。

操作方法は学習データの作成と同じです。

テストデータは、学習に使用せず、学習したモデルの確認に使用します。

---

## 3. 学習する

学習を実行する場合は、

```bash
python -m src.main.learning_main
```

を実行します。

学習が終了すると、学習したCNNモデルが保存されます。

---

## 4. リアルタイム認識する

学習済みモデルを使用してカメラから手の形を認識するには、

```bash
python -m src.main.interface_main
```

を実行します。

カメラに手を映すと、認識結果が表示されます。

現在の認識対象は以下の3種類です。

```text
Guu   → グー
Choki → チョキ
Paa   → パー
```

認識結果には信頼度も表示されます。

`ESC` を押すと終了します。

---

# ⚙️ 設定

動作に関する設定は `config` フォルダにまとめられています。

### カメラ

`config/camera_dat.yaml`

使用するカメラを設定できます。

### 画像処理

`config/frame_dat.yaml`

カメラ画像の向きなどを設定できます。

### MediaPipe

`config/mediapipe_dat.yaml`

手の検出条件などを設定できます。

### 学習

`config/learning.yaml`

学習回数、バッチサイズ、シャッフルなどを設定できます。

例：

```yaml
train:
  epoch: 3
  batch: 100
  shuffle: True
```

テストについても同様に設定できます。

### CNN

`config/CNN_dat.yaml`

CNNの入力サイズやネットワーク構成、学習方法などを設定できます。

---

# 🗂️ データについて

データは以下の2種類に分けて管理します。

### 学習データ

```text
data/train_data/
```

CNNの学習に使用します。

### テストデータ

```text
data/test_data/
```

学習したモデルの評価に使用します。

それぞれのデータには画像とラベル情報が含まれます。

```text
images/
labels.csv
```

`labels.csv` には画像と、それに対応する分類番号が記録されています。

分類番号は次のように対応しています。

| 番号 | 手の形 |
| -: | --- |
|  0 | グー  |
|  1 | チョキ |
|  2 | パー  |

---

# 🔄 基本的な利用手順

初めて使用する場合は、次の順番で実行してください。

### ① 学習データを用意

```bash
python -m src.main.data_train_make_main
```

### ② テストデータを用意

```bash
python -m src.main.data_test_make_main
```

### ③ 学習

```bash
python -m src.main.learning_main
```

### ④ 認識

```bash
python -m src.main.interface_main
```

---

# ⚠️ 注意事項

* カメラが正常に使用できる状態で実行してください。
* 学習データとテストデータは、用途を分けて用意してください。
* 手の形だけでなく、照明・背景・手の位置なども認識結果に影響する場合があります。
* 学習データを変更した場合は、必要に応じて再学習してください。
* `model` フォルダに必要なモデルファイルが存在することを確認してください。

---

# 🎯 現在の認識対象

現在は、

**グー / チョキ / パー**

の3クラスを対象としています。

将来的に認識対象を増やす場合は、データと設定を追加することで拡張できます。
