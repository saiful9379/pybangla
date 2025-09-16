from typing import List, Tuple
import re
from dataclasses import dataclass

try:
    from .config import Config as cfg
except ImportError:
    from config import Config as cfg

@dataclass
class PassportNumber:
    prefix: str  # Letter prefix (if any)
    number: str  # Numeric part
    span: Tuple[int, int]  # Position in text
    
    def __str__(self) -> str:
        return f"{self.prefix}{self.number}"

class NumberNormalizer:
    BENGALI_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
    # Fixed mapping with equal length strings
    ENGLISH_TO_BENGALI_LETTERS = {
        'A': 'এ', 'B': 'বি', 'C': 'সি', 'D': 'ডি', 'E': 'ই',
        'F': 'এফ', 'G': 'জি', 'H': 'এইচ', 'I': 'আই', 'J': 'জে',
        'K': 'কে', 'L': 'এল', 'M': 'এম', 'N': 'এন', 'O': 'ও',
        'P': 'পি', 'Q': 'কিউ', 'R': 'আর', 'S': 'এস', 'T': 'টি',
        'U': 'ইউ', 'V': 'ভি', 'W': 'ডব্লিউ', 'X': 'এক্স', 'Y': 'ওয়াই',
        'Z': 'জেড'
    }
    
    # Dictionary for number to word conversion (Bengali)
    BENGALI_NUMBERS = {
        '0': 'জিরো', '1': 'ওয়ান', '2': 'টু', '3': 'থ্রি', '4': 'ফোর', 
        '5': 'ফাইভ', '6': 'সিক্স', '7': 'সেভেন', '8': 'এইট', '9': 'নাইন',
        '০': 'শূন্য', '১': 'এক', '২': 'দুই', '৩': 'তিন', '৪': 'চার',
        '৫': 'পাঁচ', '৬': 'ছয়', '৭': 'সাত', '৮': 'আট', '৯': 'নয়'
    }
    
    @classmethod
    def to_bengali_digits(cls, text: str) -> str:
        return text.translate(cls.BENGALI_DIGITS)
    
    @classmethod
    def to_bengali_letters(cls, text: str) -> str:
        if not text:
            return ""
        return ''.join(cls.ENGLISH_TO_BENGALI_LETTERS.get(c, c) for c in text.upper())
    
    @classmethod
    def to_bengali_words(cls, number: str) -> str:
        return ' '.join(cls.BENGALI_NUMBERS.get(digit, digit) for digit in number)
#  self.passport_pattern = r'(?i)(?:e-passport|ই-পাসপোর্ট|e\s+passport|ই\s+পাসপোর্ট|passport|পাসপোর্ট)\s*(?:id|আইডি|নম্বর|নাম্বার|নং|number|no)?\s*[:=\-]?\s*([A-Za-z\u0985-\u09B9]?[\s\-]?[\u09E6-\u09EF0-9]+)'
class PassportParser:
    # Pattern to match Bangladesh Passport Numbers with optional prefix, Bengali/English digits, and separators
    # PATTERN = r'''
    #     (?:                                                    # Required group (no ? at the end)
    #         (e-passport|ই-পাসপোর্ট|e\s+passport|ই\s+পাসপোর্ট|passport|পাসপোর্ট)  # Required passport prefix
    #         \s*
    #         (?:id|আইডি|নম্বর|নাম্বার|নং|number|no)?           # Optional ID/number label
    #         \s*:?\s*
    #     )
    #     (?P<prefix>[A-Zএ-ঔ])?                                 # Optional letter prefix
    #     [\s\-\.]?
    #     (?P<number>[০-৯0-9]{7,9})                             # 7-9 digits
    # '''

    PATTERN = r'''
        (?i)                                                # Case insensitive
        (?:                                                 # Start non-capturing group
            e-passport|ই-পাসপোর্ট|e\s+passport|ই\s+পাসপোর্ট|passport|পাসপোর্ট
        )                                                   # End passport keywords
        \s*                                                 # Optional whitespace
        (?:id|আইডি|নম্বর|নাম্বার|নং|number|no)?           # Optional ID/number label
        \s*[:=\-]?\s*                                      # Optional separator with whitespace
        (?P<prefix>[A-Za-z\u0985-\u09B9])?                 # Optional letter prefix (named group)
        [\s\-]?                                            # Optional space or hyphen
        (?P<number>[\u09E6-\u09EF0-9]{7,9})               # 7-9 digits (named group)
    '''
    
    @classmethod
    def parse(cls, text: str) -> List[PassportNumber]:
        passports = []
        for match in re.finditer(cls.PATTERN, text, re.VERBOSE):
            prefix = match.group('prefix') or ''
            passports.append(PassportNumber(
                prefix=prefix,
                number=match.group('number'),
                span=match.span()
            ))

        # print("Parsed Passports:", passports)
        return passports

class PassportFormatter:
    @staticmethod
    def format_passport(passport: PassportNumber, format_type: str = 'bengali_digits') -> str:
        if format_type == 'bengali_digits':
            prefix = NumberNormalizer.to_bengali_letters(passport.prefix) if passport.prefix else ''
            return f"{prefix}{NumberNormalizer.to_bengali_digits(passport.number)}"
        elif format_type == 'bengali_words':
            prefix_text = f"{NumberNormalizer.to_bengali_letters(passport.prefix)} " if passport.prefix else ''
            return f"{prefix_text}{NumberNormalizer.to_bengali_words(passport.number)}"
        return str(passport)

    @staticmethod
    def normalize(text: str, format_type: str = 'bengali_words') -> str:
        """Replace all passport numbers in the text with their formatted versions."""
        # Sort passports by span position in reverse order to avoid position shifts
        # print("input text for passport number----> ", text)
        passports = PassportParser.parse(text)
        # print("passports parsed----> ", passports)
        passports = sorted(passports, key=lambda x: x.span[0], reverse=True)
        # passports = sorted(passports, key=lambda x: x.span[0], reverse=True)
        result = text
        for passport in passports:
            start, end = passport.span
            span_text = text[start:end]
            # print("span text----> ", span_text)
            # print("passport----> ", passport)
            formatted = PassportFormatter.format_passport(passport, format_type)
            # print("formatted----> ", formatted)
            span_text = span_text.replace(passport.prefix+passport.number, formatted.replace(" ", ", "))
            # print("span text after replace----> ", span_text)
            result = result[:start] + " " + span_text + ", " + result[end:]
        # print("result----> ", result)
                        # print("text : ", text)
        result = re.sub(cfg._whitespace_re, " ", result)
    
        result = re.sub(r"\s*,\s*", ", ", result)
        return result

if __name__ == "__main__":
    # Sample text
    texts = """
    আমার পাসপোর্ট নম্বর A01234567 এবং তার পাসপোর্ট নম্বর 987654321।
    নতুন ই-পাসপোর্ট নম্বর E12345678 ইস্যু করা হয়েছে।
    তিনি পুরাতন পাসপোর্ট নম্বর 1234567 ব্যবহার করেছেন।
    মেশিন রিডেবল পাসপোর্ট নম্বর B76543210।
    তার পাসপোর্ট নম্বর P87654321 ছিল।
    তার পাসপোর্ট নম্বর P০১২৩৪৫৬৭ ছিল।
    বাংলা নম্বর হিসেবে পাসপোর্ট নম্বর এ০১২৩৪৫৬৭ ও ই১২৩৪৫৬৭৮।
    পাসপোর্ট নম্বর এ০১২৩৪৫৬৭ ও এ১২৩৪৫৬৭৮।       
    """
    
    # Parse passport numbers
    for text in texts.split("\n"):
        if text.strip() == "":
            continue
        print("input text----> ", text)
        normalized_text =  PassportFormatter.normalize(text, 'bengali_words')
        # print("\nNormalized Text:", PassportFormatter.normalize(text, 'bengali_words'))
        print("\nNormalized Text:", normalized_text)
        print("-----------------------------")
            # text = PassportFormatter.replace_in_text(text, passport, 'bengali_words')
        # print(PassportFormatter.replace_in_text(text, passports, 'bengali_words'))


