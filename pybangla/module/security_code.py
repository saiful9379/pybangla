import re

number_mapping = {
    "0": "জিরো", "1": "ওয়ান", "2": "টু", "3": "থ্রি", "4": "ফোর",
    "5": "ফাইভ", "6": "সিক্স", "7": "সেভেন", "8": "এইট", "9": "নাইন",
    "০": "শূন্য", "১": "এক", "২": "দুই", "৩": "তিন", "৪": "চার",
    "৫": "পাঁচ", "৬": "ছয়", "৭": "সাত", "৮": "আট", "৯": "নয়"
}

def digits_to_words(digits: str) -> str:
    """Convert a string of ASCII/Bengali digits to space-separated words using number_mapping."""
    return ", ".join(number_mapping.get(ch, ch) for ch in digits)

def build_patterns():
    digit = r'[0-9০-৯]+'
    patterns = [
        # Last/First X digits
        (rf'(?:শেষ|প্রথম)\s*{digit}\s*(?:সংখ্যা|ডিজিট)\s*({digit})', 'Last X digits'),

        # OTP
        (rf'(?:ওটিপি\s*\(OTP\)|OTP\s*\(ওটিপি\)|ওটিপি|otp|OTP)\s*[:=-]?\s*({digit})', 'OTP'),

        # PIN
        (rf'(?:পিন\s*\(PIN\)|PIN\s*\(পিন\)|পিন|pin|PIN)\s*[:=-]?\s*({digit})', 'PIN'),

        # Code
        (rf'(?:কোড\s*\(code\)|code\s*\(কোড\)|কোড|code|CODE)\s*[:=-]?\s*({digit})', 'Code'),

        # CVV / CVC
        (rf'(?:সিভিভি\s*\(CVV\)|CVV\s*\(সিভিভি\)|সিভিভি|cvv|CVV)\s*[:=-]?\s*({digit})', 'CVV'),
        (rf'(?:সিভিসি\s*\(CVC\)|CVC\s*\(সিভিসি\)|সিভিসি|cvc|CVC)\s*[:=-]?\s*({digit})', 'CVV'),

        # Generic সংখ্যা
        (rf'সংখ্যা\s*({digit})', 'সংখ্যা'),

        # Security code
        (rf'(?:সিকিউরিটি\s*কোড\s*\(security\s*code\)|security\s*code\s*\(সিকিউরিটি\s*কোড\)|সিকিউরিটি\s*কোড|security\s*code)\s*[:=-]?\s*({digit})', 'Security Code'),

        # Verification Code
        (rf'(?:ভেরিফিকেশন\s*কোড\s*\(verification\s*code\)|verification\s*code\s*\(ভেরিফিকেশন\s*কোড\)|ভেরিফিকেশন\s*কোড|verification\s*code)\s*[:=-]?\s*({digit})', 'Verification Code'),

        # Token number
        (rf'(?:টোকেন\s*\(token\)|token\s*\(টোকেন\)|টোকেন|token)\s*(?:নম্বর|number)?\s*[:=-]?\s*({digit})', 'Token'),

        # Password (digits only)
        (rf'(?:পাসওয়ার্ড\s*\(password\)|password\s*\(পাসওয়ার্ড\)|পাসওয়ার্ড|password)\s*[:=-]?\s*({digit})', 'Password'),
    ]
    return [(re.compile(p, re.IGNORECASE), name) for p, name in patterns]

_COMPILED_PATTERNS = build_patterns()

def extract_digit_patterns_with_spans(text: str):
    """
    Return a list of matches as dicts:
    {
        'type': <pattern name>,
        'digits': <matched digit-group text>,
        'span': (start, end),     # span of the digit group (group 1)
        'full_match_span': (s, e) # span of the whole match (optional, useful for debug)
    }
    """
    results = []
    for regex, name in _COMPILED_PATTERNS:
        for m in regex.finditer(text):
            g_start, g_end = m.span(1)  # span of the capturing group with the digits
            results.append({
                'type': name,
                'digits': m.group(1),
                'span': (g_start, g_end),
                'full_match_span': m.span(0),
            })
    return results

def security_code_normalizer(text: str):
    """
    Replace ONLY the digit-group (group 1) of every match with per-digit words.
    - Handles overlapping matches safely (right-to-left replacement).
    Returns:
        replaced_text, matches
    """
    matches = extract_digit_patterns_with_spans(text)

    # If multiple patterns match the same region, we still do deterministic replacement
    # by processing right-to-left to keep earlier spans valid.
    matches_sorted = sorted(matches, key=lambda x: x['span'][0], reverse=True)

    replaced_text = text
    for m in matches_sorted:
        s, e = m['span']
        original_digits = replaced_text[s:e]
        # Map the digits in the current slice; guard in case earlier replacements shifted content
        replacement = digits_to_words(original_digits)
        replaced_text = replaced_text[:s] + replacement + replaced_text[e:]
        # Update the match record with the replacement we actually used
        m['replacement'] = replacement

    return replaced_text, matches

# -----------------------------
# Example usage / quick test
# -----------------------------
if __name__ == "__main__":
    test_texts = [
        "ওটিপি (OTP): 123456",
        "কোড (code): 999888",
        "পিন (PIN): 4321",
        "সিভিভি (CVV): 123",
        "শেষ ৪ সংখ্যা  1234",
        "সংখ্যা 1234",
        "আপনার 123456",
        "আপনার ওটিপি (OTP): 123456 এবং পিন (PIN): 1234",
        "CVV (সিভিভি) ৯৮৭",  # Reverse format
        "ওটিপি 938221",       # Simple format
        "সিকিউরিটি code 938221",
        "পাসওয়ার্ড 123456",
        "ওটিপি 12345",
    ]

    for t in test_texts:
        new_t, found = security_code_normalizer(t)
        print(f"Original: {t}")
        print(f"Replaced: {new_t}")
        for f in found:
            print(f"  - {f['type']}: '{f['digits']}' at {f['span']} -> '{f.get('replacement')}'")
        print("-" * 60)
