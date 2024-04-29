# Project Discription

PYBANGLA is a python3 package for Bengala Number, DateTime and Text Normalizer. This package can be used Normalize the text number and date (ex: number to text vice versa). This framework  also can be used Django, Flask, FastAPI, and others. PYBANGLA module supported operating system Linux/Unix, Mac OS and Windows.
Available Features

Features available in PYBANGLA:

1. Date Format
2. Text Normalization
3. Number Converstion
4. Months, Weekdays, Seasons


# Installation

The easiest way to install pybangla is to use pip:

```
pip install pybangala
```

# Usage

## 1. Date Format
Supported Date Format:

```
"2023-04-05",  "06-04-2023", "04/01/2023", "07 April, 2023", "Apr 1, 2023", "2023/04/01", "01-Apr-2023", "01-Apr/2023",  "20230401",  "20042024", ["1", "4", "2025"]
```
output :


```
Bangla : 
{'date': '০৪', 'month': 'জানুয়ারি', 'year': '২০২৩', 'weekday': 'বুধবার', 'ls_month': 'বৈশাখ', 'seasons': 'গ্রীষ্ম'}

or
English:

{'date': '04', 'month': 'January', 'year': '2023', 'weekday': 'Wednesday', 'ls_month': 'Jan', 'seasons': 'Summer'}
```
## Command line::

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


