import re
from typing import Dict

class OrdinalConverter:
    def __init__(self):
        # English ordinals mapping (1-31 most common)
        self.english_ordinals = {
            '1': 'first', '2': 'second', '3': 'third', '4': 'fourth', '5': 'fifth',
            '6': 'sixth', '7': 'seventh', '8': 'eighth', '9': 'ninth', '10': 'tenth',
            '11': 'eleventh', '12': 'twelfth', '13': 'thirteenth', '14': 'fourteenth',
            '15': 'fifteenth', '16': 'sixteenth', '17': 'seventeenth', '18': 'eighteenth',
            '19': 'nineteenth', '20': 'twentieth', '21': 'twenty-first', '22': 'twenty-second',
            '23': 'twenty-third', '24': 'twenty-fourth', '25': 'twenty-fifth',
            '26': 'twenty-sixth', '27': 'twenty-seventh', '28': 'twenty-eighth',
            '29': 'twenty-ninth', '30': 'thirtieth', '31': 'thirty-first'
        }
        
        # Bengali ordinals mapping
        self.bengali_ordinals = {
            '1': 'প্রথম', '2': 'দ্বিতীয়', '3': 'তৃতীয়', '4': 'চতুর্থ', '5': 'পঞ্চম',
            '6': 'ষষ্ঠ', '7': 'সপ্তম', '8': 'অষ্টম', '9': 'নবম', '10': 'দশম',
            '11': 'একাদশ', '12': 'দ্বাদশ', '13': 'ত্রয়োদশ', '14': 'চতুর্দশ',
            '15': 'পঞ্চদশ', '16': 'ষোড়শ', '17': 'সপ্তদশ', '18': 'অষ্টাদশ',
            '19': 'ঊনবিংশ', '20': 'বিংশ', '21': 'একবিংশ', '22': 'দ্বাবিংশ',
            '23': 'ত্রয়োবিংশ', '24': 'চতুর্বিংশ', '25': 'পঞ্চবিংশ',
            '26': 'ষড়বিংশ', '27': 'সপ্তবিংশ', '28': 'অষ্টাবিংশ',
            '29': 'ঊনত্রিংশ', '30': 'ত্রিংশ', '31': 'একত্রিংশ'
        }
        
        # Pattern to match ordinal numbers
        self.ordinal_pattern = re.compile(r'\b(\d+)(st|nd|rd|th)\b', re.IGNORECASE)
        
    def convert_ordinals(self, text: str, lang: str = "en") -> str:
        """Convert ordinal numbers in text to their word form."""
        
        # Find all ordinal matches
        matches = list(self.ordinal_pattern.finditer(text))
        
        # Process in reverse order to maintain correct positions
        for match in reversed(matches):
            number = match.group(1)
            start, end = match.span()
            
            # Get the word form
            if lang == "bn":
                word = self.get_bengali_ordinal(number)
            else:
                word = self.get_english_ordinal(number)
            
            # Replace in text
            text = text[:start] + word + text[end:]
        
        return text
    
    def get_english_ordinal(self, number: str) -> str:
        """Get English word form of ordinal number."""
        
        # Check if in predefined mapping
        if number in self.english_ordinals:
            return self.english_ordinals[number]
        
        # Handle larger numbers
        num = int(number)
        
        # Handle 32-99
        if 32 <= num <= 99:
            tens = num // 10
            ones = num % 10
            
            tens_words = {
                3: 'thirty', 4: 'forty', 5: 'fifty',
                6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'
            }
            
            if ones == 0:
                # 40th -> fortieth
                return tens_words[tens].rstrip('y') + 'ieth'
            else:
                # 42nd -> forty-second
                ones_ordinals = ['', 'first', 'second', 'third', 'fourth', 
                               'fifth', 'sixth', 'seventh', 'eighth', 'ninth']
                return f"{tens_words[tens]}-{ones_ordinals[ones]}"
        
        # Handle 100-999
        elif 100 <= num <= 999:
            hundreds = num // 100
            remainder = num % 100
            
            hundreds_words = ['', 'one hundred', 'two hundred', 'three hundred',
                            'four hundred', 'five hundred', 'six hundred',
                            'seven hundred', 'eight hundred', 'nine hundred']
            
            if remainder == 0:
                # 100th -> one hundredth
                return hundreds_words[hundreds] + 'th'
            elif str(remainder) in self.english_ordinals:
                # 113th -> one hundred thirteenth
                return f"{hundreds_words[hundreds]} {self.english_ordinals[str(remainder)]}"
            else:
                # 142nd -> one hundred forty-second
                return f"{hundreds_words[hundreds]} {self.get_english_ordinal(str(remainder))}"
        
        # Fallback for very large numbers
        return f"{number}th"
    
    def get_bengali_ordinal(self, number: str) -> str:
        """Get Bengali word form of ordinal number."""
        
        # Check if in predefined mapping
        if number in self.bengali_ordinals:
            return self.bengali_ordinals[number]
        
        # For numbers > 31, add তম suffix
        num = int(number)
        
        if 32 <= num <= 99:
            # Simple approach: number + তম
            return f"{number}তম"
        
        # Fallback
        return f"{number}তম"


# Example usage
if __name__ == "__main__":
    converter = OrdinalConverter()
    
    # Test sentences
    test_sentences = [
        "MSI Thin 15 B13VE Core i5 13th Gen RTX 4050 6GB Graphics",
        "This is the 1st time I'm using this laptop",
        "He finished in 2nd place",
        "The 3rd option is the best",
        "Today is the 21st of December",
        "It's the 42nd anniversary",
        "The 100th customer wins a prize",
        "She came in 123rd position"
    ]
    
    print("ORDINAL NUMBER CONVERSION")
    print("=" * 60)
    
    for sentence in test_sentences:
        print(f"\nOriginal: {sentence}")
        
        # English conversion
        english = converter.convert_ordinals(sentence, lang="en")
        print(f"English:  {english}")
        
        # Bengali conversion but it not use into bangla sentence
        bengali = converter.convert_ordinals(sentence, lang="bn")
        print(f"Bengali:  {bengali}")
        
        print("-" * 60)