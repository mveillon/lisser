from datetime import date
import math

from src.utilities.helpers import get_months, get_weeks, time_filter
from src.utilities.column import Column

from tests.test_utils import sample_data


def test_get_weeks():
    start = date(2024, 1, 1)
    end = date(2024, 5, 1)

    weeks = get_weeks(start, end)

    assert min(weeks) >= start
    assert max(weeks) <= end

    assert len(weeks) == math.ceil((end - start).days / 7)

    for i, dtm in enumerate(weeks):
        if i == len(weeks) - 2:
            break

        assert (weeks[i + 1] - dtm).days == 7


def test_get_months():
    start = date(2024, 1, 1)
    end = date(2024, 5, 15)

    months = get_months(start, end)

    assert min(months) >= start
    assert max(months) <= end

    assert len(months) == math.ceil((end - start).days / 30)

    for i, dtm in enumerate(months):
        if i == len(months) - 2:
            break

        assert dtm.day == months[i + 1].day


def test_time_filter():
    data = sample_data()

    fmt = "%m/%d/%Y"
    start = date(2024, 1, 2)
    end = date(2024, 1, 30)

    filt = time_filter(data, start.strftime(fmt), end.strftime(fmt))

    assert filt[Column.DATE.value].min().date() >= start
    assert filt[Column.DATE.value].max().date() <= end
