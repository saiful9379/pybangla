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
            "096",
            "০৯৬"
        ]
        # self.pattern = r'(?:\+?৮৮)?০১[৩-৯][০-৯]{2}-?[০-৯]{6}|(?:\+88)?01[3-9]\d{2}-?\d{6}'
        self.pattern = r"(?:\+?৮৮)?০১[৩-৯][০-৯]{2}-?[০-৯]{6}(?=[, ]|$)|(?:\+88)?01[3-9]\d{2}-?\d{6}(?=[, ]|$)"
        self.plux = {"+": "প্লাস"}
        self.ip_phone_number_patter = r"(?:০৯৬\d{2}-?[০-৯]{6})|(?:096\d{2}-?\d{6})"  # Pattern to match numbers starting with 096 (English) or ০৯৬ (Bengali)

        self.postfix_pattern = r"\[\d{5}-PHN_NUMBER\]|\[[০-৯]{5}-PHN_NUMBER\]" 

    def checking_postfix_phn_number(self, text):
        # Pattern to match both English and Bengali patterns for PHN_NUMBER
        
        # Input text
        # text = """
        # Here are some patterns:[16622-PHN_NUMBER]patterns, [১৬৬৭৮-PHN_NUMBER], and some other text without the pattern.
        # """
        # Extract matches for the specific pattern
        matches = re.findall(self.postfix_pattern, text)
        for phn_n in matches:
            r_phn = (phn_n.replace("[", "")).split("-PHN_NUMBER")[0]
            textual_phn_num = self.label_repeats(r_phn)
            text = text.replace(phn_n, " "+textual_phn_num+" ")
        return text

    def ip_phone_number(self, text):

        # # Pattern to match numbers starting with 096 (English) or ০৯৬ (Bengali)
        # pattern = r"(?:০৯৬\d{2}-?[০-৯]{6})|(?:096\d{2}-?\d{6})"
        # # Input text
        # text = """
        # ডিজিটাল রেজিস্ট্রেশন ০৯৬১২৩৪৫৬৭৮, ডিজিটাল রেজিস্ট্রেশন ০৯৬১০-০১০৬১৬, ডিজিটাল রেজিস্ট্রেশন 09612745678, ডিজিটাল রেজিস্ট্রেশন 09610-010616, 01790540211, +8801790540211, ০১৭৯০৫৪০২১১
        # """
        # Extract matches for the specific pattern
        phone_number = re.findall(self.ip_phone_number_patter, text)
        return phone_number

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
    
    def add_space_into_text(self, text):
        # Find all number blocks with their positions
        number_blocks = [(match.group(), match.start(), match.end()) for match in re.finditer(r'\d+[-,./]?\d*', text)]
        # print(number_blocks)

        extracted_data = []
        for number, start, end in number_blocks:
            extracted_data.append((number, start, end))

        sorted_data_reverse = sorted(extracted_data, key=lambda x: x[1], reverse=True)

        # print(sorted_data_reverse)

        for number, start, end in sorted_data_reverse:
            first_3_character = number.strip()[:3]
            # print("first_3_character : ", first_3_character)
            if first_3_character in self.number_extention or first_3_character in self.phn_number:
                if len(number)<=11 or len(number)<= 14: 
                    # print("number1 : ", number)
                    if start !=0 and text[start-1]!=" ":
                        if text[start-1]=="+":
                            text = text[:start-1] + ' ' + text[start-1:]
                            end = end+1
                        elif text[start-1]=="." or text[start-1]==",":
                            text = text 
                        else:
                            text = text[:start] + ' ' + text[start:]
                            end = end+1
                    if end !=len(text) and text[end+1]!=" ":
                        if text[end+1]=="." or text[end+1]==",":
                            text = text
                        else:
                            text = text[:end] + ' ' + text[end:]
        text = re.sub(r'\s+', ' ', text).strip()
        # print(text)
        return text

    def phn_num_extractor(self, text):

        # add spance numerical value staring and ending point
        text = self.checking_postfix_phn_number(text)
        text = self.add_space_into_text(text)
        # print("adding space : ", text)
        phone_numbers = re.findall(self.pattern, text)
        #handel 096 patter phone number
        ip_phone_number = self.ip_phone_number(text)

        sorted_matches = sorted(phone_numbers+ip_phone_number, key=len, reverse=True)
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
