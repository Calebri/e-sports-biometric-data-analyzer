import pandas as pd
import matplotlib.pyplot as plt

import data_import
import data_process

DATA_PATH = "./data/esports_gaming_biometrics_250k.csv"


def process_win_loss(df: pd.DataFrame) -> None:
    PROC_CATEGORIES: list = [
        "Age",
        "Game_Genre",
        "PlayTime_Hours",
        "Sleep_Hours",
        "Energy_Drinks",
        "Screen_Brightness",
        "Blue_Light_Filter",
        "APM",
        "Reaction_Time_ms",
    ]

    for category in PROC_CATEGORIES:
        gdf: pd.DataFrame = data_process.win_loss_split(df, category)

        data_process.win_loss_chart(gdf, category, ["win_prop"], save=True)


def process_genre(df: pd.DataFrame) -> None:
    PROC_CATEGORIES: list[str] = [
        "Age",
        "PlayTime_Hours",
        "Sleep_Hours",
        "Energy_Drinks",
        "Screen_Brightness",
        "Heart_Rate_BPM",
        "APM",
        "Reaction_Time_ms",
    ]

    for category in PROC_CATEGORIES:
        statistic = "mean"

        gdf: pd.DataFrame = data_process.genre_split(df, category, statistic)

        data_process.genre_chart(gdf, statistic, save=True)


def main() -> None:
    df: pd.DataFrame = data_import.get_clean_data(DATA_PATH)

    process_win_loss(df)
    
    process_genre(df)

    print("Operation complete!")


if __name__ == "__main__":
    main()