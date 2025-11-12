from dataclasses import dataclass
from typing import List, Tuple, Optional
import re

mapping = {
    "০": "শূন্য",
    "১": "এক",
    "২": "দুই",
    "৩": "তিন",
    "৪": "চার",
    "৫": "পাঁচ",
    "৬": "ছয়",
    "৭": "সাত",
    "৮": "আট",
    "৯": "নয়",
    '0': 'জিরো', '1': 'ওয়ান', '2': 'টু', '3': 'থ্রি', '4': 'ফোর', 
    '5': 'ফাইভ', '6': 'সিক্স', '7': 'সেভেন', '8': 'এইট', '9': 'নাইন',
}

@dataclass
class NIDMatch:
    """Class to represent a matched NID number with its position in text"""
    value: str
    start: int
    end: int
    bengali_value: str

    def __str__(self) -> str:
        return f"NID(value='{self.value}', span=({self.start}, {self.end}), bengali='{self.bengali_value}')"


@dataclass
class NIDNumber:
    """Class to represent and validate Bangladesh National ID numbers"""
    value: str
    
    # Class constants
    BENGALI_DIGITS = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
    BENGALI_TO_ENGLISH = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
    
    # Updated pattern to match both Bengali and English digits
    # NID_PATTERNS = [
    #     r'\b(?:NID|NID নম্বর|জাতীয় পরিচয়পত্র নং|জাতীয় পরিচয়পত্র নম্বর|জাতীয় পরিচয়পত্র|পরিচয়পত্র|'
    #     r'জাতীয় পরিচয় নম্বর|NID Number|NID নং|এনআইডি|এনআইডি নম্বর|এনআইডি Number|এনআইডি নং)\s*[:ঃ]?\s*([০-৯\d]{10,17})\b'
    # ]

    NID_PATTERNS = [
        r'(?:NID|NID নম্বর|জাতীয় পরিচয়পত্র নং|জাতীয় পরিচয়পত্র নম্বর|জাতীয় পরিচয়পত্র|পরিচয়পত্র|লাইসেন্স|ড্রাইভিং লাইসেন্স'
        r'জাতীয় পরিচয় নম্বর|NID Number|NID নং|এনআইডি|এনআইডি নম্বর|এনআইডি Number|এনআইডি নং)\s*[:ঃ]?\s*([০-৯0-9]+(?:\s+[০-৯0-9]+)*)'
    ]

    def __post_init__(self) -> None:
        """Validate the NID number format after initialization"""
        # if not self._is_valid_format():
        #     raise ValueError("Invalid NID number format")

    # def _is_valid_format(self) -> bool:
    #     """Check if the NID number has valid format"""
    #     # Convert Bengali digits to English first if needed
    #     english_value = self.value.translate(self.BENGALI_TO_ENGLISH)
    #     return len(english_value) >= 10 and len(english_value) <= 17 and english_value.isdigit()

    def to_bengali(self) -> str:
        """Convert the NID number to Bengali digits"""
        # First ensure we have English digits

        english_value = self.value.translate(self.BENGALI_TO_ENGLISH)
        # return english_value.translate(self.BENGALI_DIGITS)
        return english_value

    @classmethod
    def from_bengali(cls, bengali_number: str) -> 'NIDNumber':
        """Create NIDNumber from Bengali digits"""
        english_number = bengali_number.translate(cls.BENGALI_TO_ENGLISH)
        return cls(english_number)


class NIDNormalizer:
    """Class to normalize NID numbers in text"""
    
    def __init__(self) -> None:
        self.nid_pattern = re.compile('|'.join(NIDNumber.NID_PATTERNS))

    def extract_nids(self, text: str) -> List[NIDMatch]:
        """Extract all NID numbers with their positions from text"""
        matches = []
        for match in self.nid_pattern.finditer(text):
            # try:
            nid_number = NIDNumber(match.group(1))
            # print("nid_number", nid_number)
            # Get the span of the actual number, not the whole match
            number_start = match.start(1)
            number_end = match.end(1)

            if nid_number.value.isdigit():
                bengali_value =  nid_number.value
            else:
                bengali_value= nid_number.to_bengali()
            bengali_value = ' '.join(mapping.get(char, char) for char in bengali_value)
            # print("bengali_value", bengali_value)
            matches.append(NIDMatch(
                value=nid_number.value,
                start=number_start,
                end=number_end,
                bengali_value=bengali_value
            ))
            # except ValueError:
            #     # Skip invalid NID numbers
            #     continue
        return matches

    def normalize(self, text: str) -> str:
        """Normalize NID numbers in the given text to Bengali digits"""
        result = text
        # print("result----> ", result)
        # Process matches in reverse order to avoid position shifts
        for match in reversed(self.extract_nids(text)):
            # print("match----> ", match)

            # print("match.bengali_value : ", match.bengali_value)
            result = result[:match.start] + match.bengali_value.replace(" ", ", ") +", "+result[match.end:]
        return result
    
def main() -> None:
    """Example usage of the NID classes"""
    sample_texts = [
        "তার NID নম্বর 1234567890123।",
        "জাতীয় পরিচয়পত্র নং: 987654321098।",
        "আপনার এনআইডি ৩২১০৯৮৭৬৫৪৩২।",
        "NID নং: 110022334455",
        "জাতীয় পরিচয়পত্র নম্বর: 76543210987",
        "আপনার NID: ৭৬৫৪৩২১০৯৮৭ যাচাই করুন।",
        "NID Number: 1234567890",
        "জাতীয় পরিচয় নম্বরঃ 0987654321 জাতীয় পরিচয় নম্বরঃ 0987654321",
        "এনআইডি নম্বরঃ 1234567890",
        "এনআইডি নম্বরঃ ১২৩৪৫৬৭৮৯০ hello 12345"
        "জাতীয় পরিচয়পত্র ৪৫৬৭"
    ]

    normalizer = NIDNormalizer()
    
    for text in sample_texts:
        print(f"\nOriginal: {text}")
        # Extract and print NID matches with positions
        # matches = normalizer.extract_nids(text)
        normalized = normalizer.normalize(text)
        print(f"Normalized: {normalized}")


if __name__ == "__main__":
    main()
