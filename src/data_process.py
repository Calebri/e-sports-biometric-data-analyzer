import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.figure import Figure
from matplotlib.axes import Axes

CHART_OUT = "./charts"

def win_loss_split(df: pd.DataFrame, basis: list[str]) -> pd.DataFrame:
    """
    Calculates the per-column win-loss statistics of a given DataFrame.
    Resulting DataFrame includes the following columns: `<basis>, Win, Loss, Win_Prop, Loss_Prop`.
    """

    gdf: pd.DataFrame = df.groupby(basis)["Match_Outcome"].value_counts().unstack()

    gdf.reset_index(inplace=True)

    age_total: pd.Series = gdf["Win"] + gdf["Loss"]

    gdf["Win_Prop"] = gdf["Win"] / age_total
    gdf["Loss_Prop"] = gdf["Loss"] / age_total

    return gdf


def win_loss_chart(
        df: pd.DataFrame,
        basis: list[str],
        plot: list[str],
        save: bool | None = False,
        show: bool | None = False
    ) -> tuple[Figure, Axes]:
    """
    Creates a new figure with MatPlotLib representing a DataFrame from win_loss_split().
    What exactly gets plotted is decided by the `plot` parameter.
    Options are available for showing this plot immediately or saving it to a file.
    """

    fig, ax = plt.subplots()

    # 50% line
    ax.axhline(0.5, color="yellow", linestyle="--", label="50%")

    # Plotting Data
    if "win_prop" in plot:
        df.plot(x=basis[0], y="Win_Prop", kind="bar", ax=ax, label="Win %", color="#0BC60B")
        ax.axhline(df["Win_Prop"].mean(), color="#0BC60B", linestyle="--", label="Stratified Mean")
    if "loss_prop" in plot:
        df.plot(x=basis[0], y="Loss_Prop", kind="bar", ax=ax, label="Win %", color="#BB000C")
        ax.axhline(df["Loss_Prop"].mean(), color="#BB000C", linestyle="--", label="Stratified Mean")

    # Axes Params
    ax.set_ylim(0, 1)
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=0, ha="center") # type: ignore
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))

    ax.legend()

    # Save file
    if save:
        try:
            # Make sure CHART_OUT exists.
            os.makedirs(CHART_OUT, exist_ok=True)

            # Save figure to file.
            save_path = CHART_OUT + "/" + basis[0] + ".png"
            plt.savefig(save_path)

            print("Successfully saved chart to: " + save_path)
        except Exception as e:
            print("Failed to save chart: " + str(e))

    # Halt thread and show
    if show:
        plt.show(block=True)

    return fig, ax