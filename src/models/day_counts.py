from src.models.paths import Paths
import calendar


class DayCounts:
    @staticmethod
    def days_per_year() -> int:
        """
        Returns exactly how many days were in this year.

        Parameters:
            None

        Returns:
            days (int): how many days were in this year
        """
        if calendar.isleap(Paths.get_year()):
            return 366

        return 365

    @staticmethod
    def months_per_year() -> int:
        """
        Returns how many months there are in a year.

        Parameters:
            None

        Returns:
            months (int): how many months per year there are
        """
        return 12

    @staticmethod
    def weeks_per_year() -> float:
        """
        Returns exactly how many weeks there are in a year.

        Parameters:
            None

        Returns:
            weeks (int): how many weeks there are in a year
        """
        return DayCounts.days_per_year() / DayCounts.days_per_week()

    @staticmethod
    def days_per_week() -> int:
        """
        Returns how many days are in a week.

        Parameters:
            None

        Returns:
            days (int): how many days are in a week
        """
        return 7

    @staticmethod
    def days_per_month() -> float:
        """
        Returns exactly how many days are in an average month.

        Parameters:
            None

        Returns:
            days (float): average number of days per month
        """
        return DayCounts.days_per_year() / DayCounts.months_per_year()

    @staticmethod
    def weeks_per_month() -> float:
        """
        Returns how many weeks are in the average month.

        Parameters:
            None

        Returns:
            weeks (float): average weeks per month
        """
        return DayCounts.days_per_month() / DayCounts.days_per_week()
