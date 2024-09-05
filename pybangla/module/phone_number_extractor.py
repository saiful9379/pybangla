import re
from .config import Config as cfg


class PhoneNumberExtractor:

    def __init__(self):
        self.number_extention = ["+88", "+৮৮"]
        self.phn_number = [
            "017",
            "015",
            "013",
            "016",
            "018",
            "019",
            "০১৭",
            "০১৫",
            "০১৩",
            "০১৬",
            "০১৮",
            "০১৯",
        ]
        # self.pattern = r'(?:\+?৮৮)?০১[৩-৯][০-৯]{2}-?[০-৯]{6}|(?:\+88)?01[3-9]\d{2}-?\d{6}'
        self.pattern = r"(?:\+?৮৮)?০১[৩-৯][০-৯]{2}-?[০-৯]{6}(?=[, ]|$)|(?:\+88)?01[3-9]\d{2}-?\d{6}(?=[, ]|$)"
        self.plux = {"+": "প্লাস"}

    # def checking_prefix()

    def contains_only_english(self, input_string):
        # Check if all characters in the string are English (ASCII) characters
        return all(ord(char) < 128 for char in input_string)

    def get_number2word(self, num):
        num_mapping = {
            **cfg.data["en"]["number_mapping"],
            **cfg.data["bn"]["number_mapping"],
        }
        if num in num_mapping:

            return num_mapping[num]
        return num

    def label_repeats(self, number):
        result = []
        digit_map = cfg.data["en"]["number_mapping"]
        c_number = []
        for i in number:
            status = self.contains_only_english(i)
            if status == False:
                if i in cfg._bangla2english_digits_mapping:
                    c_n = cfg._bangla2english_digits_mapping[i]
                    c_number.append(c_n)
                else:
                    c_number.append(i)
            else:
                c_number.append(i)
        number = c_number
        i = 0
        n = len(number)
        while i < n:
            if i + 2 < n and number[i] == number[i + 1] == number[i + 2]:
                result.append(cfg.special_map[number[i] * 3])
                i += 3
            elif i + 1 < n and number[i] == number[i + 1]:
                result.append(cfg.special_map[number[i] * 2])
                i += 2
            else:
                if number[i] in digit_map:
                    # print("number[i] : ", number[i], type(number[i]))
                    result.append(digit_map[number[i]])
                elif number[i] == "-":
                    result.append(" ")
                i += 1

        return " ".join(result)

    def phn_num_extractor(self, text):
        phone_numbers = re.findall(self.pattern, text)

        sorted_matches = sorted(phone_numbers, key=len, reverse=True)
        for phone_number in sorted_matches:

            modify_phone_number = "".join(re.split(r"[- ]", phone_number))

            # print(modify_phone_number)

            first_3_character = modify_phone_number.strip()[:3]
            if (
                first_3_character in self.number_extention
                or first_3_character in self.phn_number
                or 11 <= len(modify_phone_number)
                or len(modify_phone_number) <= 14
            ):

                temp_string = ""
                if "+" == modify_phone_number[0]:
                    # print(modify_phone_number[1:])
                    temp_string = (
                        "প্লাস" + " " + self.label_repeats(modify_phone_number[1:])
                    )
                else:
                    repate_string = self.label_repeats(modify_phone_number)
                    # print(repate_number)
                    temp_string = " " + repate_string

            phone_number_string = temp_string.strip()

            text = text.replace(phone_number, phone_number_string)
            # print(phone_number_string)
        # print(text)
        return text


if __name__ == "__main__":

    text = "ডিজিটাল রেজিস্ট্রেশন সার্টিফিকেট সংক্রান্ত 01790540211124562 যোগাযোগ করতে হলে 01790-540211 অথবা 01790-541111 নম্বরে যোগাযোগ করতে হবে 01790540211, +8801790540211, ০১৭৯০৫৪০২১১, +৮৮০১৭৯০৫৪০২১১"
    pne = PhoneNumberExtractor()
    process_text = pne.phn_num_extractor(text)
    print("input : ", text)
    print("output : ", process_text)
