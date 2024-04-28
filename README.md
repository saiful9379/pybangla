# PYBENGALA



Project description
PYBANGLA

PYBANGLA is a python3 package for Bengali DateTime and Bengali numeric number conversation and many more. This package can be used with any python framework like Django, Flask, FastAPI, and others. PYBANGLA is OS Independent, It can be used on any operating system Linux/Unix, Mac OS and Windows.
Available Features

    Features available in PYBANGLA:
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

```
pip install pybangala
```


1. Formating Date

This module support format date English as well as Bangla. those format are support of the module.

Input Format:
```
"2023-04-05",  "06-04-2023", "04/01/2023", "07 April, 2023", "Apr 1, 2023",  "2023/04/01", "01-Apr-2023", "01-Apr/2023",  "20230401",  "20042024", ["1", "4", "2025"]
```
output :

Bangla Format:

```
{'date': '০৪', 'month': 'জানুয়ারি', 'year': '২০২৩', 'weekday': 'বুধবার', 'ls_month': 'বৈশাখ', 'seasons': 'গ্রীষ্ম'}
```

English Format:
```
{'date': '04', 'month': 'January', 'year': '2023', 'weekday': 'Wednesday', 'ls_month': 'Jan', 'seasons': 'Summer'}
```

# Usage:
Supported Date formate

## 1. Date Format:

```
import pybangla
dt = pybangla.DateTranslator()

date = dt.date_format("01-Apr/2023", language="bn")
print(f"{date}")
# Output: 
{'date': '০১', 'month': 'এপ্রিল', 'year': '২০২৩', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```

```
import pybangla
dt = pybangla.DateTranslator()
en_date = dt.date_format("01-Apr/2023", language="en")
print(f"{en_date}")

# Output :
{'date': '01', 'month': 'April', 'year': '2023', 'weekday': 'Saturday', 'ls_month': 'Apr', 'seasons': 'Wet season'}
```

# 2. Bangla Today:
```
import pybangla
dt = pybangla.DateTranslator()
today = dt.today()
print(today)

# Output: 
{'date': '১৯', 'month': 'এপ্রিল', 'year': '২০২৪', 'weekday': 'শুক্রবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```

# 3. weekdays

```

import pybangla
dt = pybangla.DateTranslator()
weekdays = dt.weekdays()
print(weekdays)

# Output: 
{'date': '১৯', 'month': 'এপ্রিল', 'year': '২০২৪', 'weekday': 'শুক্রবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}


```


# 4. seasons

```

import pybangla
dt = pybangla.DateTranslator()
seasons = dt.seasons()
print(seasons)

# Output: 
{'date': '১৯', 'month': 'এপ্রিল', 'year': '২০২৪', 'weekday': 'শুক্রবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}


```

# 4. months

```
import pybangla
dt = pybangla.DateTranslator()
months = dt.months()
print(months)

# Output: 
{'date': '১৯', 'month': 'এপ্রিল', 'year': '২০২৪', 'weekday': 'শুক্রবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```
# 5. number_convert

```
import pybangla
dt = pybangla.DateTranslator()
number = dt.number_convert("12345", language="bn")
# Output:

```


