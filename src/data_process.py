"""
Submodule for processing DataFrames into statistics and producing charts.
"""

import os

import pandas as pd
from pandas.api.typing import SeriesGroupBy
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np

CHART_OUT = "./charts"


def win_loss_split(
        df: pd.DataFrame,
        basis: str,
        round: float = 10.0
    ) -> pd.DataFrame:
    """
    Calculates the per-column win-loss statistics of a given DataFrame.
    Resulting DataFrame includes the following columns: `<basis>, Win, Loss, Win_Prop, Loss_Prop`.
    """

    # Container for the grouping basis.
    groupby_this: str | pd.Series

    # Use alternative grouping algorithm for float columns, or integer columns with many unique values.
    if pd.api.types.is_float_dtype(df[basis])\
        or (pd.api.types.is_integer_dtype(df[basis]) and df.shape[0] > 10):
        # Cut value-space into 10 columns. Similar to histogram.
        series: pd.Series = df[basis]
        groupby_this = pd.cut(series, 10)
    else:
        # Default grouping for objects or small-count integers.
        groupby_this = basis

    # Grouped Data Frame.
    gdf: pd.DataFrame = df.groupby(groupby_this)["Match_Outcome"].value_counts().unstack()

    # Turn groups into indexed rows.
    gdf = gdf.reset_index()

    # 0-count entires calculate to N/A. We replace them with 0.
    gdf = gdf.fillna(0)

    # Total count series used for calculating proportional w/l columns.
    age_total: pd.Series = gdf["Win"] + gdf["Loss"]

    # Calculate proportional wins and losses for easier comparison.
    gdf["Win_Prop"] = gdf["Win"] / age_total
    gdf["Loss_Prop"] = gdf["Loss"] / age_total

    return gdf


def win_loss_chart(
        df: pd.DataFrame,
        basis: str,
        plot: list[str],
        save: bool = False,
        show: bool = False
    ) -> tuple[Figure, Axes]:
    """
    Creates a new figure with MatPlotLib representing a DataFrame from win_loss_split().
    What exactly gets plotted is decided by the `plot` parameter.
    Options are available for showing this plot immediately or saving it to a file.
    """

    # Plot init
    fig, ax = plt.subplots(layout="constrained")

    # 50% line
    ax.axhline(0.5, color="yellow", linestyle="--", label="50%")

    # Plotting Data
    if "win_prop" in plot:
        df.plot(x=basis, y="Win_Prop", kind="bar", ax=ax, label="Win %", color="#0BC60B")
        ax.axhline(df["Win_Prop"].mean(), color="#0BC60B", linestyle="--", label="Stratified Mean")
    if "loss_prop" in plot:
        df.plot(x=basis, y="Loss_Prop", kind="bar", ax=ax, label="Win %", color="#BB000C")
        ax.axhline(df["Loss_Prop"].mean(), color="#BB000C", linestyle="--", label="Stratified Mean")

    # Axes Params
    ax.set_ylim(0, 1)
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=270, ha="center") # type: ignore
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))

    # Display legend
    ax.legend()

    # Save or show plot
    plot_out(fig, (basis.lower() + "_win_loss") if save else None, show)

    return fig, ax


def genre_split(
        df: pd.DataFrame,
        statcol: str,
        method: str = "value_counts"
    ) -> pd.DataFrame:
    """
    Groups a DataFrame by "Game_Genre", then calculates a given statistic for a given column.
    """

    # Group statcol by Game_Genre.
    grouped: SeriesGroupBy = df.groupby("Game_Genre")[statcol]

    # Calculate statistic based on passed parameter. Return value must be a DataFrame.
    match method:
        case "value_counts":
            return grouped.value_counts().unstack()
        case "mean":
            return grouped.mean().to_frame()
        case _:
            raise ValueError("Unknown processing method: " + method)


def genre_chart(
        df: pd.DataFrame,
        statistic: str,
        save: bool = False,
        show: bool = False
    ) -> tuple[Figure, Axes]:

    # Retrieve statcol.
    statcol: str = df.columns[0]

    # This is used where statcol needs to appear on the chart.
    statcol_display: str = statcol.replace("_", " ").title()

    # Statistic Calculation
    mean: float = df[statcol].mean()
    std: float = df[statcol].std()
    margin: float = std * 3

    # Figure init
    fig, ax = plt.subplots()

    # Plot Bars
    df.plot(kind="bar", color="purple", ax=ax, label=statcol_display)

    # Chart Parameters and Labels
    ax.set_ylim(mean - margin, mean + margin)
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=0, ha="center") # type: ignore
    ax.set_title(statistic.title() + " " + statcol_display + " by Game Genre")
    ax.set_xlabel(statcol_display)

    # Horizontal Lines for Mean and StDev
    ax.axhline(mean, color="blue", linestyle="-", label="Mean")
    ax.axhline(mean - std, color="yellow", linestyle="--", label="Standard Deviation")
    ax.axhline(mean + std, color="yellow", linestyle="--")

    # Init legend.
    ax.legend()

    # Save/Show plot.
    plot_out(fig, (statcol.lower() + "_by_genre") if save else None, show)

    return fig, ax


def plot_out(
        fig: Figure,
        savename: str | None = None,
        show: bool = False
    ) -> None:
    """
    Handles saving and showing plots. Pass a savename to save the plot to a file.
    Pass show=True to show the graph on the screen.
    """

    # Save file
    if savename != None:
        try:
            # Make sure CHART_OUT exists.
            os.makedirs(CHART_OUT, exist_ok=True)

            # Save figure to file.
            save_path = CHART_OUT + "/" + savename + ".png"
            fig.savefig(save_path)

            print("Successfully saved chart to: " + save_path)
        except Exception as e:
            print("Failed to save chart: " + str(e))

    # Halt thread and show
    if show:
        plt.show(block=True)