import re
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class DrivingLicense:
    region: str
    first_part: str
    second_part: str
    span: Tuple[int, int]  # Add span position
    
    def __str__(self) -> str:
        return f"{self.region}-{self.first_part}-{self.second_part}"

class NumberNormalizer:
    BENGALI_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
    
    # Dictionary for number to word conversion (Bengali)
    BENGALI_NUMBERS = {
        '0': 'শূন্য', '1': 'এক', '2': 'দুই', '3': 'তিন', '4': 'চার',
        '5': 'পাঁচ', '6': 'ছয়', '7': 'সাত', '8': 'আট', '9': 'নয়',
        '০': 'শূন্য', '১': 'এক', '২': 'দুই', '৩': 'তিন', '৪': 'চার',
        '৫': 'পাঁচ', '৬': 'ছয়', '৭': 'সাত', '৮': 'আট', '৯': 'নয়'
    }
    
    @classmethod
    def to_bengali_digits(cls, text: str) -> str:
        print("to_bengali_digits text : ", text)
        trn_text = text.translate(cls.BENGALI_DIGITS)

        print("trn_text : ", trn_text)
        # check already have bangla digit
        # if any(char in text for char in '০১২৩৪৫৬৭৮৯'):
        #     return text
        return trn_text
    
    @classmethod
    def to_bengali_words(cls, number: str) -> str:
        return ' '.join(cls.BENGALI_NUMBERS.get(digit, digit) for digit in number)

class DrivingLicenseParser:
    REGION_CODES = {
        'DHA': 'ঢাকা', 'CTG': 'চট্টগ্রাম', 'KHU': 'খুলনা',
        'RAJ': 'রাজশাহী', 'BAR': 'বরিশাল', 'SYL': 'সিলেট',
        'RAN': 'রংপুর', 'MAY': 'ময়মনসিংহ', 'COM': 'কুমিল্লা'
    }
    
    PATTERN = r'''
        \b(?:DL[-_])?                      # Optional "DL-" or "DL_" prefix
        (?P<region>
            DHA|CHT|CTG|KHU|RAJ|BAR|SYL|RAN|MAY|SYN|MGM|COM  # English region codes
            |ঢাকা|চট্টগ্রাম|খুলনা|রাজশাহী|বরিশাল|সিলেট|রংপুর|ময়মনসিংহ|কুমিল্লা
        )
        [-_]?                              # Optional hyphen or underscore
        (?P<first>\d{5})[-_]              # First part (5 digits)
        (?P<second>\d{6})                  # Second part (6 digits)
        \b
    '''
    
    @classmethod
    def parse(cls, text: str) -> List[DrivingLicense]:
        licenses = []
        for match in re.finditer(cls.PATTERN, text, re.VERBOSE):
            region = match.group('region')
            # Convert English region code to Bengali if applicable
            region = cls.REGION_CODES.get(region, region)
            licenses.append(DrivingLicense(
                region=region,
                first_part=match.group('first'),
                second_part=match.group('second'),
                span=match.span()  # Add the span position
            ))
        return licenses

class DrivingLicenseFormatter:
    @staticmethod
    def format_license(license: DrivingLicense, format_type: str = 'bengali_digits') -> str:
        # if format_type == 'bengali_digits':
        #     # return NumberNormalizer.to_bengali_digits(str(license))
        # elif format_type == 'bengali_words':

        print("license 1st part: ", license.first_part)
        print("license 2nd part: ", license.second_part)
        return (f"{license.region}-"
                f"{NumberNormalizer.to_bengali_words(license.first_part)}-"
                f"{NumberNormalizer.to_bengali_words(license.second_part)}")
        # return str(license)

    def replace_in_text(text: str, licenses: List[DrivingLicense], format_type: str = 'bengali_digits') -> str:
        """Replace all license numbers in the text with their formatted versions."""
        # Sort licenses by span position in reverse order to avoid position shifts
        licenses = sorted(licenses, key=lambda x: x.span[0], reverse=True)
        result = text
        for license in licenses:
            start, end = license.span
            formatted = DrivingLicenseFormatter.format_license(license, format_type)
            result = result[:start] + formatted + result[end:]
        return result

if __name__ == "__main__":
    # Sample text
    texts = """
    তার ড্রাইভিং লাইসেন্স নম্বর ঢাকা-12345-678901।
    DHA-54321-123456 আমার লাইসেন্স নম্বর।
    CTG-12345-678901 অনুমোদিত হয়েছে।
    তার ড্রাইভিং লাইসেন্স নম্বর ঢাকা-১২৩৪৫-৬৭৮৯০১।
    আমার নতুন ড্রাইভিং লাইসেন্স নম্বর রাজশাহী-৫৪৩২১-১২৩৪৫৬।
    DL-চট্টগ্রাম-৯৮৭৬৫-৪৩২১০৯ নম্বর দিয়ে যাচাই করা হয়েছে।
    আপনার লাইসেন্স নম্বর খুলনা-১১২২৩-৪৪৫৫৬৬।
    ময়মনসিংহ-৭৭৭৭৭-৮৮৮৮৮৮ লাইসেন্স নম্বরটি যাচাই করা হয়েছে।
    BAR-99999-000000 এর জন্য আবেদন গৃহীত হয়েছে।
    তার ড্রাইভিং লাইসেন্স নম্বর ঢাকা-১২৩৪৫-৬৭৮৯০১।
    আমার নতুন ড্রাইভিং লাইসেন্স নম্বর রাজশাহী-৫৪৩২১-১২৩৪৫৬।
    DL-চট্টগ্রাম-৯৮৭৬৫-৪৩২১০৯ নম্বর দিয়ে যাচাই করা হয়েছে।
    আপনার লাইসেন্স নম্বর খুলনা-১১২২৩-৪৪৫৫৬৬।
    ময়মনসিংহ-৭৭৭৭৭-৮৮৮৮৮৮ লাইসেন্স নম্বরটি যাচাই করা হয়েছে।
    BAR-99999-000000 এর জন্য আবেদন গৃহীত হয়েছে।
    DHA-54321-123456 আমার লাইসেন্স নম্বর।
    CTG-12345-678901 অনুমোদিত হয়েছে।
    KHU12345-678901 যাচাই করা হয়েছে।
    DL-RAJ-67890-123456
    DL_SYL-11223-334455
    SYN98765-432109
    RAN-98765-432100
    """

    parser = DrivingLicenseParser()
    # Parse licenses
    for text in texts.split("\n"):
        if text.strip():
            print("text : ", text)
            licenses = parser.parse(text)
            print("Extracted licenses : ", licenses)
            for license in licenses:
                print(f"\nPosition {license.span}:")
                print("extracted Original:", str(license))
                # normalized_license = parser.format_license(license, 'bengali_words')
                # print("normalized_license: ", normalized_license, license)
                text = DrivingLicenseFormatter.replace_in_text(text, [license], 'bengali_words')
            # print("normalized_license: ", normalized_license)
            print("replaced_text: ", text)
            print("--------------------------------")   
