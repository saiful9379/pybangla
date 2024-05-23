## 2. Number Conversion
It supports converting Bangla text numbers to numeric numbers.
```py
text = "আপনার ফোন নম্বর হলো জিরো ওয়ান ডাবল সেভেন থ্রি ডাবল ফাইভ নাইন থ্রি সেভেন নাইন"
text = nrml.word2number(text)

#output:

'আপনার ফোন নম্বর হলো 01773559379 '
```

```py
text = "দশ বারো এ এগুলা একশ একশ দুই"
text = nrml.word2number(text)
print(text)
#output:
'1012 এ এগুলা 100 102 '
```

```py
text = "এক লক্ষ চার হাজার দুইশ এক টাকা এক দুই"
text = nrml.word2number(text)
print(text)
#output:
'104201 টাকা 12 '
```
```py
text = "আমাকে এক লক্ষ দুই হাজার এক টাকা দেয় এন্ড তুমি বিশ হাজার টাকা নিও এন্ড এক লক্ষ চার হাজার দুইশ এক টাকা এক ডবল দুই"
text = nrml.word2number(text)
print(text)
#output:
'আমাকে 102001 টাকা দেয় এন্ড তুমি 20000 টাকা নিও এন্ড 104201 টাকা 122 '
```

```py
# "আমার সাড়ে পাঁচ হাজার",
# "আমার সাড়ে তিনশ",
# "আড়াই হাজার",
# "আড়াই লক্ষ",
# "ডেরশ",
# "আমাকে ডেরশ টাকা দেয়",

text = "আমাকে ডেরশ টাকা দেয়"
text = nrml.word2number(text)
print(text)

#output:
'আমাকে 150 টাকা দেয় '

```

For more test case information please check ```notebook/test.ipynb```


```py
import pybangla
nrml = pybangla.DateTranslator()
number = "২০২৩"
number = nrml.number_convert(number, language="bn")
# Output:
{'digit': '২০২৩', 'digit_word': 'দুই শূন্য দুই তিন', 'number_string': 'দুই হাজার তেইশ'}

```

```py
number = "২০২৩"
number = nrml.number_convert(number, language="en")

# Output:
{'digit': '2023', 'digit_word': 'টু জিরো টু থ্রি', 'number_string': 'two thousand twenty-three'}
```

```py
number = "2013"
number = nrml.number_convert(number, language="en")

#output

{'digit': '2013', 'digit_word': 'টু জিরো ওয়ান থ্রি', 'number_string': 'two thousand thirteen'}
```

```py

number = "2013"
number = nrml.number_convert(number, language="bn")
#output
{'digit': '২০১৩', 'digit_word': 'দুই শূন্য এক তিন', 'number_string': 'দুই হাজার তেরো'}
```