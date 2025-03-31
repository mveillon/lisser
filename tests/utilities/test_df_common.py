import math

from src.utilities.df_common import group_by_month, group_by_week
from src.read_data.column import Column
from src.models.day_counts import DayCounts

from tests.test_utils import sample_data


def test_group_by_month():
    data = sample_data()
    starts, partitions = group_by_month(data)

    assert len(starts) == DayCounts.months_per_year()
    assert len(partitions) == DayCounts.months_per_year()

    assert sum(map(lambda p: p.shape[0], partitions)) == data.shape[0]


def test_group_by_week():
    data = sample_data()
    starts, partitions = group_by_week(data)

    num_weeks = math.ceil((data[Column.DATE].max() - data[Column.DATE].min()).days / 7)

    assert len(starts) == num_weeks
    assert len(partitions) == num_weeks

    assert sum(map(lambda p: p.shape[0], partitions)) == data.shape[0]
