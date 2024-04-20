
import re
import time
import datetime
from pybangla.config import Config as cfg

data = cfg.data

bn_number_mapping = cfg.bn_number_word_mapping

_abbreviations = cfg._abbreviations

_symbols = cfg._abbreviations

en_to_bn_digits_mapping = {e : b for e, b in zip(data["en"]["number"], data["bn"]["number"])}
bn_to_en_digits_mapping = {v : k for k, v in en_to_bn_digits_mapping.items()}
en_month_shortname = [i[:3] for i in data["en"]["months"]]

data["bn"]["digits_mapping"] = en_to_bn_digits_mapping
data["en"]["digits_mapping"] = bn_to_en_digits_mapping
data["en"]["option_name"] = en_month_shortname


class DateParser:
    def __init__(self):
        self.samples = cfg.samples

    def data_splitter(self, date_string):
        """
        
        """
        separator_pattern = '|'.join(map(re.escape, self.samples))
        return re.split(separator_pattern, date_string)


    def month_convert_to_number(self, month):
        """
        
        """
        key = month.lower().strip()
        if key in data["en"]["months"]:
            index = data["en"]["months"].index(key)+1
        elif key in data["bn"]["months"]:
            index = data["bn"]["months"].index(key)+1
        elif key in  data["bn"]["option_name"]:
            index = data["bn"]["option_name"].index(key)+1
        elif key in data["en"]["option_name"]:
            index = data["en"]["option_name"].index(key)+1
        elif key in data["en"]["number"]:
            index = data["en"]["number"].index(key)+1
        elif key in data["bn"]["number"]:
            index = data["bn"]["number"].index(key)+1
        else:
            print("else : ", key)
            index = key
        return index


    def format_non_punctuation(self, split_date):
        """
        
        """
        if len(split_date[0]) == 8:
            if int(split_date[0][4:6]) <= 12:
                year, month, day = split_date[0][:4], split_date[0][4:6], split_date[0][6:]
            else:
                year, month, day = split_date[0][4:], split_date[0][2:4], split_date[0][:2]
            return [day, month, year]
        else:
            print("This date format is not handled yet")
        return None


    def get_day_and_month(self, year_idx, idx, date_list):
        """
        
        """
        if year_idx == 0:
            return self.get_day_and_month_helper(idx, date_list, 1, 2)
        elif year_idx == 2:
            return self.get_day_and_month_helper(idx, date_list, -1, -2)
        else:
            print("Date format not handled yet")
        return None, None


    def get_day_and_month_helper(self, idx, date_list, offset1, offset2):
        """
        
        """
        if date_list[idx + offset1].isdigit() and date_list[idx + offset2].isdigit():
            return date_list[idx + offset2], date_list[idx + offset1]
        elif not date_list[idx + offset1].isdigit() and date_list[idx + offset2].isdigit():
            return date_list[idx + offset2], self.month_convert_to_number(date_list[idx + offset1])
        elif date_list[idx + offset1].isdigit() and not date_list[idx + offset2].isdigit():
            return date_list[idx + offset1], self.month_convert_to_number(date_list[idx + offset2])
        else:
            print("Date format not handled yet")
        return None, None


    def get_date_indexes(self, date_list):
        """
        
        
        """
        day, month, year = None, None, None
        for idx, elem in enumerate(date_list):
            if elem.isdigit() and len(elem) == 4:
                year_idx = idx
                year = date_list[idx]
                # print(date_list)
                day, month = self.get_day_and_month(year_idx, idx, date_list)
        return [day, month, year]

dp = DateParser()

class DateTranslator:
    def __init__(self):

        self.bn_regex = cfg.bn_regex


    def _replace_starting_zero(self, month):
        """
        Normalize string which start zero first
        
        """
        if month[0] == "0" or month[0] == "০":
            return month[1:]
        return month

    def _digit_converter(self, number, language):
        """
        convert the digit En to Bn or Bn to En
        
        """
        # print("number  : ", number)
        c_number = ""
        for n in number:
            if n in data[language]["number"]:
                c_number += n
            else:
                if n.strip() in data[language]["digits_mapping"]:
                    b_n = data[language]["digits_mapping"][n.strip()]
                    c_number+=b_n
        return c_number
    
    def get_weekday(self, date_:list=[], language="bn"):

        """
        Get weekday name Bangla or English
        
        """
        d, y = list(re.finditer(self.bn_regex, date_[0], re.UNICODE)), list(re.finditer(self.bn_regex, date_[2], re.UNICODE))
        if d:
            date_[0] = self._digit_converter(date_[0], language="bn")
        if y:
            date_[2] = self._digit_converter(date_[2], language="bn")
        current_date_object = datetime.datetime(int(date_[2]), int(date_[1]), int(date_[0]))
        if language in data:
            weekday = data[language]["weekdays"][current_date_object.weekday()]
        else:
            print("language not handel")
            weekday = ""
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
        search_key = int(self._replace_starting_zero(search_key))-1
        month = data[language]["months"][search_key]
        seasons = data[language]["seasons"][search_key//2]
        option_name = data[language]["option_name"][search_key]

        return [month, option_name, seasons]
    
    def today(self, language="bn"):

        """
        It return today date if may Bangla and English
        
        """
        current_date_object = datetime.date.today()
        formatted_date = [current_date_object.day, current_date_object.month, current_date_object.year]

        weekday = self.get_weekday(formatted_date, language)
        formatted_date = list(map(str, formatted_date))
        day   = self._digit_converter(formatted_date[0], language)
        month = self.search_month(formatted_date[1], language)
        year  =  self._digit_converter(formatted_date[2], language)

        return {"date":day, "month": month[0], "year": year, "weekday" : weekday, "ls_month": month[1], "seasons" : month[2]}
    
    def weekdays(self, language=""):
        """
        Weekday return or pair of weekday
        """
        if language:
            return data[language]["weekdays"]
        weekdays_map = [(i, j)for i, j in zip(data["bn"]["weekdays"], data["en"]["weekdays"])]
        return weekdays_map

    def seasons(self, language="bn"):
        """
        seasons return or pair of seasons

        """
        if language in data[language]["seasons"]:
            return data[language]["seasons"]
        bn_en_seasons = [(i, j)for i, j in zip(data["bn"]["seasons"], data["bn"]["seasons"])]
        return bn_en_seasons
    
    def months(self, language="bn"):

        """
        months return or pair of months
        
        """
        if language in data:
            return data[language]["months"]
        months_map = [(i, j)for i, j in zip(data["bn"]["months"], data["en"]["months"])]
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
        if isinstance(date_, list):
            if len(date_):
                formatted_date = date_
        else:
            split_date = dp.data_splitter(date_)
            split_date = [i for i in split_date if i]

            if len(split_date) == 1:
                formatted_date = dp.format_non_punctuation(split_date)
            else:
                formatted_date = dp.get_date_indexes(split_date)

        if formatted_date[0] == None and formatted_date[1] == None and formatted_date[2] == None:
            current_date_object = datetime.date.today()
            formatted_date = [current_date_object.day, current_date_object.month, current_date_object.year]

        weekday = self.get_weekday(formatted_date, language)
        day   = self._digit_converter(str(formatted_date[0]), language)
        month = self.search_month(str(formatted_date[1]), language)
        year  =  self._digit_converter(str(formatted_date[2]), language)

        return {"date":day, "month": month[0], "year": year, "weekday" : weekday, "ls_month": month[1], "seasons" : month[2]}

    def number_convert(self, number, language="bn"):
        """
        Convert the number digits English -> Bangla  or Bangla -> English

        Arg:
            number{str}  :  number string
            language{str}: specific language format, support bangla and english

        return: string
        
        """
        number   = self._digit_converter(number, language)
        return number




def expand_symbols(text, lang="bn"):
    for regex, replacement in _symbols[lang]:
        text = re.sub(regex, replacement, text)
        text = text.replace("  ", " ")  # Ensure there are no double spaces
    return text.strip()

def expand_abbreviations(text, lang="bn"):
    for regex, replacement in _abbreviations[lang]:
        text = re.sub(regex, replacement, text)
    return text



if __name__ == "__main__":
    # date_list = ["০১-এপ্রিল/২০২৩", "2023-04-05",  "06-04-2023", "04/01/2023",  "07 April, 2023", "Apr 1, 2023",  "2023/04/01", "01-Apr-2023", "01-Apr/2023",  "20230401",  "20042024", ["1", "4", "2025"]]
    # number = "123456"
    # dt = DateTranslator()
    # for date_ in date_list:
    #     start_time = time.time()
    #     formated_date = dt.date_format(date_, language="en")
    #     print(formated_date)

    

    # ০৫০৩ ২০২৩ 
    # formated_date = dt.date_format("০১-এপ্রিল/২০২৩", language="bn")
    # print(formated_date)
        # print("processing time : ", time.time()-start_time)
        
    # number = dt.number_convert(number, language="bn")
    # print("number : ", number)
    # today_date = dt.today(language="en")
    # print(today_date)

    # weekdays = dt.weekdays()
    # print(weekdays)

    text = "মোঃ সাইফুল ইসলাম &"

    text = expand_abbreviations(text)
    text = expand_symbols(text)
    print(text)