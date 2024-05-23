# 3. Date Format

It supports converting different formats of Bangla date to English date.

```py

import pybangla
nrml = pybangla.Normalizer()
date = "০১-এপ্রিল/২০২৩"
date = nrml.date_format(date, language="bn")
print(date)
#output:


{'date': '০১', 'month': '৪', 'year': '২০২৩', 'txt_date': 'এক', 'txt_month': 'এপ্রিল', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```



```py
date = nrml.date_format("সেপ্টেম্বর ০৫ ২০২৩", language="bn")

#output

{'date': '০৫', 'month': '৯', 'year': '২০২৩', 'txt_date': 'পাঁচ', 'txt_month': 'সেপ্টেম্বর', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'পৌষ', 'seasons': 'শীত'}


```

```py
date = nrml.date_format("20230401", language="bn")
print(date)
#output
{'date': '০১', 'month': '০৪', 'year': '২০২৩', 'txt_date': 'এক', 'txt_month': 'এপ্রিল', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}

```


```py

#input ex. ['dd', "mm", "yyyy"]
date = nrml.date_format(["1", "4", "2025"], language="bn")

print(date)

#output

{'date': '১', 'month': '৪', 'year': '২০২৫', 'txt_date': 'এক', 'txt_month': 'এপ্রিল', 'txt_year': 'দুই হাজার পঁচিশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}


```



Supported Date Format:

```py
  "০১-এপ্রিল/২০২৩",
  "১ এপ্রিল ২০২৩" 
  "2023-04-05",  
  "06-04-2023", 
  "04/01/2023",  
  "07 April, 2023", 
  "Apr 1, 2023",  
  "2023/04/01", 
  "01-Apr-2023", 
  "01-Apr/2023",  
  "20230401",  
  "20042024",
  ["1", "4", "2025"]
```
output :


```
Bangla : 
{'date': '০৪', 'month': 'জানুয়ারি', 'year': '২০২৩', 'weekday': 'বুধবার', 'ls_month': 'বৈশাখ', 'seasons': 'গ্রীষ্ম'}

or
English:

{'date': '04', 'month': 'January', 'year': '2023', 'weekday': 'Wednesday', 'ls_month': 'Jan', 'seasons': 'Summer'}
```
```py
import pybangla
nrml = pybangla.Normalizer()

date = dt.date_format("01-Apr/2023", language="bn")
print(f"{date}")
# Output: 
{'date': '০১', 'month': '৪', 'year': '২০২৩', 'txt_date': 'এক', 'txt_month': 'এপ্রিল', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}

```

```py
import pybangla
nrml = pybangla.Normalizer()
en_date = dt.date_format("01-Apr/2023", language="en")
print(f"{en_date}")

# Output :
{'date': '01', 'month': '4', 'year': '2023', 'txt_date': 'one', 'txt_month': 'april', 'txt_year': 'twenty century twenty-three', 'weekday': 'saturday', 'ls_month': 'apr', 'seasons': 'wet season'}

```

## Date extraction

```py
Rule based Date Extraction
import pybangla
nrml = pybangla.Normalizer()

text = "সম্মেলনটি সেপ্টেম্বর ০৫ ২০২৩ তারিখে নির্ধারিত করা হয়েছে. এপ্রিল ২০২৩"
dates = nrml.date_extraction(text)

#output:

[
    {'date': '০৫', 'month': '৯', 'year': '২০২৩', 'txt_date': 'পাঁচ', 'txt_month': 'সেপ্টেম্বর', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'পৌষ', 'seasons': 'শীত'}, 

{'date': '১৬', 'month': '৫', 'year': '২০২৪', 'txt_date': 'ষোল', 'txt_month': 'মে', 'txt_year': 'দুই হাজার চব্বিশ', 'weekday': 'বৃহস্পতিবার', 'ls_month': 'ভাদ্র', 'seasons': 'শরৎ'}
]


```