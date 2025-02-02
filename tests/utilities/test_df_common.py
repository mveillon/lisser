import math

from src.utilities.df_common import group_by_month, group_by_week
from src.utilities.column import Column

from tests.test_utils import sample_data


def test_group_by_month():
    data = sample_data()
    starts, partitions = group_by_month(data)

    num_months = math.ceil(
        (data[Column.DATE].max() - data[Column.DATE].min()).days / 30
    )

    assert len(starts) == num_months
    assert len(partitions) == num_months

    assert sum(map(lambda p: p.shape[0], partitions)) == data.shape[0]


def test_group_by_week():
    data = sample_data()
    starts, partitions = group_by_week(data)

    num_weeks = math.ceil((data[Column.DATE].max() - data[Column.DATE].min()).days / 7)

    assert len(starts) == num_weeks
    assert len(partitions) == num_weeks

    assert sum(map(lambda p: p.shape[0], partitions)) == data.shape[0]
