from pathlib import Path
from datetime import datetime
import pandas as pd
import shutil

class Result():
    def __init__(self):

        result_dir = Path("result")

        time = datetime.now().strftime("%Y%m%d_%H%M")

        self.save_dir = result_dir / time

        self.log_dir = self.save_dir / "log"
        self.config_dir = self.save_dir / "config"
        self.data_dir = self.save_dir / "data"

        self.log_dir.mkdir(
            parents=True,
            exist_ok=False
        )

        self.config_dir.mkdir(
            exist_ok=False
        )

        self.data_dir.mkdir(
            exist_ok=False
        )

    def save_accuracy(self, acc_list):

        df = pd.DataFrame(acc_list)
        df.to_csv(
            self.log_dir / "accuracy.csv",
            index=False
        )

    def save_config(self):

        config_dir = Path("config")
        for file in config_dir.iterdir():
            if file.is_file():
                shutil.copy2(
                    file,
                   self.config_dir / file.name
                )

    def save_data(self):

        data_dir = Path("data")

        shutil.copytree(
            data_dir,
            self.data_dir,
            dirs_exist_ok=True
        )