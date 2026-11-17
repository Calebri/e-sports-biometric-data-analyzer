import pandas as pd
import matplotlib.pyplot as plt

import data_import
import data_process

DATA_PATH = "./data/esports_gaming_biometrics_250k.csv"

def main() -> None:
    df: pd.DataFrame = data_import.get_clean_data(DATA_PATH)


    for category in ["Age", "Game_Genre", "Screen_Brightness", "Blue_Light_Filter"]:
        sdf: pd.DataFrame = data_process.win_loss_split(df, category)

        data_process.win_loss_chart(sdf, category, ["win_prop"], save=True)

    print(data_process.genre_split(df, "Age", "mean").head(10))
    

    print("Operation complete!")


if __name__ == "__main__":
    main()