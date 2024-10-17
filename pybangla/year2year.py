# import re

# def year_to_year(sentence):
#     connectors = ["থেকে", "হতে", "চেয়ে"]
#     suffixes = [
#         "সালে",
#         "সাল",
#         "শতাব্দী",
#         "শতাব্দীর",
#         "শতাব্দীতে",
#         "খ্রিস্টাব্দ",
#         "খ্রিস্টাব্দের",
#         "খ্রিস্টপূর্বাব্দের",
#     ]
    
#     # Create patterns
#     digit_pattern = r"[0-9০-৯]{4}"
#     connector_pattern = "|".join(connectors)
#     suffix_pattern = "|".join(suffixes)

#     # Regular expression pattern
#     pattern = rf"({digit_pattern})\s*({connector_pattern})\s*({digit_pattern})\s*({suffix_pattern})"

#     # Compile the regex for better performance
#     regex = re.compile(pattern)

#     # Find all matches in the sentence
#     matches = regex.findall(sentence)

#     if matches:
#         for match in matches:
#             extracted_block = " ".join(match)

#             print(f"Extracted block: {extracted_block}")
#     else:
#         print("No match found in sentence.")

# if __name__ == "__main__":
#     # Sample sentences
#     sentences = [
#         "১৯৫৪ থেকে ২০১৪ সালে বাংলাদেশ আর মানুষ বুজতে শুরু করে",
#         "1234 হতে  ২০১৪ শতাব্দী বাংলাদেশ আর মানুষ বুজতে শুরু করে",
#         "২০২৩ চেয়ে  ২০১৪ সালের বাংলাদেশ আর মানুষ বুজতে শুরু ক",
#         "1995 থেকে 2014 শতাব্দীর বাংলাদেশ আর মানুষ বুজতে শুরু করে",
#         "1234 হতে  ২০১৪ সালে বাংলাদেশ আর মানুষ বুজতে শুরু করে",
#         "2023 চেয়ে 2014 সালে বাংলাদেশ আর মানুষ বুজতে শুরু ক",
#         "১৯৫৪ থেকে ২০১৪ সালে বাংলাদেশ আর মানুষ বুজতে শুরু করে",
#         "1234 হতে  ২০১৪ শতাব্দীর বাংলাদেশ আর মানুষ বুজতে শুরু করে",
#         "২০২৩ চেয়ে  ২০১৪ সালের বাংলাদেশ আর মানুষ বুজতে শুরু ক",
#         "1995 থেকে 2014 শতাব্দীর বাংলাদেশ আর মানুষ বুজতে শুরু করে",
#         "1234 হতে  ২০১৪ শতাব্দীতে বাংলাদেশ আর মানুষ বুজতে শুরু করে",
#         "2023 চেয়ে 2014 সাল বাংলাদেশ আর মানুষ বুজতে শুরু ক",
#         "2023 চেয়ে 2014 খ্রিস্টাব্দ বাংলাদেশ আর মানুষ বুজতে শুরু ক",
#         "2023 চেয়ে 2014 খ্রিস্টাব্দের বাংলাদেশ আর মানুষ বুজতে শুরু ক",
#         "2023 চেয়ে 2014 খ্রিস্টাব্দ বাংলাদেশ আর মানুষ বুজতে শুরু ক",
#         "2023 চেয়ে 2014খ্রিস্টপূর্বাব্দের বাংলাদেশ আর মানুষ বুজতে শুরু ক 2023 চেয়ে 2030 খ্রিস্টাব্দ",
#         "2023 চেয়ে 1115 বাংলাদেশ আর মানুষ বুজতে শুরু ক",
#     ]
    
#     for sentence in sentences:
#         year_to_year(sentence)


import re

def year_to_year(sentence):
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

    # Compile the regex for better performance
    regex = re.compile(pattern)

    # Use finditer to get match objects with positions
    matches = regex.finditer(sentence)

    result = []
    for match in matches:
        extracted_block = " ".join(match)
        print("extracted_block:", extracted_block)
        start_year = match.group(1)  # First year
        end_year = match.group(3)    # Second year
        start_pos, end_pos = match.span()  # Get the starting and ending position of the entire match
        result.append({
            "years": [start_year, end_year],
            "start_pos": start_pos,
            "end_pos": end_pos
        })
    
    if result:
        for res in result:
            print(f"Extracted years: {res['years']}, Start position: {res['start_pos']}, End position: {res['end_pos']}")
    else:
        print("No match found in sentence.")

if __name__ == "__main__":
    # Sample sentences
    sentences = [
        "১৯৫৪ থেকে ২০১৪ সালে বাংলাদেশ আর মানুষ বুজতে শুরু করে ",
        "1234 হতে  ২০১৪ শতাব্দী বাংলাদেশ আর মানুষ বুজতে শুরু করে",
        "২০২৩ চেয়ে  ২০১৪ সালের বাংলাদেশ আর মানুষ বুজতে শুরু ক",
        "1995 থেকে 2014 শতাব্দীর বাংলাদেশ আর মানুষ বুজতে শুরু করে",
        "1234 হতে  ২০১৪ সালে বাংলাদেশ আর মানুষ বুজতে শুরু করে",
        "2023 চেয়ে 2014 সালে বাংলাদেশ আর মানুষ বুজতে শুরু ক",
        "১৯৫৪ থেকে ২০১৪ সালে বাংলাদেশ আর মানুষ বুজতে শুরু করে",
        "1234 হতে  ২০১৪ শতাব্দীর বাংলাদেশ আর মানুষ বুজতে শুরু করে",
        "২০২৩ চেয়ে  ২০১৪ সালের বাংলাদেশ আর মানুষ বুজতে শুরু ক",
        "1995 থেকে 2014 শতাব্দীর বাংলাদেশ আর মানুষ বুজতে শুরু করে",
        "1234 হতে  ২০১৪ শতাব্দীতে বাংলাদেশ আর মানুষ বুজতে শুরু করে",
        "2023 চেয়ে 2014 সাল বাংলাদেশ আর মানুষ বুজতে শুরু ক",
        "2023 চেয়ে 2014 খ্রিস্টাব্দ বাংলাদেশ আর মানুষ বুজতে শুরু ক",
        "2023 চেয়ে 2014 খ্রিস্টাব্দের বাংলাদেশ আর মানুষ বুজতে শুরু ক",
        "2023 চেয়ে 2014 খ্রিস্টাব্দ বাংলাদেশ আর মানুষ বুজতে শুরু ক",
        "2023 চেয়ে 2014 খ্রিস্টপূর্বাব্দের বাংলাদেশ আর মানুষ বুজতে শুরু ক 2023চেয়ে 2030 খ্রিস্টাব্দ",
        "2023 চেয়ে 1115 বাংলাদেশ আর মানুষ বুজতে শুরু ক",
        "2023 , 1115 বাংলাদেশ আর মানুষ বুজতে শুরু ক ২০১৪ সালে"
    ]
    
    for sentence in sentences:
        year_to_year(sentence)

