from .config import Config as cfg

data_map = cfg.data["bn"]["number_mapping"]


def normalize_with_3_pattern(number):
    i = 0
    normalize_string = ""
    for item in number:
        n_item = data_map[item] if item in data_map else item
        normalize_string += n_item
        if i % 3 == 0 and i != 0:  # প্রতি ৩টার পর
            normalize_string += "। "  # এখানে দাড়ি যোগ করছি
        else:
            normalize_string += ", "
        i += 1
    # print("normalize_string : ", normalize_string)
    return normalize_string


if __name__ == "__main__":
    number = "০১২৩৪৫৬৭৮৯"
    map_number = normalize_with_3_pattern(number)
    print("map_number : ", map_number)

# Examples:
# "0123456789" -> "0, 1, 2। 3, 4, 5। 6, 7, 8, 9"
# "01234567890123" -> "0, 1, 2। 3, 4, 5। 6, 7, 8, 9। 0, 1, 2, 3"
