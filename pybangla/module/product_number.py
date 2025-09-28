import re
from typing import List, Dict, Tuple, Optional


class DigitConverter:
    """Class to handle digit to word conversions"""
    
    def __init__(self):
        self.digit_words = {
            '0': 'জিরো', '1': 'ওয়ান', '2': 'টু', '3': 'থ্রি', '4': 'ফোর',
            '5': 'ফাইভ', '6': 'সিক্স', '7': 'সেভেন', '8': 'এইট', '9': 'নাইন',
            # Bengali numerals
            '০': 'জিরো', '১': 'ওয়ান', '২': 'টু', '৩': 'থ্রি', '৪': 'ফোর',
            '৫': 'ফাইভ', '৬': 'সিক্স', '৭': 'সেভেন', '৮': 'এইট', '৯': 'নাইন'
        }
    
    def number_to_words(self, num_str: str) -> str:
        """Convert a number string to words (digit by digit)"""
        words = []
        for char in num_str:
            if char in self.digit_words:
                words.append(self.digit_words[char])
            else:
                words.append(char)
        
        return ' '.join(words)


class CodeExtractor:
    """Class to handle extraction of alphanumeric codes"""
    
    def __init__(self):
        self.pattern = r'\b[A-Z0-9]+(?:-[A-Z0-9]+)+\b'
    
    def extract_alphanumeric_with_hyphen(self, text: str) -> List[str]:
        """Extract alphanumeric codes containing hyphens from text"""
        matches = re.findall(self.pattern, text, re.IGNORECASE)
        
        filtered_matches = []
        for match in matches:
            has_letter = any(c.isalpha() for c in match)
            has_digit = any(c.isdigit() for c in match)
            if has_letter and has_digit:
                filtered_matches.append(match)
        
        return filtered_matches
    
    def extract_with_spans(self, text: str) -> List[Dict]:
        """Extract alphanumeric codes with their positions in the text"""
        matches = []
        
        for match in re.finditer(self.pattern, text, re.IGNORECASE):
            matched_text = match.group()
            has_letter = any(c.isalpha() for c in matched_text)
            has_digit = any(c.isdigit() for c in matched_text)
            
            if has_letter and has_digit:
                matches.append({
                    'text': matched_text,
                    'start': match.start(),
                    'end': match.end(),
                    'span': (match.start(), match.end())
                })
        
        return matches


class CodeConverter:
    """Class to handle conversion of codes to text format"""
    
    def __init__(self):
        self.digit_converter = DigitConverter()
    
    def convert_code_to_text(self, code: str) -> str:
        """Convert alphanumeric code with hyphens to text format"""
        parts = code.split('-')
        converted_parts = []
        
        for part in parts:
            # Separate letters and numbers
            segments = re.findall(r'[A-Za-z]+|\d+', part)
            converted_segments = []
            
            for segment in segments:
                if segment.isdigit():
                    # Convert numbers to words
                    converted_segments.append(self.digit_converter.number_to_words(segment))
                else:
                    # Keep letters as is
                    converted_segments.append(segment)
            
            # Join segments with space
            converted_parts.append(' '.join(converted_segments))
        
        # Join parts with hyphen
        return ' - '.join(converted_parts)


class ProductNormalizer:
    """Main class for product number normalization"""
    
    def __init__(self, debug: bool = False):
        self.extractor = CodeExtractor()
        self.converter = CodeConverter()
        self.debug = debug
    
    def replace_codes_with_text(self, original_text: str) -> Tuple[str, List[Dict]]:
        """Replace alphanumeric codes with their textual representation"""
        # Get matches with spans
        matches = self.extractor.extract_with_spans(original_text)
        
        # Sort matches by position (reverse order for replacement)
        matches.sort(key=lambda x: x['start'], reverse=True)
        
        modified_text = original_text
        replacements = []
        
        for match in matches:
            code = match['text']
            converted = self.converter.convert_code_to_text(code)
            
            # Replace in the text
            modified_text = (modified_text[:match['start']] + 
                            converted + 
                            modified_text[match['end']:])
            
            replacements.append({
                'original': code,
                'converted': converted,
                'span': match['span']
            })
        
        return modified_text, replacements
    
    def normalize(self, text: str) -> str:
        """Normalize product text by converting alphanumeric codes to text"""
        # Extract codes with spans
        matches_with_spans = self.extractor.extract_with_spans(text)
        
        if matches_with_spans:
            text, replacements = self.replace_codes_with_text(text)
            # if self.debug:
            print("modified_text : ", text, replacements)
        
        return text
    
    def get_extracted_codes(self, text: str) -> List[str]:
        """Get list of extracted alphanumeric codes from text"""
        return self.extractor.extract_alphanumeric_with_hyphen(text)
    
    def get_codes_with_spans(self, text: str) -> List[Dict]:
        """Get extracted codes with their position information"""
        return self.extractor.extract_with_spans(text)


    def product_normalization(self, text: str) -> str:
        """Legacy function for backward compatibility"""
        normalizer = ProductNormalizer(debug=True)
        return normalizer.normalize(text)

if __name__ == "__main__":
    # Test with examples
    test_strings = [
        # "Orico 2520U3-BK-EP 2.5 inch USB 3.0 Hard Drive Enclosure",
        # "Orico 123C 2.5 inch USB 3.0 Hard Drive Enclosure 2520U3-BK-EP-346-67895",
        # "Havit HV-SC055 Laptop Cleaning Kit - HV-SC055 and the number is the 12345",
        # "তার ড্রাইভিং লাইসেন্স নম্বর ঢাকা-12-6789।",
        # "তার পাসপোর্ট নম্বর P87654321 ছিল।, 1995-1969 and phone number 01773-550379",
        # "01790540211124562 যোগাযোগ করতে হলে01790-540211অথবা 01790-541111 নম্বরে যোগাযোগ করতে হবে",
        # "Awei T71 TWS Earbuds V Bluetooth 5.3 Earphones With Mic",
        # "HTC AT-522 Rechargeable Cordless Trimmer For Men",
        # "Gigabyte A16 GA6H Core i7 13th Gen 16 FHD+ WUXGA Nvidia RTX 5050 Gaming Laptop",
        # "Starlink Standard কিটের জন্য BDT49,500। নির্ভরযোগ্য হাই-স্পিড ইন্টারনেট, যেখানেই যাবেন সেখানেই পাবেন। প্ল্যানের মূল্য শুরু প্রতি মাসে 4,200৳ থেকে।"

        "Use reference number REF-123-456-789 for all correspondence."
    ]

    print("Processing alphanumeric codes with hyphens (OOP Version):\n")
    print("=" * 80)

    # Create normalizer instance with debug enabled
    normalizer = ProductNormalizer(debug=False)
    for i, text in enumerate(test_strings):
        print(f"\n{i+1}. Original Text: {text}")
    
        # # Extract codes first to show what was found
        # extracted_codes = normalizer.get_extracted_codes(text)
        # if extracted_codes:
        #     print(f"   Found codes: {extracted_codes}")
        
        # # Normalize the text
        modified_text = normalizer.product_normalization(text)
        
        print(f"   Final Text: {modified_text}")
        print("-" * 60)

