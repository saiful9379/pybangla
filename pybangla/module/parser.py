from ast import pattern
import re
import datetime
import string
from .config import Config as cfg
from num2words import num2words
from .date_extractor import DateExtractor
from fuzzywuzzy import fuzz
from loguru import logger
# from bnemo import Translator
from .phone_number_extractor import PhoneNumberExtractor
from .nid_num_normalize import NIDNormalizer
from .passport_num_normalize import PassportFormatter
from .product_unit_normalization import UnitNormalization
from .product_number import ProductNormalizer
from .driving_license import DrivingLicenseParser, DrivingLicenseFormatter
from .symbol_conversion import SymbolNormalizer
from .number_service import NumberNormalizationService
from .email_url_normalization import EmailURLExtractor
from .ordinals_normalizaiton import OrdinalConverter
from .helpline_extractor import HelplineExtractor
from .security_code import security_code_normalizer


dt = DateExtractor()
pne = PhoneNumberExtractor()
nid_normalizer = NIDNormalizer()
un = UnitNormalization()
pn = ProductNormalizer(debug=False)
dlf = DrivingLicenseFormatter()
symn = SymbolNormalizer()
nns = NumberNormalizationService()
eue = EmailURLExtractor()
oc = OrdinalConverter()
hle = HelplineExtractor()
data = cfg.data

_abbreviations = cfg._abbreviations
_symbols = cfg._symbols
_ordinal_re = cfg._ordinal_re
_whitespace_re = cfg._whitespace_re
_currency = cfg._currency
_punctuations = cfg._punctuations

english_digits = cfg._bangla2english_digits_mapping
bangla_numeric_words = cfg._bangla_numeric_words

_STANDARDIZE_ZW = cfg._STANDARDIZE_ZW
_DELETE_ZW = cfg._DELETE_ZW


def extract_bengali_dates_with_spans(text):
    """Extract Bengali dates from text with their span positions"""
    
    # Define the regex pattern
    pattern = r'(?:(?:(?:[০-৯]{1,2}(?:ই|শে|রা|ঠা)?)\s*(?:জানুয়ারি|ফেব্রুয়ারি|মার্চ|এপ্রিল|মে|জুন|জুলাই|আগস্ট|সেপ্টেম্বর|অক্টোবর|নভেম্বর|ডিসেম্বর))|(?:(?:জানুয়ারি|ফেব্রুয়ারি|মার্চ|এপ্রিল|মে|জুন|জুলাই|আগস্ট|সেপ্টেম্বর|অক্টোবর|নভেম্বর|ডিসেম্বর)\s+[০-৯]{1,2}))(?:,)?\s+[০-৯]{4}'
    
    # Find all matches with span positions
    matches = []
    for match in re.finditer(pattern, text):
        matches.append({
            'text': match.group(0),
            'start': match.start(),
            'end': match.end(),
            'span': match.span()
        })
    
    return matches

def parse_bengali_date(text):
    """Extract Bengali dates including written-out number formats"""
    
    # Bengali number words mapping
    bengali_number_words = {
        # Days (1-31)
        'এক': '১', 'দুই': '২', 'তিন': '৩', 'চার': '৪', 'পাঁচ': '৫',
        'ছয়': '৬', 'সাত': '৭', 'আট': '৮', 'নয়': '৯', 'দশ': '১০',
        'এগারো': '১১', 'বারো': '১২', 'তেরো': '১৩', 'চৌদ্দ': '১৪', 'পনেরো': '১৫',
        'ষোল': '১৬', 'সতেরো': '১৭', 'আঠারো': '১৮', 'উনিশ': '১৯', 'বিশ': '২০',
        'একুশ': '২১', 'বাইশ': '২২', 'তেইশ': '২৩', 'চব্বিশ': '২৪', 'পঁচিশ': '২৫',
        'ছাব্বিশ': '২৬', 'সাতাশ': '২৭', 'আটাশ': '২৮', 'ঊনত্রিশ': '২৯', 'ত্রিশ': '৩০',
        'একত্রিশ': '৩১'
    }
    
    # Year words pattern (complex due to Bengali number system)
    year_pattern_words = r'(?:এক হাজার নয়শো নব্বই|দুই হাজার|উনিশশো|বিশ শতক)'
    
    # Create pattern for day numbers (both digits and words)
    day_words = '|'.join(bengali_number_words.keys())
    day_pattern = f'(?:[০-৯]{{1,2}}|{day_words})'
    
    # Month names
    months_pattern = r'(?:জানুয়ারি|ফেব্রুয়ারি|মার্চ|এপ্রিল|মে|জুন|জুলাই|আগস্ট|সেপ্টেম্বর|অক্টোবর|নভেম্বর|ডিসেম্বর)'
    
    # Combined patterns
    patterns = [
        # Pattern 1: Regular digit format
        r'(?:(?:[০-৯]{1,2})\s*(?:ই|শে|রা|ঠা)?\s*' + months_pattern + r')(?:,)?\s+[০-৯]{4}',
        # Pattern 2: Month first digit format
        months_pattern + r'\s+[০-৯]{1,2}(?:,)?\s+[০-৯]{4}',
        # Pattern 3: Written day with month and digit year
        f'(?:{day_pattern})\\s*(?:ই|শে|রা|ঠা)?\\s*{months_pattern}(?:,)?\\s+[০-৯]{{4}}',
        # Pattern 4: Written day and year
        f'(?:{day_pattern})\\s*(?:ই|শে|রা|ঠা)?\\s*{months_pattern}(?:,)?\\s+{year_pattern_words}'
    ]
    
    all_matches = []
    
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            all_matches.append({
                'text': match.group(0),
                'start': match.start(),
                'end': match.end(),
                'span': match.span(),
                'type': 'word_format' if any(word in match.group(0) for word in bengali_number_words.keys()) else 'digit_format'
            })

    return all_matches

def extract_consecutive_numbers_with_separators(text):
    """Extract consecutive numbers separated by spaces and/or hyphens, maintaining language consistency"""
    
    # Pattern for Bengali consecutive numbers (only Bengali digits)
    bengali_pattern = r'(?<![০-৯\.])[০-৯]+(?:[\s\-]+[০-৯]+)+(?![০-৯\.])'
    
    # Pattern for English consecutive numbers (only English digits)
    english_pattern = r'(?<![0-9\.])\d+(?:[\s\-]+\d+)+(?![0-9\.])'
    
    # Process each pattern separately to maintain language consistency
    all_matches = []
    
    # Find Bengali patterns
    for match in re.finditer(bengali_pattern, text):
        matched_text = match.group(0)
        # Verify it contains ONLY Bengali digits
        if not re.search(r'[0-9]', matched_text):  # No English digits
            all_matches.append((match, 'bengali'))
    
    # Find English patterns  
    for match in re.finditer(english_pattern, text):
        matched_text = match.group(0)
        # Verify it contains ONLY English digits
        if not re.search(r'[০-৯]', matched_text):  # No Bengali digits
            all_matches.append((match, 'english'))
    
    # Sort all matches by position in reverse order
    reversed_sorted = sorted(all_matches, key=lambda x: x[0].start(), reverse=True)
    
    # print("reversed_sorted : ", [m[0] for m in reversed_sorted])
    
    for match, num_type in reversed_sorted:
        matched_text = match.group(0)
        
        # Extract individual numbers
        if num_type == 'bengali':
            numbers = re.findall(r'[০-৯]+', matched_text)
        else:  # english
            numbers = re.findall(r'\d+', matched_text)

        if len(numbers) == 2:
            continue
            
        data_map = data['bn']["number_mapping"]
        number_list = []
        
        for n in numbers:
            internal_digits = []
            for i in n:
                if i in data_map:
                    word = data_map[i]
                    internal_digits.append(word)

            word = " ".join(internal_digits)
            number_list.append(word)

        number_string = ", ".join(number_list)
        text = text.replace(matched_text, " " + number_string + " ")

    # print("final text : ", text)
    return text

class NumberParser:
    def __init__(self):
        self.english_digits = english_digits
        self.bangla_numeric_words = bangla_numeric_words
        self.en_regex = cfg.en_regex
        self.bn_regex = cfg.bn_regex

    def is_english_digit_string(self, s):
        # Check if all characters in the string are digits (0-9)
        return all(char.isdigit() for char in s)

    def contains_only_english(self, input_string):
        # Check if all characters in the string are English (ASCII) characters
        return all(ord(char) < 128 for char in input_string)

    def number_to_words_converting_process(self, number_string: str, lang="bn"):
        number_string = number_string.strip()

        # print("number_string 1: ", number_string)
        num = int(
            "".join(
                [
                    self.english_digits[bangla_digit] if lang == "bn" else bangla_digit
                    for bangla_digit in number_string
                ]
            )
        )
        try:
            eng_in_num_to_words = num2words(num, lang="en_IN")
            if lang == "bn":
                bangla_num_to_words_list = [
                    self.bangla_numeric_words[word]
                    for word in eng_in_num_to_words.replace(",", " ")
                    .replace(" and ", " ")
                    .split()
                ]
            else:
                bangla_num_to_words_list = [
                    cfg._banglish_pronunciation_bn[word]
                    for word in eng_in_num_to_words.replace(",", " ")
                    .replace(" and ", " ")
                    .split()
                ]
            # print("number_string : ", bangla_num_to_words_list)
            return " ".join(bangla_num_to_words_list)
            
        except Exception as e:
            print(e)
            return

    def number_to_words(self, number: str, chunk_millions=7, language="bn"):

        en_extraction = list(re.finditer(self.en_regex, number, re.UNICODE))
        # print("en_extraction : ", en_extraction[1])
        # print("number_to_words : ", number, language)
        if en_extraction and language != "en":
            number = self._digit_converter(number)


        # self._digit_converter
        number = number[::-1]
        # print("number : ", number)
        chunks = [
            number[i : i + chunk_millions]
            for i in range(0, len(number), chunk_millions)
        ]
        chunks = [c[::-1] for c in chunks]
        chunks = chunks[::-1]

        # print("en_extraction : ", en_extraction)
        if en_extraction and language=="en":
            number = " কোর ".join(
                [
                    self.number_to_words_converting_process(chunk, lang="en")
                    for chunk in chunks
                ]
            )
            number = number.replace("zero", "")
            # print("number : ", number)
        else:
            number = " কোটি ".join(
                [
                    self.number_to_words_converting_process(chunk, lang="bn")
                    for chunk in chunks
                ]
            )
            # print(number)
            number = number.replace("শূন্য", "")
        # print("number.split() : ", number.split())

        return (" ".join(number.split())).replace(" শো", "শো")

    def digit_number_to_digit_word(self, number, language="bn"):

        number = re.sub(_whitespace_re, " ", number)

        # print("digit_number_to_digit_word : ", number, language)
        s_n = ""
        for i in number:
            n = data[language]["number_mapping"][i]
            s_n += " " + n
        return s_n.strip()

    def year_in_number(self, year_in_number: str, language="bn"):
        """Converts a Bangla year in numeric form to literal words.

        Args:
            number_string: Bangla year in numbers as string. Example: "১৯৯৪"

        Returns:
            Bangla year in words. Example: "উনিশশো চুরানব্বই"

        """

        # print("year_in_number : ", year_in_number, language)

        english_status = self.contains_only_english(year_in_number)
        if english_status:
            year_in_number = "".join(
                [cfg._english2bangla2_digits_mapping[i] for i in year_in_number]
            )
        if language == "bn":
            mid_text = "শো "
        else:
            mid_text = " century "

        if (len(year_in_number) == 4 and year_in_number[1] != "০") or len(
            year_in_number
        ) == 3:
            # print("year in ")

            if year_in_number[1] != "0":
                year_str = self.number_to_words(year_in_number)
            return (
                self.number_to_words(year_in_number[:-2])
                + mid_text
                + self.number_to_words(year_in_number[-2:])
            )
        else:
            # print("+++++++++ else+++++++++++++++")
            return self.number_to_words(year_in_number)

    def _replace_starting_zero(self, month):
        """
        Normalize string which start zero first

        """
        if month[0] == "0" or month[0] == "০":
            return month[1:]
        return month

    def _digit_converter(self, number, language="bn"):
        """
        convert the digit En to Bn or Bn to En

        """
        # print("number  : ", number, language)

        if language == "en":
            extracted_number = list(re.finditer(self.bn_regex, str(number), re.UNICODE))
            if extracted_number:
                # print("language", number)
                # [i[1] for i in number if i[0]=="0"]
                if number[0] == "0":
                    number = number[1:]
                number = "".join(
                    [
                        cfg._bangla2english_digits_mapping[i.replance(",", "")]
                        for i in number
                        if i[0] == "0"
                    ]
                )
                # print("extracted : ", number)
        c_number = ""
        for n in number:
            n = n.replace(",", "")
            if n:
                if n in data[language]["number"]:
                    c_number += n
                else:
                    if n.strip() in data[language]["digits_mapping"]:
                        b_n = data[language]["digits_mapping"][n.strip()]
                        c_number += b_n
                    # else:
                    #     print("else: ", n)
                    #     c_number += n
        # print(c_number)
        return c_number

    def get_weekday(self, date_: list = [], language="bn"):
        """
        Get weekday name Bangla or English

        """

        # print("date_", date_)
        try:
            if date_[0] is None or date_[1] is None or date_[2] is None:
                return None
            elif date_[1].isdigit():
                if int(date_[1]) > 12:
                    return None
            d, y = list(re.finditer(self.bn_regex, str(date_[0]), re.UNICODE)), list(
                re.finditer(self.bn_regex, str(date_[2]), re.UNICODE)
            )

            if d:
                date_[0] = self._digit_converter(date_[0], language="bn")
            if y:
                date_[2] = self._digit_converter(date_[2], language="bn")

            current_date_object = datetime.datetime(
                int(date_[2]), int(date_[1]), int(date_[0])
            )
            if language in data:
                weekday = data[language]["weekdays"][current_date_object.weekday()]
            else:
                print("language not handel")
                weekday = ""
        except:
            weekday = None
        # print("weekday : ", weekday)
        return weekday

    def search_month(self, search_key, language="bn"):
        """
        Search for a month or month abbreviation in the month_data dictionary.

        Args:
            search_key (str): The month or its abbreviation to search for.
            language (str, optional): Language identifier ("bn" for Bengali, "en" for English).
                Defaults to "bn".

        Returns:
            list: A list containing additional information about the month if found,
            formatted based on the specified language.
            The list contains [month_name, season_name, number_of_days].
            If the month or abbreviation is not found, returns [None, None, None].
        """
        try:
            search_key = int(self._replace_starting_zero(search_key)) - 1
            month = data[language]["months"][search_key]
            seasons = data[language]["seasons"][search_key // 2]
            option_name = data[language]["option_name"][search_key]
        except:
            month, option_name, seasons = None, None, None
        return [month, option_name, seasons]

    def find_word_index(self, text: str, word: str) -> list:
        """
        Word spanning position
        """
        start = text.find(word)
        end = start + len(word)
        return [start, end]

    def replace_text_at_position(
        self, text: str, replacement: str, start_pos: int, end_pos: int
    ) -> str:
        """
        Replance text using text position

        """
        rep_text = text[:start_pos] + replacement + text[end_pos:]
        return rep_text

    def fraction_number_conversion(self, number, language="bn"):

        if language == "bn":
            n_n = ""
            for i in number:
                if i in cfg._english2bangla2_digits_mapping:
                    n_n += cfg._english2bangla2_digits_mapping[i]
                else:
                    n_n += i
        else:
            n_n = number

        # print("n_n : ", n_n)

        s_m = n_n.split(".")
        # print("sm : ", s_m)
        before_dot_word, after_dot_word = self.number_to_words(
            s_m[0], language=language
        ), self.digit_number_to_digit_word(s_m[1], language=language)

        if before_dot_word in cfg._banglish_pronunciation_bn:
            before_dot_word = cfg._banglish_pronunciation_bn[before_dot_word]
        if len(after_dot_word):
            if language == "bn":    
                word = before_dot_word + " দশমিক " + after_dot_word
            else:
                word = before_dot_word + " পয়েন্ট " + after_dot_word
            return word
        return before_dot_word

    def check_comma_dot_dari(self, p):
        l_p = [",", ".", "।"]
        if p in l_p:
            return True
        return False

    def bai_extraction_pattern(self, text):
        # print("text bhai: ", text)
        pattern = r'([০-৯0-9]{1,2}/[০-৯0-9]{1})'
        matches = [(match.group(), match.start(), match.end()) for match in re.finditer(pattern, text)]
        sorted_matches = matches[::-1]
        # print("matches : ", sorted_matches)
        for p in sorted_matches:
            match_str, starting_position, ending_position = p[0], p[1], p[2]
            # ending_position = self.find_word_index(text, p)[1]
            # print("p : ", p)
            split_p = match_str.split("/")
            # print("split_p : ", split_p)
            if split_p and len(split_p) == 2:
                # print("split_p : ", split_p)
                first_lang = "en" if self.contains_only_english(split_p[0]) else "bn"
                second_lang = "en" if self.contains_only_english(split_p[1]) else "bn"
                first_num = self.number_to_words(split_p[0], language=first_lang)
                second_num = self.number_to_words(split_p[1], language=second_lang)
                # print("first_num : ", first_num, " second_num : ", second_num)    
                if first_num in cfg._banglish_pronunciation_bn:
                    first_num = cfg._banglish_pronunciation_bn[first_num]
                if second_num in cfg._banglish_pronunciation_bn:
                    second_num = cfg._banglish_pronunciation_bn[second_num]
                # print("=====first_num : ", first_num, " second_num : ", second_num)
                norm_string = f"{first_num} বাই {second_num}"
                text = text[:starting_position] + " " + norm_string + " " + text[ending_position:]
        return text
    

    def time_processing(self, text):
        """
        Process time in the text
        """
        pattern = r"(\d{1,2}:\d{2}(:\d{2})?)\s*(টায়|টা)?"
        matches = [(match.group(), match.group(1), match.group(3), match.start(), match.end())
                for match in re.finditer(pattern, text)]
        # Sort matches based on position (reversed for replacement)
        sorted_matches = sorted(matches, key=lambda x: x[3], reverse=True)

        for full_match, time_only, suffix, start_position, end_position in sorted_matches:
            # print(f"Found: '{full_match}' at position {start_position}-{end_position}")
            # print(f"Time: '{time_only}', Suffix: '{suffix}'")
            if ":" in time_only:
                parts = time_only.split(":")

                if len(parts) == 3:
                    hours, minutes, seconds = parts
                    first_num = self.number_to_words(hours, language="bn")
                    second_num = self.number_to_words(minutes, language="bn")
                    third_num = self.number_to_words(seconds, language="bn")
                    # Check if original had suffix and if it's hour-only
                    has_suffix = suffix is not None
                    if third_num:  # Has seconds
                        if second_num:
                            norm_string = f"{first_num}টা {second_num} মিনিট {third_num} সেকেন্ড"
                        else:
                            norm_string = f"{first_num}টা {third_num} সেকেন্ড"
                    else:  # No seconds
                        if second_num:  # Has minutes
                            norm_string = f"{first_num}টা {second_num} মিনিট"
                        else:  # Only hours
                            if has_suffix:
                                # Keep original suffix format
                                norm_string = f"{first_num} {suffix}"
                            else:
                                norm_string = f"{first_num}টা"

                elif len(parts) == 2:
                    hours, minutes = parts
                    first_num = self.number_to_words(hours, language="bn")
                    second_num = self.number_to_words(minutes, language="bn")
                    # Check if original had suffix
                    has_suffix = suffix is not None
                    if second_num and minutes != "00":  # Has non-zero minutes
                        norm_string = f"{first_num}টা {second_num} মিনিট"
                    else:  # Only hours (minutes are 00)
                        if has_suffix:
                            # Keep original suffix format
                            norm_string = f"{first_num} {suffix}"
                        else:
                            norm_string = f"{first_num}টা"
                text = text[:start_position] + " " + norm_string + " " + text[end_position:]

        return text

    def number_processing(self, text):
        text, s_match  = security_code_normalizer(text)
        # print("replaced_text : ", text)
        text = extract_consecutive_numbers_with_separators(text)

        # print("befor processing text : ", text)
        text = self.bai_extraction_pattern(text)
        # print("bai_extraction_pattern text : ", text)
        text = self.time_processing(text)

        pattern = r"[\d,\.]+"  # Matches numbers with commas and periods
        matches = [(match.group(), match.start(), match.end()) for match in re.finditer(pattern, text)]
        
        # Sort matches based on length (longest first)
        sorted_matches = sorted(matches, key=lambda x: len(x[0]), reverse=True)


        org_text = text
        # print("text : ", org_text)
        
        for n_with_p in sorted_matches:
            # print(n_with_p)
            n = n_with_p[0]
            end_position = n_with_p[2]
            ti_status = False
            if len(org_text)-2 >= end_position:
                if org_text[end_position:end_position+2]=="টি":
                    ti_status = True
                # print("index + text", org_text[end_position:end_position+2])
            # print("position : ", end_position)

            p_status = self.check_comma_dot_dari(n)
            if p_status:
                text = text.replace(n, " " + n + " ")
                # print("p_status : ", text)
            else:
                status = self.contains_only_english(n)
                # print("status : ", status)
                m_re = n.replace(",", "")
                if status:

                    if "." in m_re:
                        bn_m = self.fraction_number_conversion(m_re, language="en")
                    else:

                        # print("m_re saiful : ", m_re)
                        # print("m_re : ", self._digit_converter(m_re))
                        bn_m = self.number_to_words(m_re, language="en")
                        # print("bn_m : ", bn_m)
                        if bn_m in cfg._banglish_pronunciation_bn:
                            bn_m = cfg._banglish_pronunciation_bn[bn_m]
                    # if ti_status= ""
                    if ti_status:
                        text = text.replace(n, " " + str(bn_m))
                    else:
                        text = text.replace(n, " " + str(bn_m) + " ")
                else:
                    if "." in m_re:
                        bn_m = self.fraction_number_conversion(m_re, language="bn")
                    else:
                        
                        bn_m = self.number_to_words(m_re)
                    # print("else : bn_m ", n, bn_m)
                    if n=="০" and len(bn_m.strip())==0:
                        bn_m = "শূণ্য"
                    elif n=="0" and len(bn_m.strip())==0:
                        bn_m = "জিরো"

                    if ti_status:
                        text = text.replace(str(n), " " + str(bn_m))
                    else:
                        text = text.replace(str(n), " " + str(bn_m)+" ")

        text = re.sub(cfg._whitespace_re, " ", text)
    
        text = re.sub(r"\s*,\s*", ", ", text)
        # print("processing text : ", text)

        return text


class DateParser:
    def __init__(self):
        self.samples = cfg.samples

        self.npr = NumberParser()

    def data_splitter(self, date_string):
        """ """
        separator_pattern = "|".join(map(re.escape, self.samples))
        return re.split(separator_pattern, date_string)

    def month_convert_to_number(self, month):
        """ """
        index = None
        # print("month", month)
        key = month.lower().strip()
        if key in data["en"]["months"]:
            index = data["en"]["months"].index(key) + 1
        elif key in data["bn"]["months"]:
            index = data["bn"]["months"].index(key) + 1
        elif key in data["bn"]["option_name"]:
            index = data["bn"]["option_name"].index(key) + 1
        elif key in data["en"]["option_name"]:
            index = data["en"]["option_name"].index(key) + 1
        elif key in data["en"]["number"]:
            index = data["en"]["number"].index(key) + 1
        elif key in data["bn"]["number"]:
            index = data["bn"]["number"].index(key) + 1
        else:
            key = key.strip()
            if key[-1] in string.punctuation:
                index = key[:-1]
        return index

    def format_non_punctuation(self, split_date):
        """ """
        if len(split_date[0]) == 8:
            if int(split_date[0][4:6]) <= 12:
                year, month, day = (
                    split_date[0][:4],
                    split_date[0][4:6],
                    split_date[0][6:],
                )
            else:
                year, month, day = (
                    split_date[0][4:],
                    split_date[0][2:4],
                    split_date[0][:2],
                )
            return [day, month, year]
        else:
            print("This date format is not handled yet")
        return None

    def get_day_and_month(self, year_idx, idx, date_list):
        """ """
        if year_idx == 0:
            return self.get_day_and_month_helper(idx, date_list, 1, 2)
        elif year_idx == 2:
            return self.get_day_and_month_helper(idx, date_list, -1, -2)
        else:
            print("Date format not handled yet")
        return None, None

    def get_day_and_month_helper(self, idx, date_list, offset1, offset2):
        """ """
        if date_list[idx + offset1].isdigit() and date_list[idx + offset2].isdigit():
            return date_list[idx + offset2], date_list[idx + offset1]
        elif (
            not date_list[idx + offset1].isdigit()
            and date_list[idx + offset2].isdigit()
        ):
            return date_list[idx + offset2], self.month_convert_to_number(
                date_list[idx + offset1]
            )
        elif (
            date_list[idx + offset1].isdigit()
            and not date_list[idx + offset2].isdigit()
        ):
            return date_list[idx + offset1], self.month_convert_to_number(
                date_list[idx + offset2]
            )
        else:
            print("Date format not handled yet")
        return None, None

    def get_date_indexes(self, date_list):
        """
        Get Date index
        """

        # print(date_list)
        day, month, year = None, None, None
        for idx, elem in enumerate(date_list):
            if elem.isdigit() and len(elem) == 4:
                year_idx = idx
                year = date_list[idx]
                # print(year)
                day, month = self.get_day_and_month(year_idx, idx, date_list)
                # print(day, month)
        return [day, month, year]

    def date_processing(self, date_, slash_status=True, language="bn"):

        # print(date_)
        if isinstance(date_, list):
            if len(date_):
                formatted_date = date_
        else:
            split_date = self.data_splitter(date_)
            # print("split_date : ", split_date)
            split_date = [i for i in split_date if i]
            # print("split_date : ", split_date)
            if len(split_date) == 2:
                adding_date = ["1"] if language == "en" else ["১"]
                split_date = adding_date + split_date

            if len(split_date) == 1:
                formatted_date = self.format_non_punctuation(split_date)
            else:
                # print("hello")
                formatted_date = self.get_date_indexes(split_date)

                # print("formatted_date :", formatted_date)

        if (
            formatted_date[0] is None
            and formatted_date[1] is None
            and formatted_date[2] is None
        ):
            current_date_object = datetime.date.today()
            formatted_date = [
                current_date_object.day,
                current_date_object.month,
                current_date_object.year,
            ]

        elif formatted_date[1] == None:
            for i in split_date:
                if formatted_date[0] == i or formatted_date[2] == i:
                    continue
                m_numeric = self.month_convert_to_number(i)
                if m_numeric:
                    formatted_date[1] = cfg._english2bangla2_digits_mapping[
                        str(m_numeric)
                    ]

        # print("final formated date : ", formatted_date)

        if (
            formatted_date[0] is not None
            and formatted_date[1] is not None
            and formatted_date[2] is not None
        ):
            weekday = self.npr.get_weekday(formatted_date, language)
        else:
            weekday = None

        if formatted_date[0] is None:
            day = None
            txt_date = None
        else:
            day = self.npr._digit_converter(str(formatted_date[0]), language)
            txt_date = self.npr.number_to_words(day)
        if formatted_date[1] is None:
            month = [None, None, None]
            m_n = None
        else:
            m_n = self.npr._digit_converter(str(formatted_date[1]), language)
            month = self.npr.search_month(str(formatted_date[1]), language)
        if formatted_date[2] is None:
            year = None
            txt_year = None
        else:
            year = self.npr._digit_converter(str(formatted_date[2]), language)
            txt_year = self.npr.year_in_number(year, language=language)

        return {
            "date": day,
            "month": m_n,
            "year": year,
            "txt_date": txt_date,
            "txt_month": month[0],
            "txt_year": txt_year,
            "weekday": weekday,
            "ls_month": month[1],
            "seasons": month[2],
        }


class TextParser:

    def __init__(self):
        self.year_patterns = [
            "সালের",
            "সালে",
            "শতাব্দী",
            "শতাব্দীর",
            "শতাব্দীতে",
            "সাল",
            "খ্রিস্টাব্দ",
            "খ্রিস্টাব্দের",
            "খ্রিস্টপূর্বাব্দের",
            "তারিখের",
            "তারিখ"
        ]
        self.year_pattern = (
            r"(?:\b|^\d+)(\d{4})\s*(?:সালে?র?|শতাব্দী(?:র)?|শতাব্দীতে|এর|তারিখের|তারিখ)+"
        )
        self.currency_pattern = (
            r"(?:\$|£|৳|€|¥|₹|₽|₺|₽)?(?:\d+(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)"
        )
        # self.currency_pattern = re.compile(r"(?:\$|£|৳|€|¥|₹|₽|₺)?(?:[\d০-৯]+(?:,[\d০-৯]{3})*(?:\.[\d০-৯]+)?|[\d০-৯]+(?:\.[\d০-৯]+)?)")
        self.npr = NumberParser()
        self.dp = DateParser()
        self.nid_normalizer = NIDNormalizer()
    def collapse_whitespace(self, text):
        # print("text : ", text)
        text = re.sub(_whitespace_re, " ", text)
    
        text = re.sub(r"\s*,\s*", ", ", text)

        # print("text : ", text)
        return text

    def phone_number_processing(self):
        pass

    def birth_year(self, text):
        patterns = [
            # Bengali patterns with birth context
            r'(?:জন্ম|জন্মগ্রহণ)\s*(?:সাল)?\s*[:\-]?\s*([০-৯]{4}|\d{4})',
            r'(?:জন্ম|জন্মগ্রহণ).*?([০-৯]{4}|\d{4})\s*(?:সালে?|খ্রিস্টাব্দে?)',
            
            # English patterns with birth context
            r'(?:birth|born|dob)\s*(?:date|year|in)?\s*[:\-]?\s*([০-৯]{4}|\d{4})',
            r'(?:birth|born|dob).*?([০-৯]{4}|\d{4})',
            
            # Mixed patterns (Bengali text with English keywords)
            r'(?:বার্থ|বর্ন)\s*(?:ডেট|ইয়ার)?\s*[:\-]?\s*([০-৯]{4}|\d{4})',
            
            # Pattern for "সালে জন্ম" type
            r'([০-৯]{4}|\d{4})\s*সালে\s*(?:জন্ম|জন্মগ্রহণ)',
            
            # Birth year with context words nearby (within 10 characters)
            r'(?:জন্ম|birth|born|dob|বার্থ).{0,10}([০-৯]{4}|\d{4})',
            r'([০-৯]{4}|\d{4}).{0,10}(?:জন্ম|birth|born|সালে জন্ম)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text)
            sorted_matches = sorted(matches, key=lambda x: x.group(), reverse=True)
            for match in sorted_matches:
                # print("birth year match : ", match)
                if match is None:
                    continue
                birth_year_word = self.npr.year_in_number(match.group(1))
                start_pos, end_pos = match.span(1)
                group_word = (match.group()).replace(match.group(1), birth_year_word)
                # print("group_word : ", group_word)
                # text = text[:start_pos] + group_word + text[end_pos:]
                text = text.replace(match.group(0), group_word)
        return text 



    def exception_year_processing(self, text):

        extracted_date = parse_bengali_date(text)
        # print("extracted_date : ", extracted_date)
        if extracted_date:
            for ed in extracted_date:
                d_e = ed["text"]
                year = re.findall(r"\d{4}|[০-৯]{4}", d_e)
                if not year:
                    continue
                year_in_word = self.npr.year_in_number(year[0])
                replace_text = d_e.replace(year[0], year_in_word+", ")
                day = re.findall(r"\b\d{1,2}\b|\b[০-৯]{1,2}\b", d_e)
                if day:
                    day_in_word = self.npr.number_to_words(day[0])
                    replace_text = replace_text.replace(day[0], day_in_word)
                # print("replace_text : ", replace_text)
                text = text.replace(d_e, replace_text)

        # print("text 1.5 ", text)

        text = self.birth_year(text)
        # print("text 1.5 ", text)
        _year_with_hyphen = re.findall(r"\b(\d{4}[-–—―]\d{2})\b", text)
        replce_map = {}
        for year in _year_with_hyphen:
            rep_year = year.replace("–", "-")
            rep_year = rep_year.replace("—", "-")
            rep_year = rep_year.replace("―", "-")
            four_digit_year, two_digit_year = rep_year.split("-")

            en_status_four = self.npr.is_english_digit_string(four_digit_year)
            en_status_two = self.npr.is_english_digit_string(two_digit_year)

            if en_status_four:
                four_digit_year = self.npr._digit_converter(
                    four_digit_year, language="bn"
                )
            if en_status_two:
                two_digit_year = self.npr._digit_converter(
                    two_digit_year, language="bn"
                )

            rep_year = (
                self.npr.year_in_number(four_digit_year)
                + " "
                + self.npr.number_to_words(two_digit_year)
            )
            text = text.replace(year, rep_year)
        # print("text 1: ", text)
        return text

    def unwanted_puntuation_removing(self, text):

        # https://stackoverflow.com/questions/63256077/how-to-remove-redundant-punctuations-keep-only-the-first-one-in-text
        def my_replace(match):
            match = match.group()
            return match[0] + (" " if " " in match else "")

        # _redundent_punc_removal = r"[!\"#%&\'()*+,\-.\/:;<=>?@\[\\\]^_`।{|}~ ]{2,}"
        _redundant_punc_removal = r"([!\"#%&'()*+,\-./:;<=>?@\[\\\]^_`।{|}~ ])\1+"
        _remove_hyphen_slash = r"(?<!\d)[-/](?!\d)"
        _remove_comma = r"(?<=\d),(?=\d)"
        _remove_space_in_punctuations = r"(?<=[^\w\s])\s+(?=[^\w\s])"

        text = _STANDARDIZE_ZW.sub("\u200D", text)
        text = _DELETE_ZW.sub("", text)

        text = text.replace("'র", " এর")
        text = text.replace("-র", " এর")
        text = text.replace("\uf038", " ")
        text = text.replace("°F", "° ফারেনহাইট")
        text = text.replace("° F", "° ফারেনহাইট")
        text = text.replace("°C", "° সেলসিয়াস")
        text = text.replace("° C", "° সেলসিয়াস")
        text = text.replace("-সালের", " সালের")
        text = text.replace("-সাল", " সাল")
        text = text.replace(".com", " ডট কম ")
        text = re.sub(r'(?<=\s)সেমি(?=\s)', 'সেন্টিমিটার', text)
        # Case 2: "সেমি" at the end of the sentence (followed by the end of the string or punctuation)
        text = re.sub(r'(?<=\s)সেমি(?=$|\s|[.,!?])', 'সেন্টিমিটার', text)
        # text = re.sub(r'(?<=\s)NID(?=$|\s|[.,!?])', 'এনআইডি', text)
        text = re.sub(r'(?<=\s)NID(?=\s)|^NID|(?<=\s)NID(?=\.$)', 'এনআইডি', text)
        text = re.sub(r'\b[eE][\-\‐ ]passport\b', 'ই-পাসপোর্ট', text)
        text = re.sub(_remove_space_in_punctuations, "", text)
        text = re.sub(_redundant_punc_removal, r"\1", text).strip()
        # print("text pun1.3 : ", text)
        text = re.sub(_remove_comma, "", text)
        text = re.sub(_remove_hyphen_slash, " ", text)

        # print("text pun1.5 : ", text)
        translation_table = str.maketrans(_punctuations)
        text = text.translate(translation_table)
        # print("text pun2 : ", text)
        return text

    def expand_symbols(self, text, lang="bn"):
        # print("text 1", text)
        for key, replacement in _symbols[lang]:
            text = text.replace(key, replacement+" ")
        # print("text : ", text)
        return text.strip()

    def expand_abbreviations(self, text, lang="bn"):
        """Replace abbreviations in Bangla text with full forms."""
        # print("text : ", text)
        bengali_letter = r'[\u0980-\u09FF]'  # Full Bengali Unicode block
    
        abbreviations = [
            # Pattern for মোছা/মোসা variations (female prefix)
            (r'\b(মোছা[:।.]|মোসা[:।.])\s*', 'মোছাম্মত '),
            
            # Pattern for মো variations - must be followed by Bengali letters
            (r'\b(মো[:।.]|মোঃ)\s*(?=' + bengali_letter + ')', 'মোহাম্মদ '),
            
            # Pattern for মুহা variations
            (r'\b(মুহা[:।.])\s*', 'মুহাম্মদ '),
            
            # Pattern for ইঞ্জি variations
            (r'\b(ইঞ্জিঃ|ইঞ্জি[।.]|ইঞ্জি:)\s*', 'ইঞ্জিনিয়ার '),
            
            # Pattern for লি variations (Limited)
            (r'\b(লিঃ|লি[।.]|লি:)\s*', 'লিমিটেড '),
            
            # Additional common abbreviations
            (r'\bডাঃ\s*', 'ডাক্তার '),
            (r'\bড[।.]\s*', 'ডাক্তার '),
            (r'\bপ্রঃ\s*', 'প্রফেসর '),
            (r'\bসিঃ\s*', 'সিনিয়র '),
            (r'\bজুঃ\s*', 'জুনিয়র '),
            (r'\bকোঃ\s*', 'কোম্পানি '),
        ]
        
        # Apply replacements
        for pattern, replacement in abbreviations:
            text = re.sub(pattern, replacement, text)
        
        text = re.sub(r'\bসেমি[ .]', 'সেন্টিমিটার ', text)
        text = re.sub(r'\bকিমি[ .]', 'কিলোমিটার ', text)
        text = re.sub(r"\bড\.\s*(?=[অ-৺])", "ডক্টর ", text)

        text = text.replace("MM-DD-YYYY", "Month, Day and Year")
        text = text.replace("DD-MM-YYYY", "Day, Month and Year")
        text = text.replace("YYYY-MM-DD", "Year, Month and Day")
        text = text.replace("YYYY-DD-MM", "Year, Day and Month")


        """Replace abbreviations in the given text based on the specified language."""
        if lang in _abbreviations:
            for pattern, replacement in _abbreviations[lang]:
                # print("patter : ", pattern)
                text = pattern.sub(replacement+" ", text)
        # print("text output : ", text)
        return text


    def expand_position(self, text, lang="bn"):
        """
        Replace :
        রাহিম ক্লাস ওয়ান এ ১ম, ১১তম ২২ তম ৩৩ তম -> রাহিম ক্লাস ওয়ান এ প্রথম, এগারোতম বাইশতম তেত্রিশতম

        """
        for regex, replacement in _ordinal_re[lang]:
            text = re.sub(regex, replacement, text)
        if lang == "bn":
            matches = re.findall(r"(\d+)(?:\s*)(?:তম)", text)
            if matches:
                for i in matches:
                    word = self.npr.number_to_words(i)
                    text = text.replace(i + "তম", word + "তম")
                    text = text.replace(i + " তম", word + "তম")
        return text

    def extract_year_blocks_with_positions(self, text):
        # matches = re.finditer(cfg.date_pattern, text)
        # print("matches : ", matches)
        # matches = re.finditer(self.year_pattern, text)
        combined_pattern = f"({cfg.date_pattern})|({self.year_pattern})"
        matches = re.finditer(combined_pattern, text)
        # print("matches : ", matches)
        results = []
        for match in matches:
            block = match.group(0)
            start_pos = match.start()
            end_pos = match.end()
            if text[start_pos]!= 0 and text[start_pos-1] in cfg.currency_list:
                continue

            results.append((block, start_pos, end_pos))

        return results

    def year_to_year(self, text):
        connectors = ["থেকে", "হতে", "চেয়ে"]
        suffixes = [
            "সালে",
            "সাল",
            "শতাব্দী",
            "শতাব্দীর",
            "শতাব্দীতে",
            "খ্রিস্টাব্দ",
            "খ্রিস্টাব্দের",
            "খ্রিস্টপূর্বাব্দের",
        ]

        # Create patterns
        digit_pattern = r"[0-9০-৯]{4}"
        connector_pattern = "|".join(connectors)
        suffix_pattern = "|".join(suffixes)

        # Regular expression pattern
        pattern = rf"({digit_pattern})\s*({connector_pattern})\s*({digit_pattern})\s*({suffix_pattern})"

        # Compile the regex
        regex = re.compile(pattern)

        # Find all matches with positions
        matches = regex.finditer(text)

        # List comprehension to collect match details
        result = [
            (
                match.start(),  # start position
                match.end(),  # end position
                match.group(),  # original text
                match.group()
                .replace(match.group(1), self.npr.year_in_number(match.group(1)))
                .replace(
                    match.group(3), self.npr.year_in_number(match.group(3))
                ),  # transformed text
            )
            for match in matches
        ]

        # Sort result in reverse order by start position
        result.sort(key=lambda x: x[0], reverse=True)
        # Replace matched text in reverse order to avoid index shifting
        for start, end, original, replacement in result:
            text = text[:start] + " "+replacement + text[end:]

        # print("text year : ", text)
        return text

    def year_formation(self, text):
        for i in self.year_patterns:
            if i in text:
                # pos = text.find(i, start_pos)
                position = text.find(i)
                if position != 0:
                    previous_character = text[position-1]
                    if previous_character.isnumeric():
                        text = text.replace(i, " " + i)
                    elif previous_character in ["-", "–", "—", "―"]:
                        text = text.replace(i, " " + i)

        text = self.collapse_whitespace(text)
        # print("text year2 : ", text)
        matches = self.extract_year_blocks_with_positions(text)[::-1]
        # print(" year matches : ", matches)
        """
        Need to correct year format extraction
        """
        for i in matches:
            # print("match", i)
            start_pos, end_pos = i[1], i[2]
            for y in i[0].split(" "):
                if y.isnumeric() and len(y) == 4:
                    process_year = self.npr.year_in_number(y)
                    i = i[0].replace(y, process_year)
            text = text[:start_pos] + i + text[end_pos:]
        # print("text year : ", text)
        return text

    def extract_currency_amounts(self, text):
        split_text = (text.replace("\t", " ")).split(" ")
        matches = re.findall(self.currency_pattern, text)
        pattern = cfg.currency_pattern
        sorted_matches = sorted(matches, key=len, reverse=True)
        for m in sorted_matches:
            index = next((i for i, item in enumerate(split_text) if m in item), None)
            currency = re.findall(pattern, m)
            if currency:
                n_m = m.replace(currency[0], "")
                n_m = n_m.replace(",", "")
                language = "en" if self.npr.contains_only_english(n_m) else "bn"

                # print("language : ", language)
                if "." in n_m:
                    word = self.npr.fraction_number_conversion(n_m, language=language)
                    if index != len(split_text)-1 and split_text[index+1].strip() in cfg.decimale_chunks:
                        r_word = " " + word + " "+split_text[index+1] +" "+ _currency[currency[0]] + ", "
                        r_m = m + " "+ split_text[index+1]
                        text = text.replace(r_m, r_word)
                    else:
                        r_word = " " + word + " " + _currency[currency[0]] + " "
                        text = text.replace(m, r_word)
                else:
                    word = self.npr.number_to_words(n_m)
                    if index != len(split_text)-1 and split_text[index+1].strip() in cfg.decimale_chunks:
                        n_word = " " + word + " "+split_text[index+1] +" "+ _currency[currency[0]] + ", "
                        r_m = m+" "+split_text[index+1]
                        text = text.replace(r_m, n_word)

                    else:
                        n_word = " " + word + " " + _currency[currency[0]] + " "
                        text = text.replace(m, n_word)
        # print("text1 : ", text)
        return text

    def matching_similariy_of_months(self, input_word):
        month_name = (
            data["en"]["months"]
            + data["bn"]["months"]
            + data["en"]["option_name"]
            + data["bn"]["option_name"]
        )
        similarity_threshold = 90  # Adjust this threshold as needed
        similar_months = []
        status = False
        for month in month_name:
            similarity_score = fuzz.partial_ratio(input_word, month)
            if similarity_score >= similarity_threshold:
                similar_months.append((month, input_word, similarity_score))

        # print("Similar months:")
        for month, input_word, similarity_score in similar_months:
            # print(f"{input_word} {month}: Similarity Score = {similarity_score}")
            status = True
        # return True
        if similar_months:
            sorted_similar_months = sorted(
                similar_months, key=lambda x: x[2], reverse=True
            )
            # print("+++++++", sorted_similar_months, status)
            return status, (sorted_similar_months[0][0], sorted_similar_months[0][1])
        # print("status : ", True)
        return status, (None, None)
    

    def date_formate_validation(self, date, text):
        n_data = date.strip().split(" ")
        for n_d in n_data:
            status, text_replacer = self.matching_similariy_of_months(n_d)
            if status:
                for t in text_replacer:
                    text = text.replace(t[0], t[1])
                return status, text
            if n_d in self.year_patterns:
                return True, text
        return False, text

    def add_spaces_to_numbers(self, text):

        # print("text : ", text)
        # Define a regular expression pattern to match both Bangla and English digits without spaces around them
        pattern = r"(?<![০-৯0-9])[\u09E6-\u09EF0-9]+(?![০-৯0-9])"
        # Use re.sub to find and replace matches with spaces around them
        result = re.sub(pattern, lambda x: " " + x.group(0) + " ", text)
        # print("result : ", result)
        result = " ".join([i for i in result.split(" ") if i.strip()]).strip()
        return result

    def extract_year(self, text):
        # print("year : ", text)
        pattern = re.findall(self.year_pattern, text)
        for p in pattern:
            text = text.replace(p, f" {p} ")
        # print("year p : ", text)
        return text

    def check_date_format(self, date_string):
        # Define the regex pattern for English and Bangla digits with slashes or hyphens
        pattern = r"^[\d০-৯]{1,2}[-/][\d০-৯]{1,2}[-/][\d০-৯]{2}([\d০-৯]{2})?$"

        # Check if the date string matches the pattern
        if re.match(pattern, date_string):
            return True
        else:
            return False

    def check_date_format_exception_case(self, date_string):
        if not self.check_date_format(date_string):
            return None

        # Split the date string by either '/' or '-'
        parts = re.split(r"[-/]", date_string)

        return parts

    def english_date_to_bangla_date(self, date_list):

        bn_data_list = []
        for d_l in date_list:
            en_digits_status = self.npr.is_english_digit_string(d_l)
            if en_digits_status:
                d_character = []
                for en_d in d_l:
                    if en_d in cfg._english2bangla2_digits_mapping:
                        bn_d = cfg._english2bangla2_digits_mapping[en_d]
                        d_character.append(bn_d)
                    else:
                        d_character.append(en_d)
                bn_digits = "".join(d_character)
                bn_data_list.append(bn_digits)
            else:
                bn_data_list.append(d_l)
        # print("bn_data_list : ", bn_data_list)
        return bn_data_list

    def month_spliting_issue_solver(self, org_text, reference_data):
        date = reference_data
        text = org_text
        # Find all occurrences of the date in the text
        matches = [match.start() for match in re.finditer(date, text)]
        extracted_text_list = []
        for m in matches:
            start = m
            end = m + len(date)
            # Extend the end position until the next space or end of the text
            while end < len(text) and text[end] != " ":
                end += 1
            # Print the start and end positions and the extracted text
            # print(f"Start: {start}, End: {end}")
            # print(f"Extracted Text: '{text[start:end]}'")
            # extracted_text_list.append(text[start:end])
            return text[start:end]
        # Print the positions of the date occurrences
        return None

    def validate_may_connected_with_charater_and_is_year(
        self, org_text, reference_data
    ):

        date = reference_data
        text = org_text
        # Find all occurrences of the date in the text
        matches = [match.start() for match in re.finditer(date, text)]
        status = True
        for m in matches:
            start = m
            end = m + len(date)
            while start > 0 and text[start - 1] != " ":
                start -= 1
            matches = re.findall(self.year_pattern, text[start:end])

            if " " in text[start:end]:
                chunk_d = text[start:end].split()
                for c_d in chunk_d:
                    if (
                        c_d in cfg.data["bn"]["months"]
                        or c_d in cfg.data["bn"]["option_name"]
                    ):
                        return True
                    else:
                        return False
            else:
                return True

    def check_date_format(self, text):
        pattern1 = (
            r"^\d{4}\s*-\s*\d{1,2}\s*-\s*\d{1,2}$"  # e.g., 2023 - 04 - 05 or 2023-4-5
        )
        pattern2 = (
            r"^\d{1,2}\s*-\s*\d{1,2}\s*-\s*\d{4}$"  # e.g., 06 - 04 - 2023 or 6-4-2023
        )
        pattern3 = r"^\d{1,2}/\d{1,2}/\d{4}$"  # e.g., 04/01/2023 or 4/1/2023
        pattern4 = (
            r"^\d{4}\s*/\s*\d{1,2}\s*/\s*\d{1,2}$"  # e.g., 2023 / 04 / 01 or 2023/4/1
        )

        # Check if the text matches any of the patterns
        if (
            re.match(pattern1, text)
            or re.match(pattern2, text)
            or re.match(pattern3, text)
            or re.match(pattern4, text)
        ):
            return True
        return False

    def extract_between_dashes(text):
        # Define the regex pattern
        # pattern = r'^.{4}-(.{2})$'
        pattern = r"^\d{4}\s*-\s*\d{2}$"
        match = re.match(pattern, text)

        # print(match[0])

    def replace_date_processing(self, text):
        text = self.extract_year(text)
        # print("text date", text)
        original_text = text
        r_text = text
        # print("original_text : ", original_text)
        dates = dt.get_dates(text)
        # print("dates : ", dates)
        for date in dates:
            # print("date1 : ", date)
            r_date = self.month_spliting_issue_solver(original_text, date)
            # print("r_date ", r_date)
            n_status = self.validate_may_connected_with_charater_and_is_year(
                original_text, r_date
            )
            # print(n_status, r_date)
            if n_status == False:
                continue
            if r_date is None:
                r_data = date
            # r_date = date
            date_list = self.check_date_format_exception_case(date.strip())
            # print("date_list : ", date_list)
            if date_list:
                formated_date = self.dp.date_processing(date_list)

                bn_data_list = self.english_date_to_bangla_date(date_list)
                for k, v in formated_date.items():
                    if v in bn_data_list:
                        key = k if "txt" in k else f"txt_{k}"
                        index = bn_data_list.index(v)
                        bn_data_list[index] = formated_date[key]
                # print(bn_data_list)
                process_date = " ".join(bn_data_list).strip()
                original_text = original_text.replace(r_date, " " + process_date + " ")
            else:
                date = self.add_spaces_to_numbers(date)

                status = True
                if " " in date:

                    status, text = self.date_formate_validation(date, text)

                    # print(f"status {status} date : {date}")

                    status = self.check_date_format(date)

                    # print(f"status {status} date : {date}")
                if status:
                    formated_date = self.dp.date_processing(date)
                    # print("formated_date : ", formated_date)
                    original_date = date
                    date_list = [i for i in date.split(" ") if i.strip()]
                    bn_data_list = self.english_date_to_bangla_date(date_list)
                    for k, v in formated_date.items():
                        if v in bn_data_list:
                            key = k if "txt" in k else f"txt_{k}"
                            index = bn_data_list.index(v)
                            bn_data_list[index] = formated_date[key]

                    # print("bn_data_list : ", bn_data_list)
                    process_date = " ".join(bn_data_list).strip()
                    if process_date.isdigit():
                        continue
                    else:
                        original_text = original_text.replace(
                            r_date, " " + process_date + " "
                        )
        _only_years = re.findall(self.year_pattern, original_text)
        for y in _only_years:
            # print("y", y)
            if y.isdigit():
                continue
            else:
                original_text = original_text.replace(
                    y, " " + self.npr.year_in_number(y) + " "
                )

        f_index = 0
        for full_name in cfg.data["en"]["months"]:
            # Replace only whole words (case-insensitive)
            pattern = r'\b' + re.escape(full_name) + r'\b'
            pattern_cap = r'\b' + re.escape(full_name.capitalize()) + r'\b'
            bn_name = cfg.data["bn"]["months"][f_index]
            original_text = re.sub(pattern, bn_name, original_text)
            original_text = re.sub(pattern_cap, bn_name, original_text)
            f_index += 1
        s_index = 0
        for short_name in cfg.data["en"]["option_name"]:

            # print("short_name : ", short_name)
            # print("original_text : ", original_text)
            
            if short_name in original_text or short_name.capitalize() in original_text:
                # print(short_name)
                bn_name = cfg.data["bn"]["months"][s_index]
                # Replace only whole words (case-insensitive)
                pattern = r'\b' + re.escape(short_name) + r'\b'
                pattern_cap = r'\b' + re.escape(short_name.capitalize()) + r'\b'
                original_text = re.sub(pattern, bn_name, original_text)
                original_text = re.sub(pattern_cap, bn_name, original_text)

            s_index += 1
        return original_text

    
    def number_plate_processing(self, text):


        # print("text : ", text)
        # Compile the regex
        regex = re.compile(cfg.number_regex_pattern)
        
        # Find all matches with positions
        matches = regex.finditer(text)
        for m in matches:
            # print(m.group(0))
            t = m.group(0)
            x = t.split('-')
            y = t

            second_last = str(x[-2])
            last = str(x[-1])

            combaine_number = second_last+"."+last
            replance_number = second_last+"-"+last
            replace_text  = self.npr.fraction_number_conversion(combaine_number, language="bn") # replace with number conversion function
            replace_text = replace_text.replace("দশমিক", "")
            y = y.replace(replance_number, replace_text)
            text = text.replace(t, y)

        return text
    
    def processing(self, text, operation):

        # print("text : ", text)
        processing_steps = {
            "email_normalization": eue.email_normalization,
            "url_normalization": eue.url_normalization,
            "product_number": pn.product_normalization,
            "unit_normalization": un.unit_processing,
            "number_plate": self.number_plate_processing,
            "driving_license": dlf.replace_in_text,
            "abbreviations": self.expand_abbreviations,

            "year_processing": self.exception_year_processing,
            "year_to_year": self.year_to_year,

            "phone_number": pne.phn_num_extractor,

            "puntuation": self.unwanted_puntuation_removing,
            "whitespace": self.collapse_whitespace,

            "year": self.year_formation,

            "symbols": self.expand_symbols,
            "ordinals": self.expand_position,
            "currency": self.extract_currency_amounts,

            "date": self.replace_date_processing,
            
            "nid": nid_normalizer.normalize,
            "nns": nns.replace_numbers_with_words,
            "passport": PassportFormatter.normalize,
            "ordinal_en": oc.convert_ordinals,
            "helpline_phn": hle.helpline_normalization,
            "number": self.npr.number_processing,
            "symbols_normalize": symn.sym_normalize,
            "collapse_whitespace": self.collapse_whitespace
        }

        
        for key, step in processing_steps.items():
            if key not in operation:
                # print(f"Skipping {key} as it's not in the operation list.")oui
                continue
            else:
                try:
                    # print("text : ", text, key)
                    text = step(text)
                    # print("text : ", text, key)
                except Exception as e:
                    logger.error(f"An error occurred in {step.__name__}: {e}")
                    continue
        
        return text

    def data_normailization(self, text):
        # Define a list of processing functions
        processing_steps = [
            self.exception_year_processing,
            self.unwanted_puntuation_removing,
            self.collapse_whitespace,
            self.year_formation,
            self.replace_date_processing,
            self.collapse_whitespace  # Called again after replace_date_processing
        ]

        # Iterate over the list of functions and apply each one with try-except
        for step in processing_steps:
            try:
                text = step(text)
                # print("text : ", text. step.__name__)
            except Exception as e:
                # print(f"Error in {step.__name__}: {e}")
                continue  # Skip the function that raised an exception
        return text


class EmojiRemoval:

    def __init__(self):
        self.regex_to_remove_emoji = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002500-\U00002BEF"  # chinese char
            "\U00002702-\U000027B0"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\ufe0f"  # dingbats
            "\u3030"
            "]+",
            re.UNICODE,
        )
        self.tp = TextParser()

    def remove_emoji(self, text):
        text = text.replace(" , ", ", ")
        text = re.sub(self.regex_to_remove_emoji, " ", text)
        text = self.tp.collapse_whitespace(text)
        return text

if __name__ == "__main__":

    text = "রাহিম ক্লাস ওয়ান এ ১ম, ১১তম ২২ তম ৩৩ তম, ১২৩৪ শতাব্দীতে ¥২০৩০.১২৩৪ বিবিধ  বাকেরগঞ্জ উপজেলার প্রায় 40 ভাগের পেশাই চাষাবাদ 80 and 40 ২২"
    tp = TextParser()
    text = tp.processing(text)
    print(text)
