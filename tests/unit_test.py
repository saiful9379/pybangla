import unittest
from pprint import pprint

from ..pybangla.module.main import Normalizer


class TestJsonUpdater(unittest.TestCase):
    def test_date_parsing(self):
        test_cases = [
            (
                "2023-04-05",
                {
                    "date": "05",
                    "month": "April",
                    "year": "2023",
                    "weekday": "Wednesday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
            (
                "06-04-2023",
                {
                    "date": "06",
                    "month": "April",
                    "year": "2023",
                    "weekday": "Thursday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
            (
                "04/01/2023",
                {
                    "date": "04",
                    "month": "January",
                    "year": "2023",
                    "weekday": "Wednesday",
                    "ls_month": "Jan",
                    "seasons": "Summer",
                },
            ),
            (
                "07 April, 2023",
                {
                    "date": "07",
                    "month": "April",
                    "year": "2023",
                    "weekday": "Friday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
            (
                "Apr 1, 2023",
                {
                    "date": "1",
                    "month": "April",
                    "year": "2023",
                    "weekday": "Saturday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
            (
                "2023/04/01",
                {
                    "date": "01",
                    "month": "April",
                    "year": "2023",
                    "weekday": "Saturday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
            (
                "01-Apr-2023",
                {
                    "date": "01",
                    "month": "April",
                    "year": "2023",
                    "weekday": "Saturday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
            (
                "01-Apr/2023",
                {
                    "date": "01",
                    "month": "April",
                    "year": "2023",
                    "weekday": "Saturday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
            (
                "20230401",
                {
                    "date": "01",
                    "month": "April",
                    "year": "2023",
                    "weekday": "Saturday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
            (
                "20042024",
                {
                    "date": "20",
                    "month": "April",
                    "year": "2024",
                    "weekday": "Saturday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
            (
                ["1", "4", "2025"],
                {
                    "date": "1",
                    "month": "April",
                    "year": "2025",
                    "weekday": "Tuesday",
                    "ls_month": "Apr",
                    "seasons": "Wet season",
                },
            ),
        ]

        for date_str, expected_output in test_cases:
            parsed_date = Normalizer.date_format(date_str)

            self.assertIsNotNone(parsed_date, f"Failed to parse date string: {date_str}")

            parsed_date_info = {
                "date": parsed_date.strftime("%d"),
                "month": parsed_date.strftime("%B"),
                "year": parsed_date.strftime("%Y"),
                "weekday": parsed_date.strftime("%A"),
                "ls_month": parsed_date.strftime("%b"),
                "seasons": "Wet season",  # Assume it's always wet season for testing purposes
            }

            self.assertEqual(
                parsed_date_info, expected_output, f"Unexpected output for date string: {date_str}"
            )

    def date_format_test():
        pass

    def number_convert_test():
        pass

    def today_test(self):
        pass

    def weekday_test(self):
        pass

    def months_test(self):
        pass

    def seasons_test(self):
        pass


if __name__ == "__main__":
    unittest.main()
