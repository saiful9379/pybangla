import re
import time
import datetime
import difflib
from .config import Config as cfg
from .parser import DateParser, TextParser, NumberParser, EmojiRemoval
from .number_parser import Word2NumberMap
from .date_extractor import DateExtractor
from .phone_number_extractor import PhoneNumberExtractor
# from .nid_num_normalize import NIDNormalizer\
from .driving_license import DrivingLicenseFormatter
from loguru import logger

dp, tp, npr, wnmp, emr = (
    DateParser(),
    TextParser(),
    NumberParser(),
    Word2NumberMap(),
    EmojiRemoval(),
)
pne = PhoneNumberExtractor()
dt = DateExtractor()
data = cfg.data
# nid_normalizer = NIDNormalizer()

class CheckDiff:
    def __init__(self):
        pass

    def diff_text(self, org_text, pro_text):
        # Split the strings into words
        org_words, pro_words = org_text.split(), pro_text.split()
        # Use difflib to find differences
        diff = difflib.ndiff(org_words, pro_words)
        removed_chunk, added_chunk, added_chunks, removed_chunks = [], [], [], []
        for change in diff:
            if change.startswith("+ "):
                added_chunk.append(change[2:])
                if removed_chunk:
                    removed_chunks.append(" ".join(removed_chunk))
                    removed_chunk = []
            elif change.startswith("- "):
                removed_chunk.append(change[2:])
                if added_chunk:
                    added_chunks.append(" ".join(added_chunk))
                    added_chunk = []
            else:
                if added_chunk:
                    added_chunks.append(" ".join(added_chunk))
                    added_chunk = []
                if removed_chunk:
                    removed_chunks.append(" ".join(removed_chunk))
                    removed_chunk = []
        # Append any remaining chunks
        if added_chunk:
            added_chunks.append(" ".join(added_chunk))
        if removed_chunk:
            removed_chunks.append(" ".join(removed_chunk))
        return removed_chunks, added_chunks


class Normalizer:
    def __init__(self):
        # self.supper()

        self.bn_regex = cfg.bn_regex
        self.cdiff = CheckDiff()

    def today(self, language="bn"):
        """
        It return today date if may Bangla and English

        """
        current_date_object = datetime.date.today()
        formatted_date = [
            current_date_object.day,
            current_date_object.month,
            current_date_object.year,
        ]

        weekday = npr.get_weekday(formatted_date, language)
        formatted_date = list(map(str, formatted_date))
        day = npr._digit_converter(formatted_date[0], language)
        month = npr.search_month(formatted_date[1], language)
        year = npr._digit_converter(formatted_date[2], language)

        txt_date = npr.number_to_words(day)
        txt_year = npr.year_in_number(year, language=language)

        return {
            "date": day,
            "month": month[0],
            "month": month[0],
            "year": year,
            "txt_date": txt_date,
            "txt_year": txt_year,
            "weekday": weekday,
            "ls_month": month[1],
            "seasons": month[2],
        }

    def weekdays(self, language="", day=""):
        """
        Weekday return or pair of weekday
        """
        if day:
            day = day.lower().strip()
            bn_weakday, en_weakday = data["bn"]["weekdays"], data["en"]["weekdays"]
            if day in bn_weakday:
                return {day: en_weakday[bn_weakday.index(day)]}
            if day in en_weakday:
                return {day: bn_weakday[en_weakday.index(day)]}
        if language:
            return {language: data[language]["weekdays"]}
        weekdays_map = {"bn": data["bn"]["weekdays"], "en": data["en"]["weekdays"]}
        return weekdays_map

    def seasons(self, language="", seasons=""):
        """
        seasons return or pair of seasons

        """
        if seasons:
            seasons = seasons.lower().strip()
            bn_seasons, en_seasons = data["bn"]["seasons"], data["en"]["seasons"]
            if seasons in bn_seasons:
                return {seasons: en_seasons[bn_seasons.index(seasons)]}
            if seasons in en_seasons:
                return {seasons: bn_seasons[en_seasons.index(seasons)]}
        if language:
            return data[language]["seasons"]

        bn_en_seasons = {"bn": data["bn"]["seasons"], "en": data["en"]["seasons"]}
        return bn_en_seasons

    def months(self, language="", month=""):
        """
        months return or pair of months

        """
        if month:
            month = month.lower().strip()
            bn_months, option_name, en_months = (
                data["bn"]["months"],
                data["bn"]["option_name"],
                data["en"]["months"],
            )
            if month in bn_months:
                return {
                    month: en_months[bn_months.index(month)],
                    "bangla": option_name[bn_months.index(month)],
                }
            if month in option_name:
                return {
                    month: en_months[option_name.index(month)],
                    "bangla": bn_months[option_name.index(month)],
                }
            if month in en_months:
                return {
                    month: bn_months[en_months.index(month)],
                    "bangla": option_name[en_months.index(month)],
                }
        if language in data:
            return {language: data[language]["months"]}
        months_map = {
            "bn": data["bn"]["months"],
            "bn_name": data["bn"]["option_name"],
            "en": data["en"]["months"],
        }
        return months_map

    def date_format(self, date_, language="bn"):
        """
        Process the date from input and return format date

        Arg:
            data_{str or list} :  date may string or list of list like ["dd", "mm", "yyyy"]
            language{str}      : specific language format, support bangla and english

        return :
                Dictonary :  {"date":day, "month": month[0], "year": year, "weekday" : weekday, "ls_month": month[1], "seasons" : month[2]}
        """
        date = dt.get_dates(date_)
        # print(date)
        if len(date):
            formated_date = dp.date_processing(date_, language=language)
            return formated_date
        else:
            print("No date found")

    def number_convert(self, number, language="bn"):
        """
        Convert the number digits English -> Bangla  or Bangla -> English

        Arg:
            number{str}  :  number string
            language{str}: specific language format, support bangla and english

        return: string

        """
        number = npr._digit_converter(number, language)
        # print("====== ",number)

        number_string = npr.number_to_words(number)
        digit_word = npr.digit_number_to_digit_word(number, language=language)

        data = {
            "digit": number,
            "digit_word": digit_word,
            "number_string": number_string,
        }
        return data

    def text_normalizer(self, text,
                        all_operation,
                        email_normalization=False,
                        url_normalization=False,
                        product_number=False,
                        unit_normalization=False,
                        driving_license=False,
                        number_plate=False, 
                        abbreviations=False, 
                        year=False, 
                        puntuation=False,
                        phone_number=False, 
                        symbols=False, 
                        ordinals=False, 
                        currency=False, 
                        date=False, 
                        nid=False, 
                        nns=False,
                        passport=False,
                        ordinal_en=False,
                        helpline_phn=False,
                        number=False,
                        symbols_normalize=False,
                        emoji=False):
        """
        Processes a given text by applying various normalization techniques based on specified boolean parameters.

        Parameters:
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

        Returns:
        - str: The normalized text after applying the selected transformations.

        This function is useful for preprocessing text in speech-to-text systems, NLP applications, and text-to-speech (TTS) models where textual consistency is crucial.
        """
        
        if all_operation:
            processing_map = {
                "email_normalization": True,
                "url_normalization": True,
                "product_number" : True,
                "unit_normalization" : True,
                "driving_license": True,
                "number_plate": True,
                "abbreviations": True,
                "year_processing": True,
                "year_to_year": True,
                "phone_number": True,
                "puntuation": True,
                "whitespace": True,  # Always included
                "year": True,
                "symbols": True,
                "ordinals": True,
                "currency": True,
                "date": True,
                "nid": True,
                "nns" : True,
                "passport": True,
                "ordinal_en" : True,
                "helpline_phn": True,
                "number": True,
                "symbols_normalize": True,
                "collapse_whitespace": True  # Always included
            }
        else:
            if email_normalization or url_normalization or number_plate or abbreviations or year or puntuation or phone_number or symbols or ordinals or currency or date or nid or passport or number or emoji:
                processing_map = {
                    "email_normalization": email_normalization,
                    "url_normalization": url_normalization,
                    "product_number": product_number,
                    "unit_normalization": unit_normalization,
                    "driving_license": driving_license,
                    "number_plate": number_plate,
                    "abbreviations": abbreviations,
                    "year_processing": year,
                    "year_to_year": year,
                    "phone_number": phone_number,
                    "puntuation": puntuation,
                    "whitespace": True,  # Always included
                    "year": year,
                    "symbols": symbols,
                    "ordinals": ordinals,
                    "currency": currency,
                    "date": date,
                    "nid": nid,
                    "nns" : nns,
                    "passport": passport,
                    "ordinal_en" : ordinal_en,
                    "helpline_phn": helpline_phn,
                    "number": number,
                    "symbols_normalize": symbols_normalize,
                    "collapse_whitespace": True  # Always included
                }
            else:
                raise ValueError("At least one of the operations must be True")

        if emoji:
            text = emr.remove_emoji(text)

        # Filter only the enabled operations
        operation = [key for key, enabled in processing_map.items() if enabled]

        text = re.sub(r"\s+", " ", text)  # Initial whitespace cleanup
        text = re.sub(r"\n+", " ", text)  # Remove new lines
        text = re.sub(r"\t+", " ", text)  # Remove tabs
        text = text.strip()
        if text.strip() == "":
            logger.warning("Input text is empty after stripping whitespace.")
            return text

        text = tp.processing(text, operation)
        return text

    def data_normalizer(self, text):

        text = tp.data_normailization(text)
        return text
    
    def driving_license_norlization(self, text):
        text = DrivingLicenseFormatter.replace_in_text(text, 'bengali_words')
        return text

    # def remove_emoji(self, text):
    #     text = emr.remove_emoji(text)
    #     return text

    # def emoji2text(self, text):
    #     text = emrp.replace_emoji(text)
    #     return text

    def word2number(self, text):
        text = wnmp.convert_word2number(text)
        return text

    def date_extraction(self, text):

        dates = dt.get_dates(text)
        formated_date = [self.date_format(i) for i in dates]
        # print(f"Input: {sentence}: Output: {dates}")
        if len(formated_date):
            return formated_date
        else:
            print("No date found")

    def text_diff(self, text1, text2):
        remove_chunk, add_chunk = self.cdiff.diff_text(text1, text2)
        return remove_chunk, add_chunk

    def process_phone_number(self, text):

        text = pne.phn_num_extractor(text)

        return text


if __name__ == "__main__":

    # Testing Date format
    date_list = [
        "০১-এপ্রিল/২০২৩",
        "১ এপ্রিল ২০২৩" "2023-04-05",
        "06-04-2023",
        "04/01/2023",
        "07 April, 2023",
        "Apr 1, 2023",
        "2023/04/01",
        "01-Apr-2023",
        "01-Apr/2023",
        "20230401",
        "20042024",
        ["1", "4", "2025"],
    ]
    # number = "123456" or "২০২৩"
    number = "২০২৩"
    nmlr = Normalizer()
    print("++++++++++++++++++++ Date testing ++++++++++++++++++++++")
    print("Date format Testing : ", end="", flush=True)
    for date_ in date_list:
        start_time = time.time()
        formated_date = nmlr.date_format(date_, language="en")
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
    weekdays = nmlr.weekdays(day="Monday")
    print(weekdays)

    print("++++++++++++++++ end weekdays +++++++++++++++++++++")
    # print(weekdays)
    print("+++++++++++++++ seasons ++++++++++++++++++++++++")
    # seasons = nmlr.seasons()
    # seasons = nmlr.seasons(language="bn")
    # seasons = nmlr.seasons(language="en")
    seasons = nmlr.seasons(seasons="গ্রীষ্ম")
    print(seasons)

    print("+++++++++++++++ end seasons ++++++++++++++++++++++++")

    print("+++++++++++++++++ months +++++++++++++++++++++++++++")
    month = nmlr.months()
    month = nmlr.months(month="মার্চ")
    print(month)

    text = "রাহিম ক্লাস ওয়ান এ ১ম, ১১তম ২২ তম ৩৩ তম, ১২৩৪ শতাব্দীতে ¥২০৩০.১২৩৪ বিবিধ  বাকেরগঞ্জ উপজেলার প্রায় 40 ভাগের পেশাই চাষাবাদ 80 and 40 ২২"

    text = nmlr.text_normalizer(text)

    print(text)
