import re
from .parser import NumberParser, TextParser
from .config import Config as cfg

npr, tp = NumberParser(), TextParser()


class Word2NumberMap:

    def __init__(self):
        pass

    def equation_of_sare_and_der(self, value: str, fraction: float) -> float:
        """
        Convert word if start bangla word like "সাড়ে", সারে, দেড়, দের
        and return numerical value
        """
        re_value = int(value.replace(value[0], "1"))
        return (re_value * fraction) + int(value)

    def equation_of_arai(self, value: str, fraction: float) -> float:
        """
        Convert word if the start bangla word like "আড়াই" or "আরাই"
        and return numerical value
        """
        return int(value) * fraction

    # def call_function()

    def adjust_value_conversion(self, value, sum_status=False):
        """
        Convert adjust value with numerical representation

        """

        # print("adjust_value_conversion : ", value, sum_status)

        status, adjust_name = False, ""
        for v in value:
            if v in cfg.adjust_number:
                adjust_name = v
                status, sum_status = True, False
                break
        if status:
            if len(value) == 3 and value[1].isdigit() and value[2].isdigit():
                number = str(int(value[1]) + int(value[2]))
            else:
                number = str(value[1])

            fraction_value = cfg.adjust_number[adjust_name]
            function_name = cfg.function_mapping[adjust_name]

            if hasattr(self, function_name) and callable(getattr(self, function_name)):
                func = getattr(self, function_name)
                return_value = func(number, fraction_value)
                # print("return value : ", str(int(return_value)), sum_status)
                return str(int(return_value)), sum_status
            
        # print("return value : ", value, sum_status)
        return value, sum_status

    def check_last_chars(self, word: str) -> bool:
        """
        Checking last character match with target character
        """
        for char in cfg.target_chars:
            if word.endswith(char):
                return True, char
        return False, None

    def sum_status(self, lst: list) -> bool:
        """
        Cheching the group word sum status

        """
        status_list = []
        for sublist in lst:
            x = [
                "1" if i in sublist else "0"
                for i in cfg.checking_hunderds + cfg.checking_adjust
            ]
            if "1" in x:
                status_list.append(True)
            else:
                status_list.append(False)
        return status_list

    def word_clustering(self, input_list: list) -> list:
        """
        Grouping of the word from the list of text
        """
        output, temp_sequence = [], []
        i = 0
        while i < len(input_list):
            input_list[i] = input_list[i].replace("শত00", "শত")
            input_list[i] = input_list[i].replace("শো00", "শত")
            if input_list[i].isdigit():
                if len(input_list[i]) == 2 and len(input_list) - 1 != i:
                    if input_list[i + 1] in cfg.checking_hunderds:
                        temp_sequence.append(input_list[i])
                        output.append(temp_sequence)
                    else:
                        temp_sequence.append(input_list[i])
                        output.append(temp_sequence)
                        temp_sequence = []

                elif len(input_list) - 1 == i:
                    temp_sequence.append(input_list[i])
                    output.append(temp_sequence)
                else:
                    temp_sequence.append(input_list[i])
            elif (
                input_list[i] in cfg.decimale_chunks
                or input_list[i] in cfg.fraction_int
            ):
                temp_sequence.append(input_list[i])
            elif input_list[i] in cfg.hundreds:
                temp_sequence.append(input_list[i])
            elif input_list[i] in cfg.checking_conjugative_number:
                temp_sequence.append(input_list[i])
            elif input_list[i] in cfg.en_doshok_map:
                temp_sequence.append(input_list[i])
            elif input_list[i] in cfg.adjust_number:
                temp_sequence.append(input_list[i])
            else:
                if temp_sequence:
                    output.append(temp_sequence)
                    temp_sequence = []
            i += 1
        return output

    def checking_hundreds_only(self, input_list: list) -> bool:
        """
        Checking status if all are handerds word

        """
        all_numeric_status = all(item.isdigit() for item in input_list)
        if all_numeric_status:
            return False
        for item in input_list:
            if (
                item in cfg.decimale_chunks
                or item in cfg.adjust_number
                or item in cfg.fraction_int
                or item in cfg.conjugative_number
                or item in cfg.en_doshok_map
            ):
                return False
        return True

    def clustring_consecutive_hunderd(self, input_list: list) -> [list, list]:
        """
        Clustering consecutinve handerd with sum status

        """
        temp, output_list, output_status = [], [], []
        for i, value in enumerate(input_list):
            if value in cfg.bn_hundreds:
                temp.append(value)
                if i == len(input_list) - 1 or not input_list[i + 1].isdigit():
                    output_list.append(temp), output_status.append(False)
                    temp = []
            elif value.isdigit():
                temp.append(value)
                if i == len(input_list) - 1 or not input_list[i + 1].isdigit():
                    output_list.append(temp), output_status.append(True)
                    temp = []
            else:
                output_list.append([value]), output_status.append(False)
        return output_list, output_status

    # def find_word_index(self, text:str, word:str)->list:
    #     """
    #     Word spanning position
    #     """
    #     start  = text.find(word)
    #     end = start+len(word)
    #     return [start, end]

    # def replace_text_at_position(self, text:str, replacement:str, start_pos:int, end_pos:int)->str:
    #     """
    #     Replance text using text position

    #     """
    #     return text[:start_pos] + replacement + text[end_pos:]

    def converting_condition(
        self, word: str, final_value: list, c_data: list, index: int
    ) -> [list, int]:
        """
        Convert word to conditional mapping with digits
        """

        if word.isdigit():
            final_value.append(word)
        elif word in cfg.decimale_chunks:
            if final_value:
                value = final_value[-1]
                d_c = int(cfg.decimale_chunks[word])
                if value.isdigit():
                    final_value.append(str((d_c * int(value)) - int(value)))
                else:
                    final_value.append(d_c)
            else:
                final_value.append(int(cfg.decimale_chunks[word]))
        elif word in cfg.bn_hundreds:
            final_value.append(cfg.bn_hundreds[word])
        elif word in cfg.en_doshok_map:
            final_value.append(cfg.en_doshok_map[word])
        elif word in cfg.fraction_int:
            final_value.append(cfg.fraction_int[word])
        elif word in cfg.conjugative_number:
            c_n = int(cfg.conjugative_number[word]) - 1
            if len(c_data) > index + 1:
                l_value = [str(c_data[index + 1])] * c_n
            else:
                l_value = cfg.conjugative_number[word]
            final_value.extend(l_value)
        else:
            final_value.append(word)

        # print("final_value : ", final_value)
        return final_value, index

    def converting2digits(
        self, results: list, text_list: list, sum_status_list: list
    ) -> str:
        """

        Converting word to digit and if have hunderds only then cluster again

        """
        original_text = " ".join(text_list)

        replance_text_and_spaning_number = []
        for result_chunk, status in zip(results, sum_status_list):

            # checking hunderds only and return status
            hundreds_status = self.checking_hundreds_only(result_chunk)
            # print("hundreds_status : ", hundreds_status, result_chunk, status)

            # generate number clustring
            if hundreds_status:
                clustring_data, clustring_status = self.clustring_consecutive_hunderd(
                    result_chunk
                )
            else:
                clustring_data, clustring_status = [result_chunk], [status]
            for c_data, c_status in zip(clustring_data, clustring_status):
                # print(c_data, c_status)
                replance_text = " ".join(c_data)
                word_spanning = npr.find_word_index(original_text, replance_text)

                # print(word_spanning, original_text[word_spanning[0]:word_spanning[1]])

                index, final_value = 0, []
                for c_d in c_data:
                    final_value, index = self.converting_condition(
                        c_d, final_value, c_data, index
                    )
                    index += 1
                value, status = self.adjust_value_conversion(
                    final_value, sum_status=c_status
                )
                # print("return value2 : ", value, status)
                if status:
                    numbers = str(sum(int(num) for num in value))
                elif isinstance(value, str):
                    numbers = value
                else:
                    numbers = "".join(value)

                replance_text_and_spaning_number.append([numbers, (word_spanning[0], word_spanning[1])])
        sorted_data = sorted(replance_text_and_spaning_number, key=lambda x: x[1][0], reverse=True)
        unique_data = []
        seen = set()
        for item in sorted_data:
            if (item[0], item[1]) not in seen:
                unique_data.append(item)
                seen.add((item[0], item[1]))

        for value in unique_data:
            original_text = npr.replace_text_at_position(original_text, value[0], value[1][0], value[1][1])
        # print(original_text)

        return original_text

    def replace_word_to_number(self, text: list) -> list:
        """
        Word to numerical digit conversation

        """
        index = 0
        for t in text:
            if t in cfg.bn_word_map:
                text[index] = cfg.bn_word_map[t]
            elif t in cfg.en_number_mapping:
                text[index] = cfg.en_number_mapping[t]
            else:
                pass
            index += 1
        return text

    def normalize(self, text: str) -> list:
        """

        This funcation normalize the text like white space and decimal number

        Arg:
            text{string}    : input string

        Return:
            text_list{list} : process text list space spliting

        """
        text = tp.collapse_whitespace(text)
        texts = text.split(" ")
        text_list = []
        for word in texts:
            status, char = self.check_last_chars(word)
            if status:
                if word not in cfg.bn_word_map:
                    if word[:-2] in cfg.bn_word_map:
                        rword = npr.number_processing(
                            str(int(cfg.bn_word_map[word[:-2]]) * 100)
                        )
                        rword = rword.replace(" শত", "শত")
                        text_list.extend(rword.split(" "))
                    else:
                        text_list.append(word)
                else:
                    text_list.append(word)
            else:
                text_list.append(word)
        return text_list

    def convert_word2number(self, text):
        text = self.normalize(text + " ")
        text_list = self.replace_word_to_number(text)
        results = self.word_clustering(text_list)
        sum_status_list = self.sum_status(results)
        text = self.converting2digits(results, text_list, sum_status_list)
        return text


if __name__ == "__main__":

    texts = [
        "আমি এক দুই তিন চার পাঁচ টু থ্রি ফাইভ ছয় সেভেন এইট নাইন শূন্য আমার ফোন নাম্বার জিরো ওয়ান ডাবল সেভেন",
        "ওয়ান ডাবল নাইন টু",
        "একশ বিশ টাকা",
        "জিরো টু ডাবল ওয়ান",
        "জিরো ওয়ান ডাবল সেভেন থ্রি ডাবল ফাইভ নাইন থ্রি সেভেন নাইন",
        "আমার ফোন নম্বর জিরো ওয়ান ডাবল সেভেন থ্রি ডাবল ফাইভ নাইন থ্রি সেভেন নাইন",
        "ট্রিপল টু ওয়ান",
        "দুই হাজার চারশো বিশ",
        "দুই হাজার চারশ  বিশ",
        "হাজার বিশ",
        "ডাবল নাইন টু",
        "এক লক্ষ চার হাজার দুইশ",
        "এক লক্ষ চার হাজার দুইশ এক",
        "এক লক্ষ চার হাজার দুইশ এক টাকা এক দুই",
        "আমাকে এক লক্ষ দুই হাজার টাকা দেয়",
        "আমাকে এক লক্ষ দুই হাজার এক টাকা দেয় এন্ড তুমি বিশ হাজার টাকা নিও এন্ড এক লক্ষ চার হাজার দুইশ এক টাকা এক ডবল দুই",
        "ছয় হাজার বিশ",
        "আমার সাড়ে পাঁচ হাজার",
        "আমার সাড়ে তিনশ",
        "আড়াই হাজার",
        "আড়াই লক্ষ",
        "ডেরশ",
        "আমাকে ডেরশ টাকা দেয়",
        "সাড়ে পাঁচ কোটি টাকা",
        "সাড়ে 1254 টাকা",
        "জিরো",
        "একশ বিশ take একশ",
        "জিরো টু ডাবল ওয়ান",
        "জিরো টু ওয়ান ওয়ান",
        "থ্রি ফোর ফাইভ এইট",
        "একশ বিশ টাকা",
        "ডাবল ওয়ান ডবল টু",
        "জিরো ওয়ান টু",
        "থ্রি ফোর ফাইভ সিক্স",
        "সেভেন এইট নাইন টেন",
        "একশ দুইশ তিনশ",
        "চারশ পাঁচশ",
        "ছয়শ সাতশ",
        "আটশ নয়শ",
        "দশ তিরানব্বই",
        "ট্রিপল থ্রি টু",
        "শূন্য এক দুই তিন",
        "চার পাঁচ ছয় সাত",
        "আট নয় দশ এগারো",
        "বারো তেরো চৌদ্দ পনেরো",
        "ষোল সতেরো আঠারো উনিশ",
        "বিশ একুশ বাইশ তেইশ",
        "চব্বিশ পঁচিশ ছাব্বিশ সাতাশ",
        "আঠাশ ঊনত্রিশ ত্রিশ একত্রিশ",
        "বত্রিশ তেত্রিশ চৌত্রিশ পঁয়ত্রিশ",
        "ছত্রিশ সাঁইত্রিশ আটত্রিশ ঊনচল্লিশ",
        "চল্লিশ একচল্লিশ বিয়াল্লিশ তেতাল্লিশ",
        "চুয়াল্লিশ পঁয়তাল্লিশ ছেচল্লিশ সাতচল্লিশ",
        "আটচল্লিশ ঊনপঞ্চাশ পঞ্চাশ একান্ন",
        "বাহান্ন তিপ্পান্ন চুয়ান্ন পঞ্চান্ন",
        "ছাপ্পান্ন সাতান্ন আটান্ন ঊনষাট",
        "ষাট একষট্টি বাষট্টি তেষট্টি",
        "চৌষট্টি পঁয়ষট্টি ছেষট্টি সাতষট্টি",
        "আটষট্টি ঊনসত্তর সত্তর একাত্তর",
        "বাহাত্তর তিয়াত্তর চুয়াত্তর পঁচাত্তর",
        "ছিয়াত্তর সাতাত্তর আটাত্তর ঊনআশি",
        "আশি একাশি বিরাশি তিরাশি",
        "চুরাশি পঁচাশি ছিয়াশি সাতাশি",
        "আটাশি ঊননব্বই নব্বই একানব্বই",
        "বিরানব্বই তিরানব্বই চুরানব্বই পঁচানব্বই",
        "ছিয়ানব্বই সাতানব্বই আটানব্বই নিরানব্বই",
        "এক লক্ষ চার হাজার দুইশ এক টাকা এক দুই",
        "তিনশ পঁচিশ পাঁচশ",
        "তিনশ পঁচিশ পাঁচশ এক",
        "চা-পুন",
        "ওকে",
        "ডের আউটস্ট্যান্ডিং কত",
        "ডাবল",
        "নাইন ডাবল এইট",
        "দশ বারো এ এগুলা একশ একশ দুই",
    ]

    # texts = ["দশ বারো এ এগুলা একশ একশ দুই"]

    wnm = Word2NumberMap()
    for i in texts:
        print("=" * 40)
        print("input : ", i)
        text = wnm.convert_word2number(i)
        print("output : ", text)
        print("=" * 40)
