import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

import time
from pybangla.module.main import Normalizer

if __name__ == "__main__":


    # Testing Date format
    date_list = [
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
    ]
    # number = "123456" or "২০২৩"
    number = "২০২৩"
    nmlr = Normalizer()
    print("++++++++++++++++++++ Date testing ++++++++++++++++++++++")
    print("Date format Testing : ", end ="", flush=True)
    for date_ in date_list:
        start_time = time.time()
        formated_date = nmlr.date_format(date_, language="bn")
        print(formated_date)
    print("++++++++++++++++++++ end of Date testing ++++++++++++++++++++++")

    print("++++++++++++++++++++ en number to bn number convert ++++++++++++++++++++++")
    number = nmlr.number_convert(number, language="bn")

    print("Bn Number : ", number)
    print("++++++++++++++++++++ stop number convert ++++++++++++++++++++++")

    print("++++++++++++++++ Today +++++++++++++++++++++")
    today_date = nmlr.today(language="bn")
    # today_date = nmlr.today(language="en")
    print(today_date)

    print("++++++++++++++++ End Today +++++++++++++++++++++")
    # print(today_date)
    print("++++++++++++++++ weekdays +++++++++++++++++++++")
    # weekdays = nmlr.weekdays()
    # weekdays = nmlr.weekdays(language="bn")
    # weekdays = nmlr.weekdays(language="en")
    # weekdays = nmlr.weekdays(day = "সোমবার")
    weekdays = nmlr.weekdays(day = "Monday")
    print(weekdays)

    print("++++++++++++++++ end weekdays +++++++++++++++++++++")
    # print(weekdays)
    print("+++++++++++++++ seasons ++++++++++++++++++++++++")
    # seasons = nmlr.seasons()
    # seasons = nmlr.seasons(language="bn")
    # seasons = nmlr.seasons(language="en")
    seasons = nmlr.seasons(seasons = "গ্রীষ্ম")
    print(seasons)

    print("+++++++++++++++ end seasons ++++++++++++++++++++++++")

    print("+++++++++++++++++ months +++++++++++++++++++++++++++")
    month = nmlr.months()
    month = nmlr.months(month="মার্চ")
    print(month)


    text = "রাহিম ক্লাস ওয়ান এ ১ম, ১১তম ২২ তম ৩৩ তম, ১২৩৪ শতাব্দীতে ¥২০৩০.১২৩৪ বিবিধ  বাকেরগঞ্জ উপজেলার প্রায় 40 ভাগের পেশাই চাষাবাদ 80 and 40 ২২"
    
    text = nmlr.text_normalizer(text)

    print(text)
    print("+++++++++++++++++ end months +++++++++++++++++++++++++++")
    
    print("+++++++++++++++++ punctuations +++++++++++++++++++++++++++")
    text = "শাশ্বতী জানালেন, বিয়ে-বৌভাতের চলতি মরশুমে ভোজবাড়ির ডিনারে এক জনের প্রত্যাবর্তন ঘটেছে— দাপুটে প্রত্যাবর্তন।"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "সে যা-ই হোক, সত্যিকারের এমন পাকা পোনা শেষ বার নেমন্তন্ন বাড়িতে খেয়েছি ১৯৮৭-র এপ্রিলে।"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "‘আমি ছেলেকে ছাড়া বাঁচব কী করে’"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "২০২০ সালে ‘দেয়ার ইজ নো এভিল’ সিনেমার জন্য বার্লিন উৎসবের সর্বোচ্চ পুরস্কার স্বর্ণভালুক জেতেন রাসুলফ। ২০২২ সালে তাঁকে গ্রেপ্তার করা হয়, পরে ইরানে বিক্ষোভ শুরু হলে সে বছরের সেপ্টেম্বর মাসে তাঁকে মুক্তি দেওয়া হয়।"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "করে ‘দ্য পাবলিক গ্যাম্বলিং অ্যাক্ট ১৮৬৭’ সংশোধনের উদ্যোগ নেওয়া হয়েছে।"
    text = nmlr.text_normalizer(text)
    print(text) 
    
    text = "৬৭% সংশোধনের উদ্যোগ নেওয়া হয়েছে।"
    text = nmlr.text_normalizer(text)
    print(text)
    print("+++++++++++++++++ end punctuations +++++++++++++++++++++++++++")
    
    print("+++++++++++++++++ random test +++++++++++++++++++++++++++")
    text = '"আবূ মুসা আশা’আরী (রাঃ) থেকে বর্ণিতঃরাসূলুল্লাহ (সাল্লাল্লাহু ‘আলাইহি ওয়া সাল্লাম) বলেছেন, “তিনবার অনুমতি চাইবে। অনুমতি দিলে প্রবেশ করবে, অন্যথায় ফিরে যাবে।” (বুখারী ৬২৪৫, মুসলিম ২১৫৩)",'
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "ফাইজলামির সিমা থাকা দরকার!! সব পাগল চোদা সাংবাদিক!!"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "দাড়াবে?না হারিস আনিস জোসেফের মতো খালাস!!!???"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "মিথ্যা প্রচার করছ কে.....?"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "নিজে ও তার নেশাখোর ছেলে সহ অনুপ্রবেশকারী সন্ত্রাসীরা।। ২৬-১২-২১ ইং ভোট কেন্দ্রগূলোতেও বড় ধরনের সংঘাত করার প্ল্যান করা হইছে।"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "এই রকম পাগল কা..==.কা করে যাচ্ছে ততই মুগ্ধ হয়ে গেলাম"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "আজব এক ধর্ম। অবমাননার অর্থ কি ? ? কেউ বলবেন? ? মেধাহীন জাতি তা আর একবার প্রমাণ করলো ।"
    text = nmlr.text_normalizer(text)
    print(text)
    
    text = "রাহিম ক্লাস ওয়ান এ ১ম, ১১তম ২২ তম ৩৩ তম, ১২৩৪ শতাব্দীতে ¥২০৩০.১২৩৪ বিবিধ  বাকেরগঞ্জ উপজেলার প্রায় 40 ভাগের পেশাই চাষাবাদ 80 and 40 ২২"
    text = nmlr.text_normalizer(text)
    print(text)
    print("+++++++++++++++++ end random test +++++++++++++++++++++++++++")
    