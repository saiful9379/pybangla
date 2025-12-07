import re
number_mapping = {
        "." : "ডট",
        "0": "জিরো",
        "1": "ওয়ান",
        "2": "টু",
        "3": "থ্রি",
        "4": "ফোর",
        "5": "ফাইভ",
        "6": "সিক্স",
        "7": "সেভেন",
        "8": "এইট",
        "9": "নাইন",
        "০": "শূন্য",
        "১": "এক",
        "২": "দুই",
        "৩": "তিন",
        "৪": "চার",
        "৫": "পাঁচ",
        "৬": "ছয়",
        "৭": "সাত",
        "৮": "আট",
        "৯": "নয়",
    }

patterns = [
    # Bengali numerals with dots
    r'[০-৯]+(?:\.[০-৯]+){2,}',
    
    # English numerals with dots
    r'[0-9]+(?:\.[0-9]+){2,}',
    
    # Mixed Bengali/English numerals with dots
    r'[0-9০-৯]+(?:\.[0-9০-৯]+){2,}',
]

def multiple_dotted_numbers_process(text: str) -> list:
    """
    Extract numbers with multiple dots (IP addresses, version numbers, etc.)
    Supports both Bengali (০-৯) and English (0-9) numerals
    """
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
          for matche in matches:
            match_string = ""
            for m in matche:
              if m in number_mapping:
                if "." in m:
                  match_string += " "+number_mapping[m]+","
                else:
                  match_string += " "+number_mapping[m]
              else:
                match_string += m
            text = text.replace(matche, match_string)
    # Remove duplicates while preserving order
    return text



if __name__ == "__main__":
    # Test examples
    test_texts = [
        "আপনি চাইলে আবার শুনে নিন: ১১৫.১২৭.২০৭.২০ আর কোনো সংখ্যা বা তথ্য জানতে চান?",
        "IP address হলো ১১৫.১২৭.২০৭ এবং 192.168.1.1 দুইটাই কাজ করবে",
        "Version ২.১০.৩ এবং 3.14.159 দুইটাই সাপোর্টেড",
        "Server IP: 10.0.0.1 এবং ১০.০.০.২ উভয়ই ব্যবহার করুন",
        "Server IP: 10.0 এবং ১০.০ উভয়ই ব্যবহার করুন",
        "Server IP: 10 এবং ১০ উভয়ই ব্যবহার করুন",
    ]

    print("=" * 60)
    print("DOTTED NUMBER EXTRACTION (IP, Version, etc.)")
    print("=" * 60)

    for text in test_texts:
        print(f"\nText: {text}")
        process_text = multiple_dotted_numbers_process(text)
        print(f"Processed Text: {process_text}")