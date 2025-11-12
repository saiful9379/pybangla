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
    # BENGALI_DIGITS = str.maketrans("0123456789|০১২৩৪৫৬৭৮৯")
    
    # Dictionary for number to word conversion (Bengali)
    BENGALI_NUMBERS = {
        '0': 'জিরো', '1': 'ওয়ান', '2': 'টু', '3': 'থ্রি', '4': 'ফোর', 
        '5': 'ফাইভ', '6': 'সিক্স', '7': 'সেভেন', '8': 'এইট', '9': 'নাইন',
        '০': 'শূন্য', '১': 'এক', '২': 'দুই', '৩': 'তিন', '৪': 'চার',
        '৫': 'পাঁচ', '৬': 'ছয়', '৭': 'সাত', '৮': 'আট', '৯': 'নয়'
    }
    
    @classmethod
    def to_bengali_digits(cls, text: str) -> str:
        # print("to_bengali_digits text : ", text)
        trn_text = text.translate(cls.BENGALI_DIGITS)

        # print("trn_text : ", trn_text)
        # check already have bangla digit
        # if any(char in text for char in '০১২৩৪৫৬৭৮৯'):
        #     return text
        return trn_text
    
    @classmethod
    def to_bengali_words(cls, number: str) -> str:
        return ', '.join(cls.BENGALI_NUMBERS.get(digit, digit) for digit in number)

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
            |ফেনী|ব্রাহ্মণবাড়িয়া|রাঙ্গামাটি|নোয়াখালী|চাঁদপুর|লক্ষ্মীপুর|কক্সবাজার
            |খাগড়াছড়ি|বান্দরবান|সিরাজগঞ্জ|পাবনা|বগুড়া|নাটোর|জয়পুরহাট|চাঁপাইনবাবগঞ্জ 
            |নওগাঁ|যশোর|সাতক্ষীরা|মেহেরপুর|নড়াইল|চুয়াডাঙ্গা|কুষ্টিয়া|মাগুরা|বাগেরহাট
            |ঝিনাইদহ|ঝালকাঠি|পটুয়াখালী|পিরোজপুর|ভোলা|বরগুনা|মৌলভীবাজার
            |হবিগঞ্জ|সুনামগঞ্জ|নরসিংদী|গাজীপুর|শরীয়তপুর|নারায়ণগঞ্জ|টাঙ্গাইল|কিশোরগঞ্জ|মানিকগঞ্জ
            |মুন্সিগঞ্জ|রাজবাড়ী|মাদারীপুর|গোপালগঞ্জ|ফরিদপুর|পঞ্চগড়|দিনাজপুর|লালমনিরহাট
            |নীলফামারী|গাইবান্ধা|ঠাকুরগাঁও|কুড়িগ্রাম|শেরপুর|ময়মনসিংহ|জামালপুর|নেত্রকোণা
        )
        [-_]?                              # Optional hyphen or underscore
        (?P<first>\d+)[-_]                # First part (flexible digits) ?P<first>\d{5})[-_]              # First part (5 digits)
        (?P<second>\d+)                   # Second part (flexible digits)
        \b
    '''
    
    @classmethod
    def parse(cls, text: str) -> List[DrivingLicense]:
        licenses = []
        for match in re.finditer(cls.PATTERN, text, re.VERBOSE):
            # print("match : ", match.group(), match.span())
            dl_found  = False
            if "DL" in match.group().strip()[:2] or "dl" in match.group().strip()[:2]:
                dl_found = True
            region = match.group('region')
            # Convert English region code to Bengali if applicable
            region = cls.REGION_CODES.get(region, region)
            if dl_found:
                # print("REGION_CODES region : ", region)
                region = "DL-" + region

            licenses.append(DrivingLicense(
                region=region,
                first_part=match.group('first'),
                second_part=match.group('second'),
                span=match.span()  # Add the span position
            ))
        # print("licenses return : ", licenses)
        return licenses

class DrivingLicenseFormatter:
    def __init__(self):
        pass
    def format_license(self, license, format_type: str = 'bengali_digits') -> str:
        # Handle both string input and DrivingLicense object
        if isinstance(license, str):
            # Parse the string to extract license information
            parsed_licenses = DrivingLicenseParser.parse(license)
            if parsed_licenses:
                license_obj = parsed_licenses[0]
                return (f"{license_obj.region}-"
                        f"{NumberNormalizer.to_bengali_words(license_obj.first_part)}-"
                        f"-{NumberNormalizer.to_bengali_words(license_obj.second_part)}")
            else:
                return license  # Return original if no license found
        elif isinstance(license, DrivingLicense):
            return (f"{license.region}-"
                    f"{NumberNormalizer.to_bengali_words(license.first_part)}-"
                    f"{NumberNormalizer.to_bengali_words(license.second_part)}")
        else:
            return str(license)  # Fallback

    def replace_in_text(self, text: str, format_type: str = 'bengali_digits') -> str:
        """Replace all license numbers in the text with their formatted versions."""
        # Sort licenses by span position in reverse order to avoid position shifts
        # print("text in driver : ", text)
        licenses = DrivingLicenseParser.parse(text)
        # print("licenses : ", licenses)
        licenses = sorted(licenses, key=lambda x: x.span[0], reverse=True)
        # print("licenses : ", licenses)
        result = text
        for license in licenses:
            start, end = license.span
            formatted = self.format_license(license, format_type)

            # print("license : ", license, formatted)

            # print("formatted : ", formatted)
            result = result[:start] + formatted + result[end:]
        return result

if __name__ == "__main__":

    # তার ড্রাইভিং লাইসেন্স নম্বর ঢাকা-12345-678901।
    # DHA-54321-123456 আমার লাইসেন্স নম্বর।
    # CTG-12345-678901 অনুমোদিত হয়েছে।
    # তার ড্রাইভিং লাইসেন্স নম্বর ঢাকা-১২৩৪৫-৬৭৮৯০১।
    # আমার নতুন ড্রাইভিং লাইসেন্স নম্বর রাজশাহী-৫৪৩২১-১২৩৪৫৬।
    # DL-চট্টগ্রাম-৯৮৭৬৫-৪৩২১০৯ নম্বর দিয়ে যাচাই করা হয়েছে।
    # আপনার লাইসেন্স নম্বর খুলনা-১১২২৩-৪৪৫৫৬৬।
    # ময়মনসিংহ-৭৭৭৭৭-৮৮৮৮৮৮ লাইসেন্স নম্বরটি যাচাই করা হয়েছে।
    # BAR-99999-000000 এর জন্য আবেদন গৃহীত হয়েছে।
    # তার ড্রাইভিং লাইসেন্স নম্বর ঢাকা-১২৩৪৫-৬৭৮৯০১।
    # আমার নতুন ড্রাইভিং লাইসেন্স নম্বর রাজশাহী-৫৪৩২১-১২৩৪৫৬।
    # DL-চট্টগ্রাম-৯৮৭৬৫-৪৩২১০৯ নম্বর দিয়ে যাচাই করা হয়েছে।
    # আপনার লাইসেন্স নম্বর খুলনা-১১২২৩-৪৪৫৫৬৬।
    # ময়মনসিংহ-৭৭৭৭৭-৮৮৮৮৮৮ লাইসেন্স নম্বরটি যাচাই করা হয়েছে।
    # BAR-99999-000000 এর জন্য আবেদন গৃহীত হয়েছে।
    # DHA-54321-123456 আমার লাইসেন্স নম্বর।
    # CTG-12345-678901 অনুমোদিত হয়েছে।
    # KHU12345-678901 যাচাই করা হয়েছে।
    # DL-RAJ-67890-123456
    # DL_SYL-11223-334455
    # SYN98765-432109
    # RAN-98765-432100,
    # তার ড্রাইভিং লাইসেন্স নম্বর ঢাকা-12-6789।
    # Sample text
    texts = """
    তার ড্রাইভিং লাইসেন্স 6789।
    """

    dlf = DrivingLicenseFormatter()
    # Parse licenses
    for text in texts.split("\n"):
        if text.strip():
            print("text : ", text)
            # normalized_license = parser.format_license(license, 'bengali_words')
             # print("normalized_license: ", normalized_license, license)
            text = dlf.replace_in_text(text)
            # print("normalized_license: ", normalized_license)
            print("replaced_text: ", text)
            print("--------------------------------")   
