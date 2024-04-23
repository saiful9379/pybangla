import re
from banglanum2words import num_convert

bn = ["০","১","২","৩","৪","৫","৬","৭","৮","৯"]
en = ["0","1","2","3","4","5","6","7","8","9"]

en_bn = dict(map(lambda x, y: [x, y] ,en, bn ))

def convert_bn2en(en_n):
    """
    converting english digit to bangla digit
    """
    bn2en = "".join(map(lambda x: en_bn[x], en_n))
    return bn2en

def en_number(en_matches):
    """
    regex data type of to string convertion
    """
    return [match[0] for matchNum, match in enumerate(en_matches, start=1)]



def bn_number(text , bn_matches):

    """
    number to word convertion
    """
    bn_number_mapping = {'০':'শূন্য', '১':'এক', '২':'দুই', '৩':'তিন', '৪':'চার', '৫':'পাঁচ', '৬':'ছয়', '৭':'সাত', '৮':'আট', '৯':'নয়'}
    for matchNum, match in enumerate(bn_matches, start=1):
        match_span, matched_string = match.span(), match.group()
        num_str = num_convert.number_to_bangla_words(matched_string)
        text = text.replace(matched_string, num_str)
    return text

def number_processing(text):

    """
    number processing digit to word string
    """
    bn_regex, en_regex = r'[০-৯]+', r'[0-9]+'

    bn_matches = list(re.finditer(bn_regex, text, re.UNICODE))
    if bn_matches:
        text = bn_number(text, bn_matches)

    en_matches = list(re.finditer(en_regex, text, re.UNICODE))
    if en_matches:
        en_n = en_number(en_matches)
        for i in en_n:
            en_n_c = convert_bn2en(i)
            num_str = num_convert.number_to_bangla_words(en_n_c)
            text = text.replace(i, num_str)
    return text


if __name__ == "__main__":
    # text = "বাকেরগঞ্জ জেলা নামটি ১৭৯৭ থেকে ১৯৯৩ সালপর্যন্ত ছিল"
    text = "বিবিধ  বাকেরগঞ্জ উপজেলার প্রায় 40 ভাগের পেশাই চাষাবাদ 80"
    text = number_processing(text)
