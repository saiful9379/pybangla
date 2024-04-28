
import re
from .parser import NumberParser, TextParser

np, tp = NumberParser(), TextParser()

bn_word_map = {
    'শূন্য': '0', 'এক': '1', 'দুই': '2', 'তিন': '3', 'চার': '4', 'পাঁচ': '5', 'ছয়': '6', 'সাত': '7', 'আট': '8', 'নয়': '9', 'দশ': '10', 
    'এগারো': '11', 'বারো': '12', 'তেরো': '13', 'চৌদ্দ': '14', 'পনেরো': '15', 'ষোল': '16', 'সতেরো': '17', 'আঠারো': '18', 'উনিশ': '19', 'বিশ': '20',
    'একুশ': '21', 'বাইশ': '22', 'তেইশ': '23', 'চব্বিশ': '24', 'পঁচিশ': '25', 'ছাব্বিশ': '26', 'সাতাশ': '27', 'আঠাশ': '28', 'ঊনত্রিশ': '29', 'ত্রিশ': '30',
    'একত্রিশ': '31', 'বত্রিশ': '32', 'তেত্রিশ': '33', 'চৌত্রিশ': '34', 'পঁয়ত্রিশ': '35', 'ছত্রিশ': '36', 'সাঁইত্রিশ': '37', 'আটত্রিশ': '38', 'ঊনচল্লিশ': '39', 'চল্লিশ': '40', 
    'একচল্লিশ': '41', 'বিয়াল্লিশ': '42', 'তেতাল্লিশ': '43', 'চুয়াল্লিশ': '44', 'পঁয়তাল্লিশ': '45', 'ছেচল্লিশ': '46', 'সাতচল্লিশ': '47', 'আটচল্লিশ': '48', 'ঊনপঞ্চাশ': '49', 'পঞ্চাশ': '50', 
    'একান্ন': '51', 'বাহান্ন': '52', 'তিপ্পান্ন': '53', 'চুয়ান্ন': '54', 'পঞ্চান্ন': '55', 'ছাপ্পান্ন': '56', 'সাতান্ন': '57', 'আটান্ন': '58', 'ঊনষাট': '59', 'ষাট': '60', 
    'একষট্টি': '61', 'বাষট্টি': '62', 'তেষট্টি': '63', 'চৌষট্টি': '64', 'পঁয়ষট্টি': '65', 'ছেষট্টি': '66', 'সাতষট্টি': '67', 'আটষট্টি': '68', 'ঊনসত্তর': '69', 'সত্তর': '70', 
    'একাত্তর': '71', 'বাহাত্তর': '72', 'তিয়াত্তর': '73', 'চুয়াত্তর': '74', 'পঁচাত্তর': '75', 'ছিয়াত্তর': '76', 'সাতাত্তর': '77', 'আটাত্তর': '78', 'ঊনআশি': '79', 'আশি': '80', 
    'একাশি': '81', 'বিরাশি': '82', 'তিরাশি': '83', 'চুরাশি': '84', 'পঁচাশি': '85', 'ছিয়াশি': '86', 'সাতাশি': '87', 'আটাশি': '88', 'ঊননব্বই': '89', 'নব্বই': '90', 
    'একানব্বই': '91', 'বিরানব্বই': '92', 'তিরানব্বই': '93', 'চুরানব্বই': '94', 'পঁচানব্বই': '95', 'ছিয়ানব্বই': '96', 'সাতানব্বই': '97', 'আটানব্বই': '98', 'নিরানব্বই': '99'
}

bn_hundreds_1={'একশ': "100",'দুইশ': "200", 'তিনশ':"300",'চারশ': "400",'পাঁচশ':"500",'ছয়শ':"600",'সাতশ': "700",'আটশ':"800",'নয়শ':"900"}

bn_hundreds_2 = {i.replace(i[-1], "শত"): v for i, v in bn_hundreds_1.items()}
bn_hundreds_3 = {i.replace(i[-1], "শো"): v for i, v in bn_hundreds_1.items()}

bn_hundreds = {**bn_hundreds_1, **bn_hundreds_2, **bn_hundreds_3}


target_chars = ["শো", "শত", "শ"]
hundreds = list(bn_hundreds.keys())


checking_hunderds = ['একশ', 'দুইশ', 'তিনশ', 'চারশ', 'পাঁচশ', 'ছয়শ', 'সাতশ', 'আটশ', 'নয়শ', 'লক্ষ', 'হাজার', 'কোটি', 'লাখ', "একশত"]

# print("bn_hundreds : ", bn_hundreds)

# print(hundreds)
# print(bn_hundreds_2)

# en_hunderds = {}
# # bn_word = ['শূন্য', 'এক', 'দুই', 'তিন', 'চার', 'পাঁচ', 'ছয়', 'সাত', 'আট', 'নয়', 'দশ', 'এগারো', 'বারো', 'তেরো', 'চৌদ্দ', 'পনেরো', 'ষোল', 'সতেরো', 'আঠারো', 'উনিশ', 'বিশ', 'একুশ', 'বাইশ', 'তেইশ', 'চব্বিশ', 'পঁচিশ', 'ছাব্বিশ', 'সাতাশ', 'আঠাশ', 'ঊনত্রিশ', 'ত্রিশ', 'একত্রিশ', 'বত্রিশ', 'তেত্রিশ', 'চৌত্রিশ', 'পঁয়ত্রিশ', 'ছত্রিশ', 'সাঁইত্রিশ', 'আটত্রিশ', 'ঊনচল্লিশ', 'চল্লিশ', 'একচল্লিশ', 'বিয়াল্লিশ', 'তেতাল্লিশ', 'চুয়াল্লিশ', 'পঁয়তাল্লিশ', 'ছেচল্লিশ', 'সাতচল্লিশ', 'আটচল্লিশ', 'ঊনপঞ্চাশ', 'পঞ্চাশ', 'একান্ন', 'বাহান্ন', 'তিপ্পান্ন', 'চুয়ান্ন', 'পঞ্চান্ন', 'ছাপ্পান্ন', 'সাতান্ন', 'আটান্ন', 'ঊনষাট', 'ষাট', 'একষট্টি', 'বাষট্টি', 'তেষট্টি', 'চৌষট্টি', 'পঁয়ষট্টি', 'ছেষট্টি', 'সাতষট্টি', 'আটষট্টি', 'ঊনসত্তর', 'সত্তর', 'একাত্তর', 'বাহাত্তর', 'তিয়াত্তর', 'চুয়াত্তর', 'পঁচাত্তর', 'ছিয়াত্তর', 'সাতাত্তর', 'আটাত্তর', 'ঊনআশি', 'আশি', 'একাশি', 'বিরাশি', 'তিরাশি', 'চুরাশি', 'পঁচাশি', 'ছিয়াশি', 'সাতাশি', 'আটাশি', 'ঊননব্বই', 'নব্বই', 'একানব্বই', 'বিরানব্বই', 'তিরানব্বই', 'চুরানব্বই', 'পঁচানব্বই', 'ছিয়ানব্বই', 'সাতানব্বই', 'আটানব্বই', 'নিরানব্বই']
# en_word = ['জিরো', 'ওয়ান', 'টু', 'থ্রি', 'ফোর', 'ফাইভ', 'সিক্স', 'সেভেন', 'এইট', 'নাইন', 'টেন', 'ইলেভেন', 'টুয়েলভ', 'থার্টিন', 'ফোরটিন', 'ফিফটিন', 'সিক্সটিন', 'সেভেনটিন', 'এইটিন', 'নাইনটিন']


# en_word_dict = {value: str(i) for i, value in enumerate(en_word)}

# # print(en_word_dict)


decimale_chunks = {"কোটি" : "10000000",'লক্ষ': "100000", "লাখ": "100000", 'হাজার': "1000"}

adjust_number = {"সাড়ে":0.5, "সারে":0.5, "আড়াই": 2.5, "আরাই":2.5, "দেড়":0.5, "দের":0.5}


conjugative_number = {"ডবল": "2", "ডাবল": "2", "ট্রিপল": "3"}


en_number_mapping = {"জিরো": "0" ,"ওয়ান": "1", "টু": "2", "থ্রি":"3", "ফোর":"4", "ফাইভ":"5", "সিক্স":"6", "সেভেন":"7", "এইট":"8", "নাইন":"9", "টেন": "10"}
en_doshok_map = {'ইলেভেন':"11", 'টুয়েলভ':"12", 'থার্টিন':"13", 'ফোরটিন':"14", 'ফিফটিন':"15", 'সিক্সটিন':"16", 'সেভেনটিন':"17", 'এইটিন':"18", 'নাইনটিন':"19","টুয়েন্টি": "20", "থার্টি": "30", "ফর্টি":"40", "ফিফ্টি": "50", "সিক্সটি": "60", "সেভেন্টি":"70", "এটি": "80", "নাইনটি":"90"}
# positional_dict = {'শত':2, 'শো':2, 'হাজার':3,'লক্ষ':5,'কোটি':7, 'লাখ':5}

fraction_int = {"ডেরশ": "150", "দেরশ": "150", "আরাইশ": "250", "আড়াইশ": "250"}





function_mapping = {
                "সাড়ে"    : "equation_of_sare_and_der", 
                "সারে"    : "equation_of_sare_and_der", 
                "আড়াই"   : "equation_of_arai", 
                "আরাই"   : "equation_of_arai", 
                "দেড়"     : "equation_of_sare_and_der", 
                "দের"     : "equation_of_sare_and_der"
                }

checking_adjust = list(adjust_number.keys())
checking_conjugative_number = list(conjugative_number.keys())



def equation_of_sare_and_der(value , fraction ):
    re_value = int(value.replace(value[0], "1"))
    print(re_value*fraction)
    print(value, type(value), re_value, (re_value*int(fraction))+int(value))
    return (re_value*fraction)+int(value)

def equation_of_arai(value, fraction):
    return int(value)*fraction


def adjust_value_conversion(value, sum_status= False):

    status, adjust_name = False, ""

    for v in value:
        if v in adjust_number:
            adjust_name = v
            status, sum_status = True, False
            break
    if status:
        if len(value)==3 and value[1].isdigit() and  value[2].isdigit():
            number = str(int(value[1])+int(value[2]))
        else:
            number = str(value[1])

        fraction_value = adjust_number[adjust_name]
        function_name = function_mapping[adjust_name]

        # print("function_name : ", function_name, fraction_value)


        if function_name in globals() and callable(globals()[function_name]):
            func = globals()[function_name]
            return_value = func(number, fraction_value)
            # print("return value : ", return_value)

            return str(int(return_value)), sum_status
        

        # print("adjust_name : ", adjust_name, value)

    return value, sum_status

def check_last_chars(word):
    for char in target_chars:
        if word.endswith(char):
            return True, char
    return False, None

def normalize(text):
    text = tp.collapse_whitespace(text)
    texts = text.split(" ")
    text_list = []
    for word in texts:
        status, char = check_last_chars(word)
        if status:
            if word not in bn_word_map:
                if word[:-2] in bn_word_map:
                    value = bn_word_map[word[:-2]]
                    rword = str(int(value)*100)
                    rword = np.number_processing(rword)
                    rword = rword.replace(" শত", "শত")
                    text_list.extend(rword.split(" "))
                else:
                    text_list.append(word)
            else:
                text_list.append(word)
        else:
            text_list.append(word)
    return text_list


def replace_word_to_number_string(text):
    index = 0
    for t in text:
        if t in bn_word_map:
            text[index] = bn_word_map[t]
        elif t in en_number_mapping:
            text[index] = en_number_mapping[t]
        else:
            pass
        index+=1
    return text


def sum_status(lst):
    status_list = []
    for sublist in lst:
        x = ["1" if i in sublist else "0" for i in checking_hunderds+checking_adjust]
        if "1" in x:
            status_list.append(True)
        else:
            status_list.append(False)
    return status_list


   

def extract_values(input_list):
    output, temp_sequence = [], []
    i, previous_index = 0, 0
    while i < len(input_list):
        if input_list[i].isdigit():
            if len(input_list)-1 == i:
                temp_sequence.append(input_list[i])
                output.append(temp_sequence)
            else:
                temp_sequence.append(input_list[i])
        elif input_list[i] in decimale_chunks or input_list[i] in fraction_int:
            temp_sequence.append(input_list[i])
        elif input_list[i] in hundreds:
            temp_sequence.append(input_list[i])
        elif input_list[i] in checking_conjugative_number:
            temp_sequence.append(input_list[i])
        elif  input_list[i] in adjust_number:
            temp_sequence.append(input_list[i])
        else:
            if temp_sequence:
                output.append(temp_sequence)
                temp_sequence = []
        i+=1
    # print("extraction group :", output)
    return output



def checkin_hundreds_only(input_list):

    all_numeric_status = all(item.isdigit() for item in input_list)
    if all_numeric_status:
        return False
    
    for item in input_list:
        if item in decimale_chunks or item in adjust_number \
            or item in fraction_int or item in conjugative_number or item in en_doshok_map:
            return False
    return True


def split_consecutive_hunderd(input_list):
    temp, output_list, output_status = [], [], []
    for i, value in enumerate(input_list):
        if value in bn_hundreds:
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




def converting2digits(results:list, text_list:list, sum_status_list:list)->str:

    # print("text_list : ", text_list)
    original_text = " ".join(text_list)
    print("original_text", original_text)
    for result_chunk, status in zip(results, sum_status_list):

        print("result_chunk :", result_chunk)

        hundreds_status = checkin_hundreds_only(result_chunk)

        print("hundreds_status : ",  hundreds_status)

        if hundreds_status:
            clustring_data, clustring_status = split_consecutive_hunderd(result_chunk)
            print(clustring_data, clustring_status)
        else:
            clustring_data, clustring_status = [result_chunk], [status]

        for c_data, c_status in zip(clustring_data, clustring_status):
        
            # print("list : ", result_chunk)
            replance_text = " ".join(c_data)
            # print("replance_text : ", replance_text)
            index, final_value = 0, []
            for r in c_data:
                if r.isdigit():
                    final_value.append(r)
                elif r in decimale_chunks:
                    # print("decimale_chunks", r, final_value)
                    if final_value:
                        value = final_value[-1]
                        d_c = int(decimale_chunks[r])
                        if value.isdigit():
                            calculated_value = (d_c*int(value))-int(value)
                            final_value.append(str(calculated_value))
                        else:
                            final_value.append(d_c)
                    else:
                        d_c = int(decimale_chunks[r])
                        final_value.append(d_c)
                elif r in bn_hundreds:
                    final_value.append(bn_hundreds[r])
                elif r in fraction_int:
                    final_value.append(fraction_int[r])
                elif r in conjugative_number:
                    c_n = int(conjugative_number[r])-1
                    # print("result chunk : ", result_chunk, len(result_chunk), index+1)
                    if len(c_data) > index+1:
                        n_value = c_data[index+1]
                        l_value = [str(n_value)]*c_n
                    else:
                        l_value = conjugative_number[r]
                    final_value.extend(l_value)
                else:
                    final_value.append(r)
                index += 1
            value, status = adjust_value_conversion(final_value, sum_status= c_status)

            print("==============", value, status)
            
            if status:
                # print("status : ", status)
                # print(value)
                numbers = str(sum(int(num) for num in value))
                print(replance_text, numbers)
            elif isinstance(value, str):
                numbers = value
                print(numbers)
            else:
                numbers = "".join(value)
                print(numbers)

            print("converted value : ", numbers)

            original_text = original_text.replace(replance_text, numbers)

            print("final text : ", original_text)

    return original_text

def word2number(text):

    text = normalize(text+" ")
    text_list = replace_word_to_number_string(text)
    results = extract_values(text_list)
    sum_status_list = sum_status(results)


    text = converting2digits(results, text_list, sum_status_list)

    # print("processing text : ", text)
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
        "দশ বারো এ এগুলা একশ একশ দুই"
        ]
    
    texts = ["দশ বারো এ এগুলা একশ একশ দুই"]
    for i in texts:
        print("="*40)
        print("input : ", i)
        text = word2number(i)
        print("output : ", text)
        print("="*40)