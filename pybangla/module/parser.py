import re
import datetime
import string
from .config import Config as cfg
from num2words import num2words
from .date_extractor import DateExtractor
from fuzzywuzzy import fuzz

# from bnemo import Translator
from .phone_number_extractor import PhoneNumberExtractor


dt = DateExtractor()
pne = PhoneNumberExtractor()
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
                    word
                    for word in eng_in_num_to_words.replace(",", " ")
                    .replace(" and ", " ")
                    .split()
                ]
            return " ".join(bangla_num_to_words_list)
        except Exception as e:
            print(e)
            return

    def number_to_words(self, number: str, chunk_millions=7):

        en_extraction = list(re.finditer(self.en_regex, number, re.UNICODE))
        number = number[::-1]
        chunks = [
            number[i : i + chunk_millions]
            for i in range(0, len(number), chunk_millions)
        ]
        chunks = [c[::-1] for c in chunks]
        chunks = chunks[::-1]
        if en_extraction:
            number = " crore ".join(
                [
                    self.number_to_words_converting_process(chunk, lang="en")
                    for chunk in chunks
                ]
            )
            number = number.replace("zero", "")
        else:
            number = " কোটি ".join(
                [
                    self.number_to_words_converting_process(chunk, lang="bn")
                    for chunk in chunks
                ]
            )
            # print(number)
            number = number.replace("শূন্য", "")

        return " ".join(number.split())

    def digit_number_to_digit_word(self, number, language="bn"):

        number = re.sub(_whitespace_re, " ", number)
        s_n = ""
        for i in number:
            # print("language : ", language, i)

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
        n_n = ""
        for i in number:
            if i in cfg._english2bangla2_digits_mapping:
                n_n += cfg._english2bangla2_digits_mapping[i]
            else:
                n_n += i

        s_m = n_n.split(".")
        before_dot_word, after_dot_word = self.number_to_words(
            s_m[0]
        ), self.digit_number_to_digit_word(s_m[1], language=language)

        if len(after_dot_word):
            word = before_dot_word + " দশমিক " + after_dot_word
            return word
        return before_dot_word

    def check_comma_dot_dari(self, p):
        l_p = [",", ".", "।"]
        if p in l_p:
            return True
        return False

    def number_processing(self, text):
        pattern = r"[\d,\.]+"
        matches = re.findall(pattern, text)
        sorted_matches = sorted(matches, key=len, reverse=True)
        for n in sorted_matches:
            p_status = self.check_comma_dot_dari(n)
            if p_status:
                text = text.replace(n, " " + n + " ")
                # print("p_status : ", text)
            else:
                status = self.contains_only_english(n)
                m_re = n.replace(",", "")
                if status:

                    if "." in m_re:
                        bn_m = self.fraction_number_conversion(m_re)
                    else:
                        bn_m = self.number_to_words(self._digit_converter(m_re))
                    text = text.replace(n, " " + str(bn_m) + " ")
                else:
                    if "." in m_re:
                        bn_m = self.fraction_number_conversion(m_re, language="bn")
                    else:
                        bn_m = self.number_to_words(m_re)
                    # print("else : bn_m ", n, bn_m)
                    text = text.replace(str(n), " " + str(bn_m) + " ")
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
        self.year_patterns = ["সালের", "সালে", "শতাব্দী", "শতাব্দীর", "শতাব্দীতে"]
        self.year_pattern = (
            r"(?:\b|^\d+)(\d{4})\s*(?:সালে?র?|শতাব্দী(?:র)?|শতাব্দীতে|এর)+"
        )
        self.currency_pattern = (
            r"(?:\$|£|৳|€|¥|₹|₽|₺)?(?:\d+(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)"
        )
        self.npr = NumberParser()
        self.dp = DateParser()

    def collapse_whitespace(self, text):
        text = re.sub(_whitespace_re, " ", text)
        text = re.sub(r"\s*,\s*", ", ", text)
        return text

    def phone_number_processing(self):
        pass

    def exception_year_processing(self, text):

        # if len(text
        # s+(\d{4}(?:-|–|—|―)\d{2})\s+
        # _year_with_hyphen = re.findall(r'(\d{4}(?:-|–|—|―)\d{2})', text)
        # print(_year_with_hyphen)
        # _year_with_hyphen = re.findall(r'\s+(\d{4}(?:-|–|—|―)\d{2})\s+', text)
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
        return text

    def unwanted_puntuation_removing(self, text):

        # https://stackoverflow.com/questions/63256077/how-to-remove-redundant-punctuations-keep-only-the-first-one-in-text
        def my_replace(match):
            match = match.group()
            return match[0] + (" " if " " in match else "")

        _redundent_punc_removal = r"[!\"#$%&\'()*+,\-.\/:;<=>?@\[\\\]^_`।{|}~ ]{2,}"
        _remove_hyphen_slash = r"(?<!\d)[-/](?!\d)"
        _remove_comma = r"(?<=\d),(?=\d)"
        _remove_space_in_punctuations = r"(?<=[^\w\s])\s+(?=[^\w\s])"

        text = _STANDARDIZE_ZW.sub("\u200D", text)
        text = re.sub(r"\u200d", "", text)
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
        text = re.sub(_remove_space_in_punctuations, "", text)
        text = re.sub(
            _redundent_punc_removal, my_replace, text, 0
        )  # only keep the first punctuation
        text = re.sub(_remove_comma, "", text)
        text = re.sub(_remove_hyphen_slash, " ", text)
        translation_table = str.maketrans(_punctuations)
        text = text.translate(translation_table)
        return text

    def expand_symbols(self, text, lang="bn"):
        for key, replacement in _symbols[lang]:
            text = text.replace(key, replacement)
        return text.strip()

    def expand_abbreviations(self, text, lang="bn"):
        for key, replacement in _abbreviations[lang]:
            text = text.replace(key, replacement)
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
                    text = text.replace(i + "তম", word + " তম")
                    text = text.replace(i + " তম", word + " তম")
        return text

    def extract_year_blocks_with_positions(self, text):
        matches = re.finditer(self.year_pattern, text)

        results = []
        for match in matches:
            block = match.group(0)
            start_pos = match.start()
            end_pos = match.end()
            results.append((block, start_pos, end_pos))

        return results

    def year_formation(self, text):

        for i in self.year_patterns:
            # print(i)
            if i in text:
                text = text.replace(i, " " + i)
        text = self.collapse_whitespace(text)
        matches = self.extract_year_blocks_with_positions(text)[::-1]

        # print(" matches : ", matches)
        """
        Need to correct year format extraction
        """
        for i in matches:
            # print("match", i)
            extract_year = [y for y in i[0].split(" ") if y.isnumeric() and len(y) == 4]
            # print(extract_year)
            start_pos, end_pos = i[1], i[1] + len(extract_year[0])
            process_year = self.npr.year_in_number(extract_year[0])
            text = text[:start_pos] + process_year + text[end_pos:]
        return text

    def extract_currency_amounts(self, text):

        matches = re.findall(self.currency_pattern, text)
        pattern = r"[৳$£€¥₹₽₺]"

        sorted_matches = sorted(matches, key=len, reverse=True)

        for m in sorted_matches:
            currency = re.findall(pattern, m)
            if currency:
                n_m = m.replace(currency[0], "")
                n_m = n_m.replace(",", "")
                language = "en" if self.npr.contains_only_english(n_m) else "bn"
                if "." in n_m:
                    word = self.npr.fraction_number_conversion(n_m, language=language)
                    r_word = " " + word + " " + _currency[currency[0]] + " "
                    text = text.replace(m, r_word)
                else:
                    word = self.npr.number_to_words(n_m)
                    n_word = " " + word + " " + _currency[currency[0]] + " "
                    text = text.replace(m, n_word)
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
            # print("+++++++", sorted_similar_months)
            return status, (sorted_similar_months[0][0], sorted_similar_months[0][1])
        return status, (None, None)

    def date_formate_validation(self, date, text):

        # print("data format validation : ", date,"====", text)
        n_data = date.strip().split(" ")
        # print("n_data : ", n_data)
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
        pattern = re.findall(self.year_pattern, text)
        for p in pattern:
            text = text.replace(p, f" {p} ")
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

        print(match[0])

    def replace_date_processing(self, text):
        text = self.extract_year(text)
        # print(text)
        original_text = text
        r_text = text
        # print("original_text : ", original_text)
        dates = dt.get_dates(text)
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
                process_date = " ".join(bn_data_list).strip()
                original_text = original_text.replace(r_date, " " + process_date + " ")
            else:
                date = self.add_spaces_to_numbers(date)

                status = True
                if " " in date:

                    status, text = self.date_formate_validation(date, text)

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

                    process_date = " ".join(bn_data_list).strip()
                    if process_date.isdigit():
                        continue
                    else:
                        original_text = original_text.replace(
                            r_date, " " + process_date + " "
                        )
        _only_years = re.findall(self.year_pattern, original_text)
        for y in _only_years:
            if y.isdigit():
                continue
            else:
                original_text = original_text.replace(
                    y, " " + self.npr.year_in_number(y) + " "
                )

        f_index = 0
        for full_name in cfg.data["en"]["months"]:
            if full_name in original_text or full_name.capitalize() in original_text:
                bn_name = cfg.data["bn"]["months"][f_index]
                original_text = original_text.replace(full_name, bn_name)
                original_text = original_text.replace(full_name.capitalize(), bn_name)
            f_index += 1
        s_index = 0
        for short_name in cfg.data["en"]["option_name"]:
            # print(short_name)
            if short_name in original_text or short_name.capitalize() in original_text:
                bn_name = cfg.data["bn"]["months"][s_index]
                original_text = original_text.replace(short_name, bn_name)
                original_text = original_text.replace(short_name.capitalize(), bn_name)

            s_index += 1
        return original_text

    def processing(self, text):
        text = self.exception_year_processing(text)
        text = pne.phn_num_extractor(text)
        text = self.unwanted_puntuation_removing(text)
        text = self.collapse_whitespace(text)
        text = self.year_formation(text)
        text = self.expand_symbols(text)
        text = self.expand_abbreviations(text)
        text = self.expand_position(text)
        text = self.extract_currency_amounts(text)
        text = self.replace_date_processing(text)
        text = self.npr.number_processing(text)
        text = self.collapse_whitespace(text)
        return text

    def data_normailization(self, text):

        text = self.exception_year_processing(text)
        text = self.unwanted_puntuation_removing(text)
        text = self.collapse_whitespace(text)
        text = self.year_formation(text)
        text = self.replace_date_processing(text)
        text = self.collapse_whitespace(text)
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


# class EmojiReplacer:
#     def __init__(self):
#         self.translator = Translator()

#     def replace_emoji(self, text):
#         txt = self.translator.translate(text).text
#         # print(txt)
#         return text if len(txt)==0 else txt

if __name__ == "__main__":

    text = "রাহিম ক্লাস ওয়ান এ ১ম, ১১তম ২২ তম ৩৩ তম, ১২৩৪ শতাব্দীতে ¥২০৩০.১২৩৪ বিবিধ  বাকেরগঞ্জ উপজেলার প্রায় 40 ভাগের পেশাই চাষাবাদ 80 and 40 ২২"
    tp = TextParser()
    text = tp.processing(text)
    print(text)
