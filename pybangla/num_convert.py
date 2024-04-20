
import re
from num2words import num2words
from config import Config as cfg

english_digits = cfg._bangla2english_digits_mapping
bangla_numeric_words = cfg._bangla_numeric_words

class BanglaNumberConverter:
    def __init__(self):
        self.english_digits = english_digits
        self.bangla_numeric_words = bangla_numeric_words
        self.en_regex = cfg.en_regex

    def is_english_digit_string(s):
        # Check if all characters in the string are digits (0-9)
        return all(char.isdigit() for char in s)

    def number_to_words_converting_process(self, number_string:str, lang = "bn"):
        number_string = number_string.strip()
        num = int("".join([self.english_digits[bangla_digit] if lang =="bn" else bangla_digit for bangla_digit in number_string]))
        try:
            eng_in_num_to_words = num2words(num, lang='en_IN')
            if lang =="bn":
                bangla_num_to_words_list = [self.bangla_numeric_words[word] for word in eng_in_num_to_words.replace(',', ' ').replace(' and ', ' ').split()]
            else:
                bangla_num_to_words_list = [word for word in eng_in_num_to_words.replace(',', ' ').replace(' and ', ' ').split()]
            return ' '.join(bangla_num_to_words_list)
        except Exception as e:
            print(e)
            return 
        
    def number_to_words(self, number:str, chunk_millions = 7):

        en_extraction = list(re.finditer(self.en_regex, number, re.UNICODE))
        number = number[::-1]
        chunks = [
            number[i:i+chunk_millions] 
            for i in range(0, len(number), chunk_millions)
            ]
        chunks = [c[::-1] for c in chunks]
        chunks = chunks[::-1]
        if en_extraction:
            number = " crore ".join([self.number_to_words_converting_process(chunk, lang="en") for chunk in chunks])
            number = number.replace("zero", "")
        else:
            number = " কোটি ".join([self.number_to_words_converting_process(chunk, lang="bn") for chunk in chunks])
            # print(number)
            number = number.replace("শূন্য", "")


        return " ".join(number.split())
    
    # def year_in_number_to_bangla_words(year_in_number:str):
    #     """ Converts a Bangla year in numeric form to literal words.

    #     Args:
    #         number_string: Bangla year in numbers as string. Example: "১৯৯৪"

    #     Returns:
    #         Bangla year in words. Example: "উনিশশো চুরানব্বই"

    #     """
    #     if (len(year_in_number) == 4 and year_in_number[1] != '০') or len(year_in_number) == 3:
    #         return number_to_words(year_in_number[:-2]) + "শো " + number_to_words(year_in_number[-2:])
    #     else:
    #         return number_to_words(year_in_number)

if __name__ == "__main__":
    converter = BanglaNumberConverter()
    x = "১২৩৪৫৬৭৮৯২৩৬৫১১৩"
    # x = "1234567892365113"
    bangla_words = converter.number_to_words(x)
    print(bangla_words)
