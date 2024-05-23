

# Today, Months, Weekdays, Seasons

It converts Bangla (today, months, weekdays, and seasons) to English and English to Bangla, and vice versa, in a pair format. This is like static conversion. so if it need you can checkout.

# Uses of Day, Months and Weeks and Seasons

### 1. Today:

```py
import pybangla
nrml = pybangla.Normalizer()
today = nrml.today()
print(today)

# Output: 
{'date': '৩০', 'month': 'এপ্রিল', 'year': '২০২৪', 'txt_date': 'ত্রিশ', 'txt_year': 'দুই হাজার চব্বিশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```

```py
today= nrml.today(language="bn")
print(today)
# output:
{'date': '৩০', 'month': 'এপ্রিল', 'year': '২০২৪', 'txt_date': 'ত্রিশ', 'txt_year': 'দুই হাজার চব্বিশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```

```py
today= nrml.today(language="bn")
print(today)
#output:
{'date': '30', 'month': 'april', 'year': '2024', 'txt_date': 'thirty', 'txt_year': 'twenty century twenty-four', 'weekday': 'tuesday', 'ls_month': 'apr', 'seasons': 'wet season'}
```


### 2. Months

```py
import pybangla
nrml = pybangla.Normalizer()
month = nrml.months()
print(month)


# Output: 
{
    'bn': ['জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন', 'জুলাই', 'আগস্ট', 'সেপ্টেম্বর', 'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর'], 'bn_name': ['বৈশাখ', 'জ্যৈষ্ঠ', 'আষাঢ়', 'শ্রাবণ', 'ভাদ্র', 'আশ্বিন', 'কার্তিক', 'অগ্রহায়ণ', 'পৌষ', 'মাঘ', 'ফাল্গুন', 'চৈত্র'], 

    'en': ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
}
```


```py
month = nrml.months(month="মার্চ")
print(month)

#output:
{'মার্চ': 'march', 'bangla': 'আষাঢ়'}
```
```py
month = nrml.months(month="march")
print(month)

# output:
{'march': 'মার্চ', 'bangla': 'আষাঢ়'}

```

### 3. Weekdays

```py
import pybangla
nrml = pybangla.Normalizer()
weekdays = nrml.weekdays()

print(weekdays)

# Output: 
{
    'bn': ['সোমবার', 'মঙ্গলবার', 'বুধবার', 'বৃহস্পতিবার', 'শুক্রবার', 'শনিবার', 'রবিবার'], 
    'en': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
}
```

```py
weekdays = nrml.weekdays(language="bn")
print(weekdays)
# Output:
{
    'bn': ['সোমবার', 'মঙ্গলবার', 'বুধবার', 'বৃহস্পতিবার', 'শুক্রবার', 'শনিবার', 'রবিবার']
}

```

```py
weekdays = nrml.weekdays(language="en")
print(weekdays)
# Output:
{
    'en': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
}
```

```py
weekdays = nrml.weekdays(day = "সোমবার")
print(weekdays)
#output:
{'সোমবার': 'monday'}
```

```py
weekdays = nrml.weekdays(day = "Monday")
print(weekdays)
#output:
{'monday': 'সোমবার'}
```


### 4. Seasons

```py
import pybangla
nrml = pybangla.Normalizer()
seasons = nmlr.seasons()
print(seasons)

# Output: 
{
    'bn': ['গ্রীষ্ম', 'বর্ষা', 'শরৎ', 'হেমন্ত', 'শীত', 'বসন্ত'], 
    'en': ['summer', 'wet season', 'autumn', 'dry season', 'winter', 'spring']
}
```
```py
seasons = nrml.seasons(language="bn")
print(seasons)

# Output: 
['গ্রীষ্ম', 'বর্ষা', 'শরৎ', 'হেমন্ত', 'শীত', 'বসন্ত']
```
```py
seasons = nrml.seasons(language="en")
print(seasons)

# Output: 
['summer', 'wet season', 'autumn', 'dry season', 'winter', 'spring']
```


```py
seasons = nrml.seasons(seasons = "গ্রীষ্ম")
print(seasons)

# output:
{'গ্রীষ্ম': 'summer'}
```

```py
seasons = nrml.seasons(seasons = "summer")
print(seasons)

# output:
{'summer': 'গ্রীষ্ম'}
```


