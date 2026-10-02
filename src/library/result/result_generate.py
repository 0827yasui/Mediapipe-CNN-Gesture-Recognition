from pathlib import Path
import shutil
import pandas as pd


class Result_generate():
    def __init__(self, result_name):
        self.result_dir = Path("result") / result_name

        self.log_dir = self.result_dir / "log"
        self.config_dir = self.result_dir / "config"
        self.data_dir = self.result_dir / "data"

    def generate(self):
        self.generate_config()
        self.generate_data()

    def generate_config(self):
        config_dir = Path("config")

        for file in self.config_dir.iterdir():
            if file.is_file():
                shutil.copy2(
                    file,
                    config_dir / file.name
                )

    def generate_data(self):
        data_dir = Path("data")

        shutil.copytree(
            self.data_dir,
            data_dir,
            dirs_exist_ok=True
        )

    @classmethod
    def get_best_result(cls):
        result_dir = Path("result")

        best_name = None
        best_acc = -1.0

        for result in result_dir.iterdir():
            if not result.is_dir():
                continue

            accuracy_file = result / "log" / "accuracy.csv"

            if not accuracy_file.exists():
                continue

            df = pd.read_csv(accuracy_file)

            if df.empty or "acc" not in df.columns:
                continue

            acc = df["acc"].max()

            if acc > best_acc:
                best_acc = acc
                best_name = result.name

        if best_name is None:
            raise FileNotFoundError(
                "有効なaccuracy.csvが見つかりません。"
            )

        return cls(best_name)