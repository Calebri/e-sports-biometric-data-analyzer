import pandas as pd
import pandas.testing as tm
import pytest

import data_process


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "Classification": [1,1,2,2,3],
        "Match_Outcome": ["Win","Loss","Win","Win","Loss"],
        "Game_Genre": ["A","A","B","A","C"]
    })


def test_win_loss_split(sample_df) -> None:
    result: pd.DataFrame = data_process.win_loss_split(sample_df, "Classification")

    expected = pd.DataFrame(
        {
            "Classification": [1,2,3],
            "Loss": [1.0,0.0,1.0],
            "Win": [1.0,2.0,0.0],
            "Win_Prop": [0.5,1.0,0.0],
            "Loss_Prop": [0.5,0.0,1.0],
        }
    )
    expected.columns.name = "Match_Outcome"

    tm.assert_frame_equal(result, expected)


def test_win_loss_mutation(sample_df) -> None:
    df_copy: pd.DataFrame = sample_df.copy()

    gdf: pd.DataFrame = data_process.win_loss_split(df_copy, "Classification")

    tm.assert_frame_equal(df_copy, sample_df)

    gdf_copy: pd.DataFrame = gdf.copy()

    data_process.win_loss_chart(gdf_copy, "Classification", [])

    tm.assert_frame_equal(gdf_copy, gdf)


def test_genre_split_mutation(sample_df) -> None:
    df_copy: pd.DataFrame = sample_df.copy()

    data_process.genre_split(df_copy, "Classification")

    tm.assert_frame_equal(df_copy, sample_df)
