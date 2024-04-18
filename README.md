PYBENGALI

pybengali is a python3 package for Bengali DateTime and Bengali numeric number conversation and many more. This package can be used with any python framework like Django, Flask, FastAPI, and others. pybengali is OS Independent, It can be used on any operating system Linux/Unix, Mac OS and Windows.
Available Features

    Features available in pybengali:
    List of Bengali Numbers
    List of Bengali Months
    List of Bengali Weekdays
    List of Bengali Seasons
    Bengali Year
    Bengali Weekday
    Bengali Date
    Bengali Today
    Bengali Tomorrow
    Bengali Yesterday
    Bengali Past Date
    Bengali Future Date
    Bengali Timesince
    Convert English Month Name to Bengali
    Convert English Numeric Number to Bengali Numeric Number

Installation

$ pip install pybengali

Usage

Get Bengali Today:

import pybengali
today = pybengali.today()
print(today)
# Output: {'date': '১৯', 'month': 'আশ্বিন', 'year': '১৪২৮', 'season': 'শরৎ', 'weekday': 'সোমবার'}

today = pybengali.today(day="04", month="10", year="2022")
print(today)
# Output: {'date': '১৯', 'month': 'আশ্বিন', 'year': '১৪২৯', 'season': 'শরৎ', 'weekday': 'মঙ্গলবার'}

Get Bengali Tomorrow and Yesterday:

import pybengali
tomorrow = pybengali.tomorrow()
print(tomorrow)
# Output: {'date': '২০', 'month': 'আশ্বিন', 'year': '১৪২৮', 'season': 'শরৎ', 'weekday': 'মঙ্গলবার'}

yesterday = pybengali.yesterday(day="04", month="10", year="2022")
print(yesterday)
# Output: {'date': '১৮', 'month': 'আশ্বিন', 'year': '১৪২৮', 'season': 'শরৎ', 'weekday': 'রবিবার'}

Get Bengali Timesince:

import pybengali
timesince = pybengali.timesince(day="04",month="10",year="2019")
print(timesince)
# Output: ২ বছর আগে

Get Bengali Past or Future Date With Number of Days To Go Back or Froward :

import pybengali
# Past Date
past_date = pybengali.past_date('2')
print(past_date)
# Output: {'date': '১৭', 'month': 'আশ্বিন', 'year': '১৪২৮', 'season': 'শরৎ', 'weekday': 'শনিবার'}

# Future Date
future_date = pybengali.future_date('2')
print(future_date)
# Output: {'date': '২১', 'month': 'আশ্বিন', 'year': '১৪২৮', 'season': 'শরৎ', 'weekday': 'বুধবার'}
