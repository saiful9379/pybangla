# Text Normalization Examples

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

```py
text = "মোঃ সাইফুল ইসলাম ডাঃ রবিউল ইসলাম একসাথে বাজার যাই"
text = nrml.text_normalizer(text, all_operation=True)
print(text)
# output:
'মোহাম্মদ সাইফুল ইসলাম ডাক্তার রবিউল ইসলাম একসাথে বাজার যাই'

```

```py
text = "আজকের তাপমাত্রা ৪৪°"
text = nrml.text_normalizer(text, all_operation=True)
print(text)

#output:
'আজকের তাপমাত্রা চুয়াল্লিশ ডিগ্রী'

```

```py

text = "সম্মেলনটি সেপ্টেম্বর ০৫ ২০২৩ তারিখে নির্ধারিত করা হয়েছে. এপ্রিল ২০২৩"
text = nrml.text_normalizer(text, all_operation=True)
print(text)

#output:
'সম্মেলনটি সেপ্টেম্বর পাঁচ দুই হাজার তেইশ তারিখে নির্ধারিত করা হয়েছে . এপ্রিল দুই হাজার তেইশ'

```

```py

text = "দাড়াবে?না হারিস আনিস জোসেফের মতো খালাস!!!???"
text = nrml.text_normalizer(text, all_operation=True)
print(text)   

#output:
'দাড়াবে? না হারিস আনিস জোসেফের মতো খালাস! ?'
```

```py

text = "আজব এক ধর্ম। অবমাননার অর্থ কি ? ? কেউ বলবেন? ? মেধাহীন জাতি তা আর একবার প্রমাণ করলো ।"
text = nrml.text_normalizer(text, all_operation=True)
print(text)

#output:
'আজব এক ধর্ম। অবমাননার অর্থ কি? কেউ বলবেন? মেধাহীন জাতি তা আর একবার প্রমাণ করলো।'
```

```py
text = "সে যা-ই হোক, সত্যিকারের এমন পাকা পোনা শেষ বার নেমন্তন্ন বাড়িতে খেয়েছি ১৯৮৭-র এপ্রিলে।"
text = nrml.text_normalizer(text, all_operation=True)
print(f"{text}")

#output:
'সে যা ই হোক, সত্যিকারের এমন পাকা পোনা শেষ বার নেমন্তন্ন বাড়িতে খেয়েছি উনিশশো সাতাশি এর এপ্রিলে।'
```

```py
text = "আজকের তাপমাত্রা ৪৪°F"
text = nrml.text_normalizer(text, all_operation=True)
print(f"{text}")

#output:
'আজকের তাপমাত্রা চুয়াল্লিশ ডিগ্রী ফারেনহাইট'
```

```py
text = "নতুন নীতিমালায় ২০২৬-২৭ অর্থবছরে দেশের রপ্তানি আয় ১১ হাজার কোটি মার্কিন ডলারে উন্নীত করার ১৯৯৫ সালে লক্ষ্যমাত্রা নির্ধারণ করা হয়েছে।"
text = nrml.text_normalizer(text, all_operation=True)
print(f"{text}")

#output:
'নতুন নীতিমালায় দুই হাজার ছাব্বিশ সাতাশ অর্থবছরে দেশের রপ্তানি আয় এগারো হাজার কোটি মার্কিন ডলারে উন্নীত করার উনিশশো পঁচানব্বই সালে লক্ষ্যমাত্রা নির্ধারণ করা হয়েছে।'
```

```py
text = "আজকের তাপমাত্রা ৪৪°F"
text = nrml.text_normalizer(text, all_operation=True)
print(f"{text}")

#output:
'আজকের তাপমাত্রা চুয়াল্লিশ ডিগ্রী ফারেনহাইট'
```

```py
text = "আজকের তাপমাত্রা ৪৪°C"
text = nrml.text_normalizer(text, all_operation=True)
print(f"{text}")

#output:
'আজকের তাপমাত্রা চুয়াল্লিশ ডিগ্রী সেলসিয়াস'
```

Supported

```
#abbreviations:
("সাঃ", "সাল্লাল্লাহু আলাইহি ওয়া সাল্লাম"),                  
("আঃ", "আলাইহিস সালাম"),
("রাঃ", "রাদিআল্লাহু আনহু"),
("রহঃ", "রহমাতুল্লাহি আলাইহি"),
("রহিঃ", "রহিমাহুল্লাহ"),
("হাফিঃ", "হাফিযাহুল্লাহ"),
("দাঃবাঃ", "দামাত বারাকাতুহুম,দামাত বারাকাতুল্লাহ"),
("মোঃ",  "মোহাম্মদ"),
("মো.",  "মোহাম্মদ"),
("মোসাঃ",  "মোসাম্মত"),
("মোছাঃ", "মোছাম্মত"),
("আ:" , "আব্দুর"),
("ডাঃ" , "ডাক্তার"),
("ড." , "ডক্টর"),

#Symbols:
("&", " এন্ড"),
("@", " এট দা রেট"),
("%", " পারসেন্ট"),
("#", " হ্যাশ"),
("°", " ডিগ্রী")

#Currency

("৳", "টাকা"), 
("$", "ডলার"), 
("£", "পাউন্ড"), 
("€", "ইউরো"), 
("¥", "ইয়েন"), 
("₹", "রুপি"), 
("₽", "রুবেল"), 
("₺", "লিরা")

```

