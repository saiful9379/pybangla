
import re
class Config:
    data = {
        "en":{
            "number"   : ["0","1","2","3","4","5", "6", "7","8", "9", "10", "11", "12"],
            "weekdays" : ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
            "months"   : ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",  "december"],
            "seasons" : ["summer", "wet season", "autumn","dry season", "winter", "spring"],
            "number_mapping": {'0': 'জিরো', '1': 'ওয়ান', '2': 'টু', '3': 'থ্রি', '4': 'ফোর', '5': 'ফাইভ', '6': 'সিক্স', '7': 'সেভেন', '8': 'এইট', '9': 'নাইন'}
            
            },
        "bn":{
            "number"   : ["০","১","২","৩","৪", "৫", "৬", "৭", "৮", "৯", "১০", "১১", "১২"],
            "weekdays" : ["সোমবার", "মঙ্গলবার", "বুধবার","বৃহস্পতিবার", "শুক্রবার", "শনিবার", "রবিবার"],
            "months"   : ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর",  "ডিসেম্বর"],
            "option_name" :  ["বৈশাখ", "জ্যৈষ্ঠ","আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"],
            "seasons"  : ["গ্রীষ্ম","বর্ষা", "শরৎ", "হেমন্ত", "শীত", "বসন্ত"],
            "number_mapping": {'০':'শূন্য', '১':'এক', '২':'দুই', '৩':'তিন', '৪':'চার', '৫':'পাঁচ', '৬':'ছয়', '৭':'সাত', '৮':'আট', '৯':'নয়'}

            }
    }
    bn_number_word_mapping = {'০':'শূন্য', '১':'এক', '২':'দুই', '৩':'তিন', '৪':'চার', '৫':'পাঁচ', '৬':'ছয়', '৭':'সাত', '৮':'আট', '৯':'নয়'}

    bn_regex = r'[০-৯]+'
    en_regex = r'[0-9]+'
    samples = ["-", ",", "/", " "]
    _currency = {"৳" : "টাকা", "$" : "ডলার", "£" : "পাউন্ড", "€" : "ইউরো", "¥" : "ইয়েন", "₹" : "রুপি", "₽" : "রুবেল", "₺" : "লিরা"}
    en_to_bn_digits_mapping = {e : b for e, b in zip(data["en"]["number"], data["bn"]["number"])}
    bn_to_en_digits_mapping = {v : k for k, v in en_to_bn_digits_mapping.items()}
    en_month_shortname = [i[:3] for i in data["en"]["months"]]

    data["bn"]["digits_mapping"] = en_to_bn_digits_mapping
    data["en"]["digits_mapping"] = bn_to_en_digits_mapping
    data["en"]["option_name"] = en_month_shortname
    _bangla2english_digits_mapping = {'১':'1', '২':'2', '৩':'3', '৪':'4', '৫':'5', '৬':'6', '৭':'7', '৮':'8', '৯':'9', '০':'0'}

    _abbreviations = {
        "en": [
            (re.compile("\\b%s\\." % x[0], re.IGNORECASE), x[1])
            for x in [
                ("mrs", "misess"),
                ("mr", "mister"),
                ("dr", "doctor"),
                ("st", "saint"),
                ("co", "company"),
                ("jr", "junior"),
                ("maj", "major"),
                ("gen", "general"),
                ("drs", "doctors"),
                ("rev", "reverend"),
                ("lt", "lieutenant"),
                ("hon", "honorable"),
                ("sgt", "sergeant"),
                ("capt", "captain"),
                ("esq", "esquire"),
                ("ltd", "limited"),
                ("col", "colonel"),
                ("ft", "fort"),
            ]
        ],
        "bn": [
            (re.compile(r"%s" % x[0], re.IGNORECASE), x[1])
            for x in [
                ("সাঃ", "সাল্লাল্লাহু আলাইহি ওয়া সাল্লাম"),                  
                ("আঃ", "আলাইহিস সালাম"),
                ("রাঃ", "রাদিআল্লাহু আনহু"),
                ("রহঃ", "রহমাতুল্লাহি আলাইহি"),
                ("রহিঃ", "রহিমাহুল্লাহ"),
                ("হাফিঃ", "হাফিযাহুল্লাহ"),
                ("দাঃবাঃ", "দামাত বারাকাতুহুম,দামাত বারাকাতুল্লাহ"),
                ("মোঃ",  "মোহাম্মদ"),
                ("মোসাঃ",  "মোসাম্মত"),
                ("মোছাঃ", "মোছাম্মত"),
                ("আ:" , "আব্দুর"),
                ("ডাঃ" , "ডাক্তার"),
            ]
        ]
    }

    _symbols = {
            "en": [
                (re.compile(r"%s" % re.escape(x[0]), re.IGNORECASE), x[1])
                for x in [
                    ("&", " and "),
                    ("@", " at "),
                    ("%", " percent "),
                    ("#", " hash "),
                    ("°", " degree ")
                ]
            ],
            "bn": [
                (re.compile(r"%s" % re.escape(x[0]), re.IGNORECASE), x[1])
                for x in [
                    ("&", " এবং"),
                    ("@", " এট দা রেট"),
                    ("%", " পারসেন্ট"),
                    ("#", " হ্যাশ"),
                    ("°", " ডিগ্রী")
                ]
            ],
        }

    
    _ordinal_re = {
        "en": re.compile(r"([0-9]+)(st|nd|rd|th)"),
        "bn": [
                (re.compile(r"%s" % re.escape(x[0]), re.IGNORECASE), x[1])
                for x in [
                    ("১ম", "প্রথম"),
                    ("২য়", "দ্বিতীয়"),
                    ("৩য়", "তৃতীয়"),
                    ("৪র্থ", "চতুর্থ"),
                    ("৫ম","পঞ্চম"),
                    ("৬ষ্ঠ", "ষষ্ঠ"),
                    ("৭ম", "সপ্তম"),
                    ("৮ম", "অষ্টম"),
                    ("৯ম", "নবম"),
                    ("১০ম", "দশম")
                ]
            ],
        }
    
    
    _whitespace_re = re.compile(r"\s+")
    
    
    _bangla_numeric_words = {
        'zero':'শূন্য',
        'one':'এক',
        'two':'দুই',
        'three':'তিন',
        'four':'চার',
        'five':'পাঁচ',
        'six':'ছয়',
        'seven':'সাত',
        'eight':'আট',
        'nine':'নয়',
        "hundred" : "শত", 
        "thousand" : "হাজার", 
        "lakh" : "লক্ষ", 
        "crore" : "কোটি" ,
        "ten" : "দশ",
        "eleven" : "এগারো",
        "twelve" : "বারো",
        "thirteen" : "তেরো",
        "fourteen" : "চৌদ্দ",
        "fifteen" : "পনেরো",
        "sixteen" : "ষোল",
        "seventeen" : "সতেরো",
        "eighteen" : "আঠারো",
        "nineteen" : "উনিশ",
        "twenty" : "বিশ",
        "twenty-one" : "একুশ",
        "twenty-two" : "বাইশ",
        "twenty-three" : "তেইশ",
        "twenty-four" : "চব্বিশ",
        "twenty-five" : "পঁচিশ",
        "twenty-six" : "ছাব্বিশ",
        "twenty-seven" : "সাতাশ",
        "twenty-eight" : "আঠাশ",
        "twenty-nine" : "ঊনত্রিশ",
        "thirty" : "ত্রিশ",
        "thirty-one" : "একত্রিশ",
        "thirty-two" : "বত্রিশ",
        "thirty-three" : "তেত্রিশ",
        "thirty-four" : "চৌত্রিশ",
        "thirty-five" : "পঁয়ত্রিশ",
        "thirty-six" : "ছত্রিশ",
        "thirty-seven" : "সাইত্রিশ",
        "thirty-eight" : "আটত্রিশ",
        "thirty-nine" : "ঊনচল্লিশ",
        "forty" : "চল্লিশ",
        "forty-one" : "একচল্লিশ",
        "forty-two" : "বেয়াল্লিশ",
        "forty-three" : "তেতাল্লিশ",
        "forty-four" : "চুয়াল্লিশ",
        "forty-five" : "পঁয়তাল্লিশ",
        "forty-six" : "ছেচল্লিশ",
        "forty-seven" : "সাতচল্লিশ",
        "forty-eight" : "আটচল্লিশ",
        "forty-nine" : "ঊনপঞ্চাশ",
        "fifty" : "পঞ্চাশ",
        "fifty-one" : "একান্ন",
        "fifty-two" : "বায়ান্ন",
        "fifty-three" : "তেপ্পান্ন",
        "fifty-four" : "চুয়ান্ন",
        "fifty-five" : "পঞ্চান্ন",
        "fifty-six" : "ছাপ্পান্ন",
        "fifty-seven" : "সাতান্ন",
        "fifty-eight" : "আটান্ন",
        "fifty-nine" : "ঊনষাট",
        "sixty" : "ষাট",
        "sixty-one" : "একষট্টি",
        "sixty-two" : "বাষট্টি",
        "sixty-three" : "তেষট্টি",
        "sixty-four" : "চৌষট্টি",
        "sixty-five" : "পঁয়ষট্টি",
        "sixty-six" : "ছেষট্টি",
        "sixty-seven" : "সাতষট্টি",
        "sixty-eight" : "আটষট্টি",
        "sixty-nine" : "ঊনসত্তর",
        "seventy" : "সত্তর",
        "seventy-one" : "একাত্তর",
        "seventy-two" : "বাহাত্তর",
        "seventy-three" : "তেয়াত্তর",
        "seventy-four" : "চুয়াত্তর",
        "seventy-five" : "পঁচাত্তর",
        "seventy-six" : "ছিয়াত্তর",
        "seventy-seven" : "সাতাত্তর",
        "seventy-eight" : "আটাত্তর",
        "seventy-nine" : "ঊনআশি",
        "eighty" : "আশি",
        "eighty-one" : "একাশি",
        "eighty-two" : "বিরাশি",
        "eighty-three" : "তিরাশি",
        "eighty-four" : "চুরাশি",
        "eighty-five" : "পঁচাশি",
        "eighty-six" : "ছিয়াশি",
        "eighty-seven" : "সাতাশি",
        "eighty-eight" : "আটাশি",
        "eighty-nine" : "ঊননব্বই",
        "ninety" : "নব্বই",
        "ninety-one" : "একানব্বই",
        "ninety-two" : "বিরানব্বই",
        "ninety-three" : "তিরানব্বই",
        "ninety-four" : "চুরানব্বই",
        "ninety-five" : "পঁচানব্বই",
        "ninety-six" : "ছিয়ানব্বই",
        "ninety-seven" : "সাতানব্বই",
        "ninety-eight" : "আটানব্বই",
        "ninety-nine" : "নিরানব্বই"
    }