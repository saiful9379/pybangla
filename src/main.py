
import re
import time
import datetime



bn_weekdays = ["সোমবার", "মঙ্গলবার", "বুধবার","বৃহস্পতিবার", "শুক্রবার", "শনিবার", "রবিবার"]
en_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" "Sunday"]

bangla_seasons = ["গ্রীষ্ম","বর্ষা", "শরৎ", "হেমন্ত", "শীত", "বসন্ত",]
en_name_bangla_seasons = ["Summer", "Wet season", "Autumn","Dry season", "Winter", "Spring"]

bangla_months = ["বৈশাখ", "জ্যৈষ্ঠ","আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"]
en_name_bangla_months = ["জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর",  "ডিসেম্বর"]

bn_number = ["০","১","২","৩","৪", "৫", "৬", "৭", "৮", "৯"]
en_number = ["0","1","2","3","4","5", "6", "7","8", "9"]

months_map = {
    "1": ["জানুয়ারি", "January", "Jan", "১", "বৈশাখ", "গ্রীষ্ম", "Summer"],
    "2": ["ফেব্রুয়ারি", "February", "Feb", "২", "জ্যৈষ্ঠ", "গ্রীষ্ম", "Summer"],
    "3": ["মার্চ", "March", "Mar", "৩", "আষাঢ়", "বর্ষা", "Wet season"],
    "4": ["এপ্রিল", "April", "Apr", "৪", "শ্রাবণ", "বর্ষা", "Wet season"],
    "5": ["মে", "May", "May", "৫", "ভাদ্র", "শরৎ", "Autumn"],
    "6": ["জুন", "June", "Jun", "৬", "আশ্বিন", "শরৎ", "Autumn"],
    "7": ["জুলাই","July", "Jul", "৭", "কার্তিক", "হেমন্ত", "Dry season"],
    "8": ["আগস্ট", "August", "Aug", "৮", "অগ্রহায়ণ", "হেমন্ত", "Dry season"],
    "9": ["সেপ্টেম্বর", "September", "Sep", "৯", "পৌষ", "শীত", "Winter"],
    "10": ["অক্টোবর", "October", "Oct", "১০", "মাঘ", "শীত", "Winter"],
    "11": ["নভেম্বর", "November", "Nov", "১১", "ফাল্গুন", "বসন্ত", "Spring"],
    "12": ["ডিসেম্বর", "December", "Dec", "১২", "চৈত্র", "বসন্ত", "Spring"]
}

month_map_number = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
    "aug": "07", "sep": "08", "sept": "09", "oct": "10", "nov": "11", "dec": "12",
    "january": "01", "february": "02", "march": "03", "april": "04", "june": "06",
    "july": "07", "august": "08", "september": "09", "october": "10", "movember": "11", "december": "12"
}

en_to_bn_digits_mapping ={e : b for e,b in zip(en_number, bn_number)}
bn_to_en_digits_mapping = {v:k for k, v in en_to_bn_digits_mapping.items()}

SYMBLES = ["-", ",", "/", " "]


class DateParser:
    SAMPLES = SYMBLES
    MONTH_MAPPING = month_map_number

    @staticmethod
    def data_splitter(date_string):
        separator_pattern = '|'.join(map(re.escape, DateParser.SAMPLES))
        return re.split(separator_pattern, date_string)

    @staticmethod
    def month_convert_to_number(month):
        key = month.lower().strip()
        return DateParser.MONTH_MAPPING.get(key, month)

    @staticmethod
    def format_non_punctuation(split_date):
        if len(split_date[0]) == 8:
            if int(split_date[0][4:6]) <= 12:
                year, month, day = split_date[0][:4], split_date[0][4:6], split_date[0][6:]
            else:
                year, month, day = split_date[0][4:], split_date[0][2:4], split_date[0][:2]
            return [day, month, year]
        else:
            print("This date format is not handled yet")
            return None

    @staticmethod
    def get_day_and_month(year_idx, idx, date_list):
        if year_idx == 0:
            return DateParser.get_day_and_month_helper(idx, date_list, 1, 2)
        elif year_idx == 2:
            return DateParser.get_day_and_month_helper(idx, date_list, -1, -2)
        else:
            print("Date format not handled yet")
            return None, None

    @staticmethod
    def get_day_and_month_helper(idx, date_list, offset1, offset2):
        if date_list[idx + offset1].isdigit() and date_list[idx + offset2].isdigit():
            return date_list[idx + offset2], date_list[idx + offset1]
        elif not date_list[idx + offset1].isdigit() and date_list[idx + offset2].isdigit():
            return date_list[idx + offset2], DateParser.month_convert_to_number(date_list[idx + offset1])
        elif date_list[idx + offset1].isdigit() and not date_list[idx + offset2].isdigit():
            return date_list[idx + offset1], DateParser.month_convert_to_number(date_list[idx + offset2])
        else:
            print("Date format not handled yet")
            return None, None

    @staticmethod
    def get_date_indexes(date_list):
        day, month, year = None, None, None
        for idx, elem in enumerate(date_list):
            if elem.isdigit() and len(elem) == 4:
                year_idx = idx
                year = date_list[idx]
                day, month = DateParser.get_day_and_month(year_idx, idx, date_list)
        return [day, month, year]



class Translator:
    def __init__(self):
        self.month_data = months_map

    @staticmethod
    def _replace_starting_zero(month):
        if month[0] == "0" or month[0] == "০":
            return month[1:]
        return month
    @staticmethod
    def _digit_converter(number, language):
        c_number = ""
        if language== "bn":
            for n in number:
                if n.strip() in en_to_bn_digits_mapping:
                    b_n = en_to_bn_digits_mapping[n.strip()]
                    c_number+=b_n

        elif language== "en":
            for n in number:
                if n.strip() in bn_to_en_digits_mapping:
                    e_n = bn_to_en_digits_mapping[n.strip()]
                    c_number+=e_n
        else:
            print("language not handel yet")
        return c_number
    
    def get_weekday(self, date_:list=[]):
        current_date_object = datetime.datetime(int(date_[2]), int(date_[1]), int(date_[0]))
        print(current_date_object)
        bangla_weekday = bn_weekdays[current_date_object.weekday()]
        return bangla_weekday

    def search_month(self, search_key, language="bn"):
        search_key = self._replace_starting_zero(search_key)
        if search_key in self.month_data:

            # need to add more information

            return self.month_data[search_key][0] if language == "bn" else self.month_data[search_key][1]
        

        for key, value in self.month_data.items():
            if search_key in value:

                # need to add more information

                return value[0] if language == "bn" else value[1]
        return None
    
    def today(self, language="bn"):
        current_date_object = datetime.date.today()
        formatted_date = [current_date_object.day, current_date_object.month, current_date_object.year]

        weekday = self.get_weekday(formatted_date)
        formatted_date = list(map(str, formatted_date))
        day   = self._digit_converter(formatted_date[0], language)
        month = self.search_month(formatted_date[1], language)
        year  =  self._digit_converter(formatted_date[2], language)

        return {"date":day, "month": month, "year": year, "weekday" : weekday}
    
    def weekdays(self, language="bn"):
        if language=="bn":
            return bn_weekdays
        elif language =="en":
            return en_weekdays
        bn_en_weekday = [(i, j)for i, j in zip(bn_weekdays, en_weekdays)]
        return bn_en_weekday

    def seasons(self, language="bn"):
        if language=="bn":
            return bangla_seasons
        elif language =="en":
            return en_name_bangla_seasons
        bn_en_seasons = [(i, j)for i, j in zip(bangla_seasons, en_name_bangla_seasons)]
        return bn_en_seasons
    
    def months(self, language="bn"):
        if language=="bn":
            return bangla_months
        elif language =="en":
            return en_name_bangla_months
        bn_en_seasons = [(i, j)for i, j in zip(bangla_months, en_name_bangla_months)]
        return bn_en_seasons

    def date_format(self, date_, language="bn"):

        if isinstance(date_, list):
            if len(date_):
                formatted_date = date_
        else:
            split_date = DateParser.data_splitter(date_)
            split_date = [i for i in split_date if i]

            if len(split_date) == 1:
                formatted_date = DateParser.format_non_punctuation(split_date)
            else:
                formatted_date = DateParser.get_date_indexes(split_date)

        # print(f"Date: {split_date}, formated Date: {formatted_date}")

        if formatted_date[0] == None and formatted_date[1] == None and formatted_date[2] == None:
            current_date_object = datetime.date.today()
            formatted_date = [current_date_object.day, current_date_object.month, current_date_object.year]
            # formatted_date = list(map(str, formatted_date))


        weekday = self.get_weekday(formatted_date)
        day   = self._digit_converter(str(formatted_date[0]), language)
        month = self.search_month(str(formatted_date[1]), language)
        year  =  self._digit_converter(str(formatted_date[2]), language)
        # print(month
        return {"date":day, "month": month, "year": year, "weekday" : weekday}

    def number_convert(self, number, language):
        number   = self._digit_converter(number, language)
        return number

if __name__ == "__main__":
    date_strings = [
        "2023-04-05", "06-04-2023", "04/01/2023", "07 April, 2023", "Apr 1, 2023", "2023/04/01",
        "01-Apr-2023", "01-Apr/2023", "20230401", "20042024", ["1", "4", "2025"]
    ]
    number = "123456"
    TR = Translator()
    for date_ in date_strings:
        start_time = time.time()
        formated_date = TR.date_format(date_, language="bn")
        print(formated_date)
        print("processing time : ", time.time()-start_time)
        
    number = TR.number_convert(number, language="bn")
    print("number : ", number)
    today_date = TR.today()
    print(today_date)