

 __Citation Paper:__  BnVITS: Voice Cloning in Bangla with Minimal Audio Samples

__PyBangla:__

PyBangla is a python3 package for Bangla Number, DateTime and Text Normalizer and Date Extraction. This package can be used to Normalize the text number and date (ex: number to text vice versa). This framework  also can be used Django, Flask, FastAPI, and others. PyBangla module supported operating systems Linux/Unix, Mac OS and Windows.
Available Features.

__Features available in PyBangla:__

1. [Text Normalization](https://github.com/saiful9379/pybangla/blob/main/docs/Text_Normalizer.md)
2. [Number Conversion](https://github.com/saiful9379/pybangla/blob/main/docs/Number_Conversion.md)
3. [Date Format](https://github.com/saiful9379/pybangla/blob/main/docs/Date_Formating.md)
4. [Emoji Removal](https://github.com/saiful9379/pybangla/blob/main/docs/Emoji_Remove.md)
5. [Months, Weekdays, Seasons](https://github.com/saiful9379/pybangla/blob/main/docs/Day_Weeks_Months.md)
<h4 style='color:LightGreen'> [N.B: Here listed Every Feature has implemented Text Normalization as well as Isolated Uses feature]
 </h4>



## Installation

The easiest way to install pybangla is to use pip:

```py
pip install pybangla
#or
pip install git+https://github.com/saiful9379/pybangla.git
#or
git clone https://github.com/saiful9379/pybangla.git
cd pybangla
pip install -e .
```

## Evaluation
For the evaluation, we selected 200 sentences. The dataset contains numerical values and has been normalized using PyBangla. We generated AI-based ground truth (GT) text and had it corrected by human annotators. The performance of our tool is evaluated using three key metrics: Word Error Rate (WER), Character Error Rate (CER), and Match Error Rate (MER).

### PyBangla Evaluation

The performance of PyBangla was evaluated using **200** sentences. However, no evaluation report is available for versions earlier than **V2.0.9**.
**PyBangla** V2.0.9 Presenting conversion accuracy as well as it's processing time performance.

 ### Conversion Accuracy

| Module Version | No. of Sentences | WER (Word Error Rate) | CER (Character Error Rate) | MER (Match Error Rate) |
|---------------|----------------|----------------------|----------------------|----------------------|
| **<= V2.0.8** | 200            | _No evaluation report_ | _No evaluation report_ | _No evaluation report_ |
| **V2.0.9**    | 200            | 0.1291               | 0.0319               | 0.0975               |


__N.B : For more detail and all of processing category listed here please check : [link](./test_data/PyBangla_Evalution_V2.0.9.xlsx)__


### Processing Time Performance




| Module Version | Total Sentences | Raw Character Count | Normalized Character Count | Per Character Processing Time (sec) | Total Processing Time (sec) |
|---------------|---------------|---------------------|--------------------------|----------------------------------|----------------------|
| 2.0.9        | 200           | 9,217               | 12,584                   | 0.0001167                         | 1.076                |

## Interpretation

- The text normalization process increased the character count from **9,217** to **12,584** due to transformations such as Unicode normalization, diacritic removal, and standardization.
- The **average processing time per character** was **0.0001167 seconds**, resulting in a **total processing time of 1.076 seconds** for 200 sentences.
- These metrics demonstrate the efficiency of **PyBangla** in handling Bangla text normalization.



## Usage

### 1. [Text Normalization](https://github.com/saiful9379/pybangla/blob/main/docs/Text_Normalizer.md)
It supports converting Bangla abbreviations, symbols, and currencies to Bangla textual format.

Processes a given text by applying various normalization techniques based on specified boolean parameters.

__Parameters:__
- `text` (str): The input text to be normalized.
- `all_operation` (bool): Make this `True` if you need all operations to take place or `False`
- `number_plate` (bool, default=False): Converts or normalizes vehicle number plates if present in the text.
- `abbreviations` (bool, default=False): Expands common abbreviations into their full forms.
- `year` (bool, default=False): Handles and formats years correctly. 
- `punctuation` (bool, default=False): Removes or standardizes unwanted punctuation marks.
- `phone_number` (bool, default=False): Extracts and normalizes phone numbers.
- `symbols` (bool, default=False): Expands common symbols into their textual representation.
- `ordinals` (bool, default=False): Converts ordinal numbers.
- `currency` (bool, default=False): Converts currency values into words.
- `date` (bool, default=False): Standardizes and normalizes date formats.
- `nid` (bool, default=False): Converts national identification numbers (NID) into a textual format.
- `passport` (bool, default=False): Normalizes passport numbers.
- `number` (bool, default=False): Processes and converts numeric values into textual form.
- `emoji` (bool, default=False): Removes emojis from text.

__Returns:__
- str: The normalized text after applying the selected transformations.

__Example:__

<h3>We can enable all conversion with a simple boolean parameter.</h3>

```py
import pybangla
nrml = pybangla.Normalizer()
text = "রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য ২০৩০ শতাব্দীতে ¥২০৩০.১২৩৪ দিতে হয়েছে"
print(f"Input: {text} \nOutput {nrml.text_normalizer(text, 
                                                     all_operation=True)}")

print(text)

# output:
'রাহিম ক্লাস ওয়ান এ প্রথম, এন্ড বাসার ক্লাস এ তেত্রিশতম, সে জন্য দুই হাজার ত্রিশ শতাব্দীতে দুই হাজার ত্রিশ দশমিক এক দুই তিন চার ইয়েন দিতে হয়েছে'
```

<h3>This can be used for single operations also.</h3>

For example, if only year conversion needed -

```py
import pybangla
nrml = pybangla.Normalizer()
text = "রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য ২০৩০ শতাব্দীতে ¥২০৩০.১২৩৪ দিতে হয়েছে"
print(f"Input: {text} \nOutput {nrml.text_normalizer(text,
                                                     all_operation=False
                                                     year=True)}")

print(text)

# output:
'রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য দুই হাজার ত্রিশ শতাব্দীতে ¥২০৩০.১২৩৪ দিতে হয়েছে'
```

If only ordinal conversion needed -

```py
import pybangla
nrml = pybangla.Normalizer()
text = "রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য ২০৩০ শতাব্দীতে ¥২০৩০.১২৩৪ দিতে হয়েছে"
print(f"Input: {text} \nOutput {nrml.text_normalizer(text,
                                                     all_operation=False
                                                     ordinals=True)}")

print(text)

# output:
'রাহিম ক্লাস ওয়ান এ প্রথম, এন্ড বাসার ক্লাস এ তেত্রিশতম, সে জন্য ২০৩০ শতাব্দীতে ¥২০৩০.১২৩৪ দিতে হয়েছে'
```

If only currency conversion needed -

```py
import pybangla
nrml = pybangla.Normalizer()
text = "রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য ২০৩০ শতাব্দীতে ¥২০৩০.১২৩৪ দিতে হয়েছে"
print(f"Input: {text} \nOutput {nrml.text_normalizer(text,
                                                     all_operation=False
                                                     currency=True)}")

print(text)

# output:
'রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য ২০৩০ শতাব্দীতে দুই হাজার ত্রিশ দশমিক এক দুই তিন চার ইয়েন দিতে হয়েছে'
```

<h3>We can also use multiple conversion at once.</h3>

```py
import pybangla
nrml = pybangla.Normalizer()
text = "রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য ২০৩০ শতাব্দীতে ¥২০৩০.১২৩৪ দিতে হয়েছে"
print(f"Input: {text} \nOutput {nrml.text_normalizer(text,
                                                     all_operation=False
                                                     currency=True)}")

print(text)

# output:
'রাহিম ক্লাস ওয়ান এ ১ম, এন্ড বাসার ক্লাস এ ৩৩ তম, সে জন্য দুই হাজার ত্রিশ শতাব্দীতে দুই হাজার ত্রিশ দশমিক এক দুই তিন চার ইয়েন দিতে হয়েছে'
```

Normalizer more information or example check the [link](./docs/Text_Normalizer.md)
## 2. [Number Conversion](https://github.com/saiful9379/pybangla/blob/main/docs/Number_Conversion.md)
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

## 3. [Date Format](https://github.com/saiful9379/pybangla/blob/main/docs/Date_Formating.md)

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

## 4. [Today, Months, Weekdays, Seasons](https://github.com/saiful9379/pybangla/blob/main/docs/Day_Weeks_Months.md)

```py
import pybangla
nrml = pybangla.Normalizer()
today = nrml.today()
print(today)

Output: 
{'date': '৩০', 'month': 'এপ্রিল', 'year': '২০২৪', 'txt_date': 'ত্রিশ', 'txt_year': 'দুই হাজার চব্বিশ', 'weekday': 'মঙ্গলবার', 'ls_month': 'শ্রাবণ', 'seasons': 'বর্ষা'}
```

Today, Months, Weekdays, Seasons more information or examples check the [link](./docs/Day_Weeks_Months.md)

<h1 style='color:LightGreen'> New Feature </h1>

## <h2 style='color:LightBlue'>(UPDATE TEXT NORMALIZATION) It supports year conversion like </h2>

* "১৯৮৭-র" to "উনিশশো সাতাশি এর"
* "১৯৯৫ সালে" to "উনিশশো পঁচানব্বই সালে"
* "২০২৬-২৭" to "দুই হাজার ছাব্বিশ সাতাশ"

## <h3 style='color:LightBlue'> Now it also has the abbreviation for units of temperature </h3>

* "৪৪°F" to "চুয়াল্লিশ ডিগ্রী ফারেনহাইট"
* "৪৪°C" to "চুয়াল্লিশ ডিগ্রী সেলসিয়াস"


## <h2 style='color:LightBlue'>Phone Number Processing </h2>

* "01790-540211" to "জিরো ওয়ান সেভেন নাইন জিরো ফাইভ ফোর জিরো টু ডাবল ওয়ান"

```py
import pybangla
nrml = pybangla.Normalizer()
number_string = nrml.process_phone_number("01790-540211")
Output:
জিরো ওয়ান সেভেন নাইন জিরো ফাইভ ফোর জিরো টু ডাবল ওয়ান
```


## <h2 style='color:LightBlue'> Compare Two String Changes </h2>

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

### Next Upcoming Features

1. Bangla lemmatization and stemming algorithm
2. Bangla Tokenizer


## Contact
If you have any suggestions: Email: saifulbrur79@gmail.com

## Contributor

```
@misc{pybangla,
  title={PYBANGLA module used for normalize textual format like text to number and number to text},
  author={Islam, Md Saiful and Emon, Hassan Ali and  HM-badhon and Sarker, Sagor and Das, Udoy},
  howpublished={},
  year={2024}
}
```
