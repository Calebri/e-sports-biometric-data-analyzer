import numpy as np
import pandas as pd
import pandas.testing as tm
import pytest

import data_import


@pytest.fixture
def unclean_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ID": [1,2,3,4],
            "SomeValue": [3.0, 2.0, np.nan, 5.0]
        }
    )


def test_clean_data(unclean_df):
    result: pd.DataFrame = data_import.clean_data(unclean_df)

    expected: pd.DataFrame = pd.DataFrame(
        {
            "ID": [1,2,4],
            "SomeValue": [3.0, 2.0, 5.0]
        },
        index=pd.Index([0, 1, 3], dtype='int64')
    )

    tm.assert_frame_equal(result, expected)
