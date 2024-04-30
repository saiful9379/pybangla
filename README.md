# Project Discription
PYBANGLA is a Python 3 package designed to normalize Bengali numbers, time, date, and text. With this package, you can easily standardize text, numbers, and dates. It also offers the reverse functionality, allowing you to convert text into numbers. PYBANGLA is versatile, compatible with any Python environment or framework such as Django, Flask, or FastAPI. Moreover, it seamlessly integrates with various operating systems including Linux/Unix, MacOS, and Windows, serving as an additional library to simplify the challenges of time and date normalization.

Features available in PYBANGLA:
1. Date Format
2. Text Normalization
3. Number Converstion
4. Months, Weekdays, Seasons

# Installation

The easiest way to install pybangla is to use pip:

```
pip install pybangla
```

# Usage

## 1. Text Normalization
Text Normalization steps
1. Whitespace
2. Symbol Expansion (eg. & -> এবং)
3. Text Expansion (eg. মোঃ ->  মোহাম্মদ)
4. Positional Expansion (eg. ১ম -> প্রথম, 1st -> first)
4. Currency Expansion (eg. ৳-> টাকা, $ -> Dollar)[Supprotes ৳,$£,€,¥,₹,₽,₺]
5. Year Formation (eg. ২০৩০ -> দুই হাজার ত্রিশ)
6. Number Processing (৩৩-> তেত্রিশ)

```python
import pybangla
nrml = pybangla.Normalizer()

text = "আব্দুর রহিম ক্লাস ওয়ান এ ১ম, অ্যান্ড বাসার ৩৩ তম হয়েছিল। এটা ২০২৩ শতাব্দীর কথা & সে কারণে আব্দুর রহিম ¥২০৩০.১২৩৪ পুরষ্কার পেয়েছিল"
text = nrml.text_normalizer(text)
print(f"{text}")
```
Output
```
আব্দুর রহিম ক্লাস ওয়ান এ প্রথম, অ্যান্ড বাসার তেত্রিশতম হয়েছিল।। এটা দুই হাজার তেইশ শতাব্দীর কথা এবং সে কারণে আব্দুর রহিম দুই হাজার ত্রিশ দশমি এক দুই তিন চার ইয়েন পুরষ্কার পেয়েছিল
```

## 2.1. Number Conversion (Text to Number)

```python
import pybangla
nrml = pybangla.Normalizer()

text = "আমাকে এক লক্ষ দুই হাজার একশত তিন টাকা দিলে এন্ড এক লক্ষ চার হাজার দুইশ এক টাকা সামনের মাসে পাবো ।  তোমাকে সেখান থেকে বিশ হাজার টাকা দিব এন্ড এক ডবল দুই মানে দুই মাসের মধ্যে তুমি আমাকে টাকা টা ফেরত দিবে"
number = nrml.word2number(text)
print(f"{number}")
```
Output
```
আমাকে 102103 টাকা দিলে এন্ড 104201 টাকা সামনের মাসে পাবো । তোমাকে সেখান থেকে 20000 টাকা দিব এন্ড 122 মানে 2 মাসের মধ্যে তুমি আমাকে টাকা টা ফেরত দিবে
```
``` python
import pybangla
nrml = pybangla.Normalizer()
input_texts = [
    "আমি এক দুই তিন চার পাঁচ টু থ্রি ফাইভ ছয় সেভেন এইট নাইন শূন্য আমার ফোন নাম্বার জিরো ওয়ান ডাবল সেভেন",
    "ওয়ান ডাবল নাইন টু",
    "একশ বিশ টাকা",
    "জিরো টু ডাবল ওয়ান",
    "জিরো ওয়ান ডাবল সেভেন থ্রি ডাবল ফাইভ নাইন থ্রি সেভেন নাইন",
    "আমার ফোন নম্বর জিরো ওয়ান ডাবল সেভেন থ্রি ডাবল ফাইভ নাইন থ্রি সেভেন নাইন",
    "ট্রিপল টু ওয়ান",
    "দুই হাজার চারশো বিশ",
    "দুই হাজার চারশ  বিশ",
    "হাজার বিশ",
    "ডাবল নাইন টু",
    "এক লক্ষ চার হাজার দুইশ",
    "এক লক্ষ চার হাজার দুইশ এক",
    "এক লক্ষ চার হাজার দুইশ এক টাকা এক দুই",
    "আমাকে এক লক্ষ দুই হাজার টাকা দেয়",
    "আমাকে এক লক্ষ দুই হাজার এক টাকা দেয় এন্ড তুমি বিশ হাজার টাকা নিও এন্ড এক লক্ষ চার হাজার দুইশ এক টাকা এক ডবল দুই",
    "ছয় হাজার বিশ",
    "আমার সাড়ে পাঁচ হাজার",
    "আমার সাড়ে তিনশ",
    "আড়াই হাজার",
    "আড়াই লক্ষ",
    "ডেরশ",
    "আমাকে ডেরশ টাকা দেয়",
    "সাড়ে পাঁচ কোটি টাকা",
    "সাড়ে 1254 টাকা",
    "জিরো",
    "একশ বিশ take একশ",
    "জিরো টু ডাবল ওয়ান",
    "জিরো টু ওয়ান ওয়ান",
    "থ্রি ফোর ফাইভ এইট",
    "একশ বিশ টাকা",
    "ডাবল ওয়ান ডবল টু",
    "জিরো ওয়ান টু",
    "থ্রি ফোর ফাইভ সিক্স",
    "সেভেন এইট নাইন টেন",
    "একশ দুইশ তিনশ",
    "চারশ পাঁচশ",
    "ছয়শ সাতশ",
    "আটশ নয়শ",
    "দশ তিরানব্বই",
    "ট্রিপল থ্রি টু",
    "শূন্য এক দুই তিন",
    "চার পাঁচ ছয় সাত",
    "আট নয় দশ এগারো",
    "বারো তেরো চৌদ্দ পনেরো",
    "ষোল সতেরো আঠারো উনিশ",
    "বিশ একুশ বাইশ তেইশ",
    "চব্বিশ পঁচিশ ছাব্বিশ সাতাশ",
    "আঠাশ ঊনত্রিশ ত্রিশ একত্রিশ",
    "বত্রিশ তেত্রিশ চৌত্রিশ পঁয়ত্রিশ",
    "ছত্রিশ সাঁইত্রিশ আটত্রিশ ঊনচল্লিশ",
    "চল্লিশ একচল্লিশ বিয়াল্লিশ তেতাল্লিশ",
    "চুয়াল্লিশ পঁয়তাল্লিশ ছেচল্লিশ সাতচল্লিশ",
    "আটচল্লিশ ঊনপঞ্চাশ পঞ্চাশ একান্ন",
    "বাহান্ন তিপ্পান্ন চুয়ান্ন পঞ্চান্ন",
    "ছাপ্পান্ন সাতান্ন আটান্ন ঊনষাট",
    "ষাট একষট্টি বাষট্টি তেষট্টি",
    "চৌষট্টি পঁয়ষট্টি ছেষট্টি সাতষট্টি",
    "আটষট্টি ঊনসত্তর সত্তর একাত্তর",
    "বাহাত্তর তিয়াত্তর চুয়াত্তর পঁচাত্তর",
    "ছিয়াত্তর সাতাত্তর আটাত্তর ঊনআশি",
    "আশি একাশি বিরাশি তিরাশি",
    "চুরাশি পঁচাশি ছিয়াশি সাতাশি",
    "আটাশি ঊননব্বই নব্বই একানব্বই",
    "বিরানব্বই তিরানব্বই চুরানব্বই পঁচানব্বই",
    "ছিয়ানব্বই সাতানব্বই আটানব্বই নিরানব্বই",
    "এক লক্ষ চার হাজার দুইশ এক টাকা এক দুই",
    "তিনশ পঁচিশ পাঁচশ",
    "তিনশ পঁচিশ পাঁচশ এক",
    "চা-পুন",
    "ওকে",
    "ডের আউটস্ট্যান্ডিং কত",
    "ডাবল",
    "নাইন ডাবল এইট",
    "দশ বারো এ এগুলা একশ একশ দুই"
    ]
for text in input_texts:
    print(f"input   : {text}")
    number = nrml.word2number(text)
    print(f"output : {number}")
```
Output
```
input   : আমি এক দুই তিন চার পাঁচ টু থ্রি ফাইভ ছয় সেভেন এইট নাইন শূন্য আমার ফোন নাম্বার জিরো ওয়ান ডাবল সেভেন
output : আমি 1234523567890 আমার ফোন নাম্বার 0177 
input   : ওয়ান ডাবল নাইন টু
output : 1992 
input   : একশ বিশ টাকা
output : 120 টাকা 
input   : জিরো টু ডাবল ওয়ান
output : 0211 
input   : জিরো ওয়ান ডাবল সেভেন থ্রি ডাবল ফাইভ নাইন থ্রি সেভেন নাইন
output : 01773559379 
input   : আমার ফোন নম্বর জিরো ওয়ান ডাবল সেভেন থ্রি ডাবল ফাইভ নাইন থ্রি সেভেন নাইন
output : আমার ফোন নম্বর 01773559379 
input   : ট্রিপল টু ওয়ান
output : 2221 
input   : দুই হাজার চারশো বিশ
output : 2420 
input   : দুই হাজার চারশ  বিশ
output : 2420 
input   : হাজার বিশ
output : 1020 
input   : ডাবল নাইন টু
output : 992 
input   : এক লক্ষ চার হাজার দুইশ
output : 104200 
input   : এক লক্ষ চার হাজার দুইশ এক
output : 104201 
input   : এক লক্ষ চার হাজার দুইশ এক টাকা এক দুই
output : 104201 টাকা 12 
input   : আমাকে এক লক্ষ দুই হাজার টাকা দেয়
output : আমাকে 102000 টাকা দেয় 
input   : আমাকে এক লক্ষ দুই হাজার এক টাকা দেয় এন্ড তুমি বিশ হাজার টাকা নিও এন্ড এক লক্ষ চার হাজার দুইশ এক টাকা এক ডবল দুই
output : আমাকে 102001 টাকা দেয় এন্ড তুমি 20000 টাকা নিও এন্ড 104201 টাকা 122 
input   : ছয় হাজার বিশ
output : 6020 
input   : আমার সাড়ে পাঁচ হাজার
output : আমার 5500 
input   : আমার সাড়ে তিনশ
output : আমার 350 
input   : আড়াই হাজার
output : 2500 
input   : আড়াই লক্ষ
output : 250000 
input   : ডেরশ
output : 150 
input   : আমাকে ডেরশ টাকা দেয়
output : আমাকে 150 টাকা দেয় 
input   : সাড়ে পাঁচ কোটি টাকা
output : 55000000 টাকা 
input   : সাড়ে 1254 টাকা
output : 1881 টাকা 
input   : জিরো
output : 0 
input   : একশ বিশ take একশ
output : 120 take 100 
input   : জিরো টু ডাবল ওয়ান
output : 0211 
input   : জিরো টু ওয়ান ওয়ান
output : 0211 
input   : থ্রি ফোর ফাইভ এইট
output : 3458 
input   : একশ বিশ টাকা
output : 120 টাকা 
input   : ডাবল ওয়ান ডবল টু
output : 1122 
input   : জিরো ওয়ান টু
output : 012 
input   : থ্রি ফোর ফাইভ সিক্স
output : 3456 
input   : সেভেন এইট নাইন টেন
output : 78910 
input   : একশ দুইশ তিনশ
output : 100 200 300 
input   : চারশ পাঁচশ
output : 400 500 
input   : ছয়শ সাতশ
output : 600 700 
input   : আটশ নয়শ
output : 800 900 
input   : দশ তিরানব্বই
output : 1093 
input   : ট্রিপল থ্রি টু
output : 3332 
input   : শূন্য এক দুই তিন
output : 0123 
input   : চার পাঁচ ছয় সাত
output : 4567 
input   : আট নয় দশ এগারো
output : 891011 
input   : বারো তেরো চৌদ্দ পনেরো
output : 12131415 
input   : ষোল সতেরো আঠারো উনিশ
output : 16171819 
input   : বিশ একুশ বাইশ তেইশ
output : 20212223 
input   : চব্বিশ পঁচিশ ছাব্বিশ সাতাশ
output : 24252627 
input   : আঠাশ ঊনত্রিশ ত্রিশ একত্রিশ
output : 28293031 
input   : বত্রিশ তেত্রিশ চৌত্রিশ পঁয়ত্রিশ
output : 32333435 
input   : ছত্রিশ সাঁইত্রিশ আটত্রিশ ঊনচল্লিশ
output : 36373839 
input   : চল্লিশ একচল্লিশ বিয়াল্লিশ তেতাল্লিশ
output : 40414243 
input   : চুয়াল্লিশ পঁয়তাল্লিশ ছেচল্লিশ সাতচল্লিশ
output : 44454647 
input   : আটচল্লিশ ঊনপঞ্চাশ পঞ্চাশ একান্ন
output : 48495051 
input   : বাহান্ন তিপ্পান্ন চুয়ান্ন পঞ্চান্ন
output : 52535455 
input   : ছাপ্পান্ন সাতান্ন আটান্ন ঊনষাট
output : 56575859 
input   : ষাট একষট্টি বাষট্টি তেষট্টি
output : 60616263 
input   : চৌষট্টি পঁয়ষট্টি ছেষট্টি সাতষট্টি
output : 64656667 
input   : আটষট্টি ঊনসত্তর সত্তর একাত্তর
output : 68697071 
input   : বাহাত্তর তিয়াত্তর চুয়াত্তর পঁচাত্তর
output : 72737475 
input   : ছিয়াত্তর সাতাত্তর আটাত্তর ঊনআশি
output : 76777879 
input   : আশি একাশি বিরাশি তিরাশি
output : 80818283 
input   : চুরাশি পঁচাশি ছিয়াশি সাতাশি
output : 84858687 
input   : আটাশি ঊননব্বই নব্বই একানব্বই
output : 88899091 
input   : বিরানব্বই তিরানব্বই চুরানব্বই পঁচানব্বই
output : 92939495 
input   : ছিয়ানব্বই সাতানব্বই আটানব্বই নিরানব্বই
output : 96979899 
input   : এক লক্ষ চার হাজার দুইশ এক টাকা এক দুই
output : 104201 টাকা 12 
input   : তিনশ পঁচিশ পাঁচশ
output : 325 500 
input   : তিনশ পঁচিশ পাঁচশ এক
output : 325 501 
input   : চা-পুন
output : চা-পুন 
input   : ওকে
output : ওকে 
input   : ডের আউটস্ট্যান্ডিং কত
output : ডের আউটস্ট্যান্ডিং কত 
input   : ডাবল
output : 2 
input   : নাইন ডাবল এইট
output : 988 
input   : দশ বারো এ এগুলা একশ একশ দুই
output : 1012 এ এগুলা 100 102 
```
## 2.1. Number Conversion (Number to Text)
Bangla
``` python
import pybangla
nrml = pybangla.Normalizer()
number = nrml.number_convert("12345", language="bn")
print(number)
```
Output
```
{'digit': '১২৩৪৫', 'digit_word': 'এক দুই তিন চার পাঁচ', 'number_string': 'বারো হাজার তিন শত পঁয়তাল্লিশ'}
```
English
``` python
number = nrml.number_convert("১২৩৪৫", language="en")
print(number)
```
Output
```
{'digit': '12345', 'digit_word': 'ওয়ান টু থ্রি ফোর ফাইভ', 'number_string': 'twelve thousand three hundred forty-five'}
```
## 3. Date Format
Supported Date Format:

```
2023-04-05
06-04-2023
04/01/2023
07 April, 2023
Apr 1, 2023
2023/04/01
01-Apr-2023
01-Apr/2023
20230401
20042024
["1", "4", "2025"]
```

``` python
import pybangla
nrml = pybangla.Normalizer()

date = nrml.date_format("০১-এপ্রিল/২০২৩", language="bn")
print(f"{date}")
```
Output
```
{'date': '০১', 'month': 'এপ্রিল', 'year': '২০২৩', 'txt_date': 'এক', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```
Bangla (`Parameter "bn"`)
``` python
date_list  = ["2023-04-05",  "06-04-2023", "04/01/2023", "07 April, 2023", "Apr 1, 2023",  "2023/04/01", "01-Apr-2023", "01-Apr/2023",  "20230401",  "20042024", ["1", "4", "2025"]]
for date in date_list:
    print("input :", date)
    fromat_date = nrml.date_format(date, language="bn")
    print("output :", fromat_date)
```
Output
```
input : 2023-04-05
output : {'date': '০৫', 'month': 'এপ্রিল', 'year': '২০২৩', 'txt_date': 'পাঁচ', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'বুধবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
input : 06-04-2023
output : {'date': '০৬', 'month': 'এপ্রিল', 'year': '২০২৩', 'txt_date': 'ছয়', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'বৃহস্পতিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
input : 04/01/2023
output : {'date': '০৪', 'month': 'জানুয়ারি', 'year': '২০২৩', 'txt_date': 'চার', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'বুধবার', 'ls_month': 'বৈশাখ', 'seasons': 'গ্রীষ্ম'}
input : 07 April, 2023
output : {'date': '০৭', 'month': 'এপ্রিল', 'year': '২০২৩', 'txt_date': 'সাত', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শুক্রবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
input : Apr 1, 2023
output : {'date': '১', 'month': 'এপ্রিল', 'year': '২০২৩', 'txt_date': 'এক', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
input : 2023/04/01
output : {'date': '০১', 'month': 'এপ্রিল', 'year': '২০২৩', 'txt_date': 'এক', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
input : 01-Apr-2023
output : {'date': '০১', 'month': 'এপ্রিল', 'year': '২০২৩', 'txt_date': 'এক', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
input : 01-Apr/2023
output : {'date': '০১', 'month': 'এপ্রিল', 'year': '২০২৩', 'txt_date': 'এক', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
input : 20230401
output : {'date': '০১', 'month': 'এপ্রিল', 'year': '২০২৩', 'txt_date': 'এক', 'txt_year': 'দুই হাজার তেইশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
input : 20042024
output : {'date': '২০', 'month': 'এপ্রিল', 'year': '২০২৪', 'txt_date': 'বিশ', 'txt_year': 'দুই হাজার চব্বিশ', 'weekday': 'শনিবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
input : ['1', '4', '2025']
output : {'date': '১', 'month': 'এপ্রিল', 'year': '২০২৫', 'txt_date': 'এক', 'txt_year': 'দুই হাজার পঁচিশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```
English (`Parameter "en"`)
```python
date_list  = ["2023-04-05",  "06-04-2023", "04/01/2023", "07 April, 2023", "Apr 1, 2023",  "2023/04/01", "01-Apr-2023", "01-Apr/2023",  "20230401",  "20042024", ["1", "4", "2025"]]
for date in date_list:
    print("input :", date)
    fromat_date = nrml.date_format(date, language="en")
    print("output :", fromat_date)
```
Output
```
input : 2023-04-05
output : {'date': '05', 'month': 'april', 'year': '2023', 'txt_date': 'five', 'txt_year': 'twenty century twenty-three', 'weekday': 'wednesday', 'ls_month': 'apr', 'seasons': 'wet season'}
input : 06-04-2023
output : {'date': '06', 'month': 'april', 'year': '2023', 'txt_date': 'six', 'txt_year': 'twenty century twenty-three', 'weekday': 'thursday', 'ls_month': 'apr', 'seasons': 'wet season'}
input : 04/01/2023
output : {'date': '04', 'month': 'january', 'year': '2023', 'txt_date': 'four', 'txt_year': 'twenty century twenty-three', 'weekday': 'wednesday', 'ls_month': 'jan', 'seasons': 'summer'}
input : 07 April, 2023
output : {'date': '07', 'month': 'april', 'year': '2023', 'txt_date': 'seven', 'txt_year': 'twenty century twenty-three', 'weekday': 'friday', 'ls_month': 'apr', 'seasons': 'wet season'}
input : Apr 1, 2023
output : {'date': '1', 'month': 'april', 'year': '2023', 'txt_date': 'one', 'txt_year': 'twenty century twenty-three', 'weekday': 'saturday', 'ls_month': 'apr', 'seasons': 'wet season'}
input : 2023/04/01
output : {'date': '01', 'month': 'april', 'year': '2023', 'txt_date': 'one', 'txt_year': 'twenty century twenty-three', 'weekday': 'saturday', 'ls_month': 'apr', 'seasons': 'wet season'}
input : 01-Apr-2023
output : {'date': '01', 'month': 'april', 'year': '2023', 'txt_date': 'one', 'txt_year': 'twenty century twenty-three', 'weekday': 'saturday', 'ls_month': 'apr', 'seasons': 'wet season'}
input : 01-Apr/2023
output : {'date': '01', 'month': 'april', 'year': '2023', 'txt_date': 'one', 'txt_year': 'twenty century twenty-three', 'weekday': 'saturday', 'ls_month': 'apr', 'seasons': 'wet season'}
input : 20230401
output : {'date': '01', 'month': 'april', 'year': '2023', 'txt_date': 'one', 'txt_year': 'twenty century twenty-three', 'weekday': 'saturday', 'ls_month': 'apr', 'seasons': 'wet season'}
input : 20042024
output : {'date': '20', 'month': 'april', 'year': '2024', 'txt_date': 'twenty', 'txt_year': 'twenty century twenty-four', 'weekday': 'saturday', 'ls_month': 'apr', 'seasons': 'wet season'}
input : ['1', '4', '2025']
output : {'date': '1', 'month': 'april', 'year': '2025', 'txt_date': 'one', 'txt_year': 'twenty century twenty-five', 'weekday': 'tuesday', 'ls_month': 'apr', 'seasons': 'wet season'}
```
## Months, Weekdays, and Seasons
### Today
``` python
import pybangla
nrml = pybangla.Normalizer()

date = nrml.today()
print(f"{date}")
```
Output
```
{'date': '২৯', 'month': 'এপ্রিল', 'year': '২০২৪', 'txt_date': 'ঊনত্রিশ', 'txt_year': 'ঊনত্রিশ', 'weekday': 'সোমবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```
### Weekday
```python
import pybangla
nrml = pybangla.Normalizer()

date = nrml.weekdays()
print(f"{date}")
```
Output
```
{'bn': ['সোমবার', 'মঙ্গলবার', 'বুধবার', 'বৃহস্পতিবার', 'শুক্রবার', 'শনিবার', 'রবিবার'], 
'en': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']}
```
### Season
```python
import pybangla
nrml = pybangla.Normalizer()

date = nrml.seasons()
print(f"{date}")
```
Output
``` 
{'bn': ['গ্রীষ্ম', 'বর্ষা', 'শরৎ', 'হেমন্ত', 'শীত', 'বসন্ত'],
 'en': ['summer', 'wet season', 'autumn', 'dry season', 'winter', 'spring']}
```