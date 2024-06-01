
PYBANGLA is a python3 package for Bangla Number, DateTime and Text Normalizer and Date Extraction. This package can be used to Normalize the text number and date (ex: number to text vice versa). This framework  also can be used Django, Flask, FastAPI, and others. PYBANGLA module supported operating systems Linux/Unix, Mac OS and Windows.
Available Features

Features available in PYBANGLA:

1. [Text Normalization](https://github.com/saiful9379/pybangla/blob/main/docs/Text_Normalizer.md)
2. [Number Conversion](https://github.com/saiful9379/pybangla/blob/main/docs/Number_Conversion.md)
3. [Date Format](https://github.com/saiful9379/pybangla/blob/main/docs/Date_Formating.md)
4. [Emoji Removal](https://github.com/saiful9379/pybangla/blob/main/docs/Emoji_Remove.md)
5. [Months, Weekdays, Seasons](https://github.com/saiful9379/pybangla/blob/main/docs/Day_Weeks_Months.md)
<h4 style='color:LightGreen'> [N.B: Here listed Every Feature has implemented Text Normalization as well as Isolated Uses feature]
 </h4>

# Installation

The easiest way to install pybangla is to use pip:

```
pip install pybangla
```


# Usage

# 1. [Text Normalization](https://github.com/saiful9379/pybangla/blob/main/docs/Text_Normalizer.md)
It supports converting Bangla abbreviations, symbols, and currencies to Bangla textual format.

Example:
```py
import pybangla
nrml = pybangla.Normalizer()
text = "রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য ২০৩০ শতাব্দীতে ¥২০৩০.১২৩৪ দিতে হয়েছে"
text = nrml.text_normalizer(text)

print(text)

# output:
'রাহিম ক্লাস ওয়ান এ প্রথম, এন্ড বাসার ক্লাস এ তেত্রিশতম, সে জন্য দুই হাজার ত্রিশ শতাব্দীতে দুই হাজার ত্রিশ দশমিক এক দুই তিন চার ইয়েন দিতে হয়েছে'
```
Normalizer more information or example check the [link](./docs/Text_Normalizer.md)
# 2. [Number Conversion](https://github.com/saiful9379/pybangla/blob/main/docs/Number_Conversion.md)
Example:

```py
import pybangla
nrml = pybangla.Normalizer()
text = "আমাকে এক লক্ষ দুই হাজার এক টাকা দেয় এন্ড তুমি বিশ হাজার টাকা নিও এন্ড এক লক্ষ চার হাজার দুইশ এক টাকা এক ডবল দুই"
text = nrml.word2number(text)
print(text)
#output:
'আমাকে 102001 টাকা দেয় এন্ড তুমি 20000 টাকা নিও এন্ড 104201 টাকা 122 '

```
Number conversion more information or examples check the [link](./docs/Number_Conversion.md)

# 3. [Date Format](https://github.com/saiful9379/pybangla/blob/main/docs/Date_Formating.md)

Example:
```py
import pybangla
nrml = pybangla.Normalizer()
date = "০১-এপ্রিল/২০২৩"
date = nrml.date_format(date, language="bn")
print(date)
#output:


{'date': '০১', 'month': '৪', 'year': '২০২৩', 'txt_date': 'এক', 'txt_month': 'এপ্রিল', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}

```
Date Format for more information or example check the [link](./docs/Date_Formating.md)

# 4. [Emoji Removal](https://github.com/saiful9379/pybangla/blob/main/docs/Emoji_Remove.md)


```py
text = 'দয়া করে পবিত্র কুরআনুল কারিম বলেন,,,,পবিত্র কথাটা অবশ্যই বলবেন,,, প্লিজ 😢😥🙏🙏🙏'
text = nrml.remove_emoji(text)
print(f"{text}")

#output:
দয়া করে পবিত্র কুরআনুল কারিম বলেন,,,,পবিত্র কথাটা অবশ্যই বলবেন,,, প্লিজ
```
For Emoji Removal more information or example check the [link](./docs/Emoji_Remove.md)
# 5. [Today, Months, Weekdays, Seasons](https://github.com/saiful9379/pybangla/blob/main/docs/Day_Weeks_Months.md)

```py
import pybangla
nrml = pybangla.Normalizer()
today = nrml.today()
print(today)

# Output: 
{'date': '৩০', 'month': 'এপ্রিল', 'year': '২০২৪', 'txt_date': 'ত্রিশ', 'txt_year': 'দুই হাজার চব্বিশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```

Today, Months, Weekdays, Seasons more information or examples check the [link](./docs/Day_Weeks_Months.md)

<h1 style='color:LightGreen'> New Feature </h1>

<h2 style='color:LightBlue'>(UPDATE TEXT NORMALIZATION) It supports year conversion like </h2>

* "১৯৮৭-র" to "উনিশশো সাতাশি এর"
* "১৯৯৫ সালে" to "উনিশশো পঁচানব্বই সালে"
* "২০২৬-২৭" to "দুই হাজার ছাব্বিশ সাতাশ"

<h3 style='color:LightBlue'> Now it also has the abbreviation for units of temperature </h3>

* "৪৪°F" to "চুয়াল্লিশ ডিগ্রী ফারেনহাইট"
* "৪৪°C" to "চুয়াল্লিশ ডিগ্রী সেলসিয়াস"


<h2 style='color:LightBlue'>Phone Number Processing </h2>

* "01790-540211" to "জিরো ওয়ান সেভেন নাইন জিরো ফাইভ ফোর জিরো টু ডাবল ওয়ান"

```py
import pybangla
nrml = pybangla.Normalizer()
number_string = nrml.process_phone_number("01790-540211")
Output:
জিরো ওয়ান সেভেন নাইন জিরো ফাইভ ফোর জিরো টু ডাবল ওয়ান
```


<h2 style='color:LightBlue'> Compare Two String Changes </h2>

```py
import pybangla
nrml = pybangla.Normalizer()

input1 = "১৯৯৬সালের ৬ সেপ্টেম্বররণ ভ্রমণ পরিকল্পনা করছি ২০৩০সালের ৬সেপ্টেম্বর"

input2 = "উনিশশো ছিয়ানব্বই সালের ছয় সেপ্টেম্বর রণ ভ্রমণ পরিকল্পনা করছি দুই হাজার ত্রিশ সালের ছয় সেপ্টেম্বর"

print(nrml.text_diff(input1, input2))

#Output: 

(
    ['১৯৯৬সালের ৬', 'সেপ্টেম্বররণ', '২০৩০সালের', '৬সেপ্টেম্বর'], 
    ['উনিশশো ছিয়ানব্বই সালের ছয়', 'সেপ্টেম্বর রণ', 'দুই হাজার ত্রিশ সালের ছয়', 'সেপ্টেম্বর']
)

```

<h2> </h2>

# Next Upcoming Features

1. Bangla lemmatization and stemming algorithm
2. Bangla Tokenizer


# Contact
If you have any suggestions: Email: saifulbrur79@gmail.com

# Contributor

```
@misc{pybangla,
  title={PYBANGLA module used for normalize textual format like text to number and number to text},
  author={Md Saiful Islam, Hassan Ali Emon,  HM-badhon, Sagor Sarker, ud0y},
  howpublished={},
  year={2024}
}
```
If you face any problems feel free to open an issue.

