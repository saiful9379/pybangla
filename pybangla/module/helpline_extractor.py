import re
from typing import List, Tuple, Dict
try:
    from phone_number_extractor import PhoneNumberExtractor
except ImportError:
    from .phone_number_extractor import PhoneNumberExtractor

pne = PhoneNumberExtractor()

class HelplineExtractor:
    def __init__(self):
        # Single merged pattern combining all Bangla, English and Mixed patterns
        self.extraction_pattern = r'(?:' + '|'.join([
            # Bangla service patterns
            r'(?:হটলাইন|এজেন্ট|কল\s*সেন্টার|সাপোর্ট|অভিযোগ|গ্রাহক\s*সেবা|কাস্টমার\s*সেবা|জরুরি|টেকনিক্যাল\s*সাপোর্ট)(?:\s+নম্বর)?(?:\s*[:]\s*|\s+)([১][০-৯]{4})',
            r'(?:হটলাইন|এজেন্ট|কল\s*সেন্টার|সাপোর্ট|অভিযোগ|সেবা)(?:(?:\s+নম্বর)?\s+কল\s+করুন|ে\s+কল\s+করুন|\s+পেতে\s+কল\s+করুন|র\s+সাথে\s+যোগাযোগ|\s+জানাতে)\s*([১][০-৯]{4})',
            r'(?:ফোন|মোবাইল|যোগাযোগ)\s+(?:নম্বর\s+)?([১][০-৯]{4})',
            r'(?:কল\s+করুন|যোগাযোগ\s+করুন)\s*([১][০-৯]{4})',
            r'জরুরি\s+সেবা\s*([১][০-৯]{4})',  # Added for "জরুরি সেবা"
            r'(?:রুম\s+নম্বর|ফোন:)\s*([1][0-9]{4})',  # Added for "জরুরি সেবা"
            r'রুম\s+নম্বর\s*[:।]?\s*(\d+)',
            r'ফোন(?:\s+নম্বর)?\s*:\s*(\d+)',
            r'(?:নম্বর|নাম্বার|number)\s*(?:হলো|হল|is)?\s*[:।]?\s*(\d+)',
            
            # English service patterns
            r'(?:hotline|agent|call\s*center|support|complaint|customer\s*service|emergency|technical\s*support)(?:\s+number)?(?:\s*[:]\s*|\s+)([1][0-9]{4})',
            r'(?:call|contact)\s+(?:our\s+)?(?:hotline|agent|support|service|center)\s+(?:at\s+)?([1][0-9]{4})',  # Fixed for "call X at"
            r'(?:phone|mobile|contact)\s+(?:number\s+)?([1][0-9]{4})',
            r'(?:call|contact)\s+(?:us\s+at\s+)?([1][0-9]{4})',
            r'Call\s+(?:for\s+)?(?:service|support)\s+(?:at\s+)?([1][0-9]{4})',  # Added for "Call for service"
            r'(?:file\s+)?complaint\s+(?:at\s+)?([1][0-9]{4})',  # Added for "File complaint at"
            r'(?:emergency\s+)?service\s+([1][0-9]{4})',  # Added for "Emergency service"
            
            # Mixed language patterns
            r'(?:Customer|Emergency|support|Technical)\s+(?:সেবা|হটলাইন)\s*([১1][০-৯0-9]{4})',
            r'(?:Call|Phone)\s+করুন\s*([১1][০-৯0-9]{4})',
            r'কল\s+করুন\s*([১1][০-৯0-9]{4})',
            r'(?:Agent|Service)\s+(?:সেবার\s+জন্য|এর\s+জন্য\s+যোগাযোগ)\s*([১1][০-৯0-9]{4})',  # Added for "Agent সেবার জন্য"
            r'(?:Customer\s+care|support)\s+(?:নম্বর|হটলাইন)\s*([১1][০-৯0-9]{4})',  # Added for "Customer care নম্বর"
            r'(?:Complaint|Service)\s+(?:করতে\s+কল\s+করুন|এর\s+জন্য\s+যোগাযোগ)\s*([১1][০-৯0-9]{4})',  # Added for mixed patterns
            r'(?:Hotline|support)\s+এ\s+কল\s+করুন\s*([১1][০-৯0-9]{4})',  # For "Hotline এ কল করুন"
            r'(?:agent|support)\s+service\s+কল\s+করুন\s*([১1][০-৯0-9]{4})',
            r'(?:agent|call center)\s+service\s+at\s*([১1][০-৯0-9]{4})',
            
            # Additional patterns for better coverage
            r'(?:হটলাইন|এজেন্ট|সাপোর্ট|সেবা)\s+(?:এর\s+জন্য\s+)?(?:কল\s+করুন|নম্বর)\s*([1][0-9]{4})',
            r'(?:Customer|Emergency|support|Agent|Service)\s+(?:সেবা|হটলাইন|নম্বর)\s*([1][0-9]{4})',
            r'(?:Customer|Emergency|support)\s+এর\s+জন্য\s+কল\s+করুন\s*([1][0-9]{4})'
        ]) + r')\b'
        
        self.number_to_word = {
            "0": "জিরো", "1": "ওয়ান", "2": "টু", "3": "থ্রি", "4": "ফোর",
            "5": "ফাইভ", "6": "সিক্স", "7": "সেভেন", "8": "এইট", "9": "নাইন",
            "০": "শূন্য", "১": "এক", "২": "দুই", "৩": "তিন", "৪": "চার",
            "৫": "পাঁচ", "৬": "ছয়", "৭": "সাত", "৮": "আট", "৯": "নয়"
        }
    
    def convert_bangla_to_english(self, bangla_num: str) -> str:
        """Convert Bangla numerals to English numerals"""
        bangla_to_english = {
            '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4',
            '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'
        }
        english_num = ''
        for digit in bangla_num:
            english_num += bangla_to_english.get(digit, digit)
        return english_num
    
    def number_to_words(self, number: str) -> str:
        """Convert a number to its word representation"""
        words = []
        for digit in number:
            if digit in self.number_to_word:
                words.append(self.number_to_word[digit])
            else:
                # If digit not found, keep as is
                words.append(digit)
        return ' '.join(words)
    
    def extract_numbers_with_positions(self, text: str) -> List[Tuple[str, int, int]]:
        """Extract numbers with their positions (number, start, end)"""
        pattern = re.compile(self.extraction_pattern, re.IGNORECASE)
        results = []
        
        for match in pattern.finditer(text):
            # Get the captured group that is not None
            for i in range(1, len(match.groups()) + 1):
                if match.group(i):
                    number = match.group(i)
                    # Find the actual position of just the number within the full match
                    full_match_start = match.start()
                    full_match_text = match.group(0)
                    number_pos_in_match = full_match_text.rfind(number)
                    
                    start_pos = full_match_start + number_pos_in_match
                    end_pos = start_pos + len(number)
                    
                    results.append((number, start_pos, end_pos))
                    break
        
        return results
    
    def extract_numbers(self, text: str) -> List[str]:
        """Extract numbers using the single merged pattern"""
        results = self.extract_numbers_with_positions(text)
        return [num for num, _, _ in results]
    
    def normalize_text_with_word_conversion(self, text: str) -> str:
        """Replace extracted numbers with their word representation"""
        # Get numbers with positions
        numbers_with_positions = self.extract_numbers_with_positions(text)
        
        # Sort by position in reverse order (from end to start)
        # This ensures we don't mess up positions when replacing
        numbers_with_positions.sort(key=lambda x: x[1], reverse=True)
        
        # Create a mutable version of the text
        result_text = text
        
        # Replace each number with its word representation
        for number, start, end in numbers_with_positions:
            # word_representation = self.number_to_words(number)
            word_representation = pne.label_repeats(number, helpine=True)
            result_text = result_text[:start] + word_representation + result_text[end:]
        
        return result_text
    
    def helpline_normalization(self, text: str) -> Dict:
        """Get detailed extraction information"""
        numbers_with_positions = self.extract_numbers_with_positions(text)
        # print("Extracted Numbers with Positions:", numbers_with_positions)
        # print("text : ", text)
        # Sort by position in reverse order
        numbers_with_positions.sort(key=lambda x: x[1], reverse=True)
        for number, start, end in numbers_with_positions:

            # print(f"Replacing number '{number}' at positions ({start}, {end})")
            # word_string = self.number_to_words(number)
            word_string = pne.label_repeats(number, helpine=True)

            text = text[:start] + word_string + text[end:]
        # print("Normalized Text:", text)
        return text

if __name__ == "__main__":
    # Initialize extractor
    extractor = HelplineExtractor()
    test_lines = """
        # "আমাদের হটলাইনে নম্বর কল করুন ১৬২২১, আমাদের হটলাইনে নম্বর কল করুন ১৬২২১",
        # "এজেন্ট সেবা পেতে কল করুন ১৬২৩৪",
        # "Call our hotline number 16221",
        # "Emergency হটলাইন ১৬২২১ and support 16456",
        # "হটলাইন: ১৬২২১, এজেন্ট: ১৬৫৬৭",
        # "আমাদের হটলাইনে নম্বর কল করুন ১৬২২১, আমাদের হটলাইনে নম্বর কল করুন ১৬২২১",
        # "এজেন্ট সেবা পেতে কল করুন ১৬২৩৪",
        # "এজেন্ট নম্বর ১৬৫৬৭",
        # "কল সেন্টার নম্বর ১৬৯৮১",
        # "আমার ফোন নম্বর ১৬৭৮৯",
        # "আমাদের একাউন্ট নম্বর ১৬২২১",  # Won't match
        # "ব্যাংক একাউন্ট নম্বর ১৬৩৪৫",  # Won't match
        # "হটলাইন: ১৬২২১",
        # "Call our hotline number 16221",
        # "Agent Patterns: 16832",
        # "Customer সেবা 16789",
        # "Emergency হটলাইন ১৬২২১",
        # "Support এর জন্য কল করুন 16456",
        # "যোগাযোগ নম্বর ১৬৫৬৭",
        # "মোবাইল নম্বর ১৬৭৮৯",
        # "রেজিস্ট্রেশন নম্বর ১৬৩৪৫",  # Won't match
        # "Phone number 16789",
        # "My account number 16221",  # Won't match
        # "Contact us at 16567",
        # "Just a number 16789",  # Won't match
        # "My account number 16221",  # Invalid
        # Hotline Patterns:
        # আমাদের হটলাইনে নম্বর কল করুন ১৬২২১
        # হটলাইন নম্বর ১৬২২১
        # হটলাইন: ১৬২২১
        # হটলাইনে কল করুন ১৬২২১
        # জরুরি হটলাইন ১৬২২১
        # Agent Patterns:
        # এজেন্ট সেবা পেতে কল করুন ১৬২৩৪
        # এজেন্ট নম্বর ১৬৫৬৭
        # এজেন্ট হটলাইন ১৬৫৬৭
        # এজেন্টের সাথে যোগাযোগ ১৬৫৬৭
        # এজেন্ট: ১৬৫৬৭
        # Call Center Patterns:
        # কল সেন্টার নম্বর ১৬৯৮১
        # কল সেন্টার: ১৬৯৮১
        # কল সেন্টারে যোগাযোগ করুন ১৬৯৮১
        # আমাদের কল সেন্টার ১৬৯৮১
        # ২৪/৭ কল সেন্টার ১৬৯৮১
        # Service Patterns:
        # কাস্টমার সেবা ১৬৭৮৯
        # সেবা হটলাইন ১৬৭৮৯
        # গ্রাহক সেবা নম্বর ১৬৭৮৯
        # সেবা পেতে কল করুন ১৬৭৮৯
        # জরুরি সেবা ১৬৭৮৯
        # Support Patterns:
        # সাপোর্ট নম্বর ১৬৪৫৬
        # টেকনিক্যাল সাপোর্ট ১৬৪৫৬
        # সাপোর্ট হটলাইন ১৬৪৫৬
        # সাপোর্টে কল করুন ১৬৪৫৬
        # Complaint Patterns:
        # অভিযোগ নম্বর ১৬৩৪৫
        # অভিযোগ জানাতে ১৬৩৪৫
        # অভিযোগ হটলাইন ১৬৩৪৫
        # English Patterns
        # Hotline Patterns:
        # Call our hotline number 16221
        # Hotline number 16221
        # Hotline: 16221
        # Call hotline at 16221
        # Emergency hotline 16221
        # Agent Patterns:
        # Call agent service at 16234
        # Agent number 16567
        # Agent hotline 16567
        # Contact agent 16567
        # Agent: 16567
        # Call Center Patterns:
        # Call center number 16981
        # Call center: 16981
        # Contact our call center 16981
        # Our call center 16981
        # 24/7 call center 16981
        # Service Patterns:
        # Customer service 16789
        # Service hotline 16789
        # Customer service number 16789
        # Call for service 16789
        # Emergency service 16789
        # Support Patterns:
        # Support number 16456
        # Technical support 16456
        # Support hotline 16456
        # Call support at 16456
        # Complaint Patterns:
        # Complaint number 16345
        # File complaint at 16345
        # Complaint hotline 16345
        # Mixed Language Patterns:
        # Customer সেবা 16789
        # Call করুন 16221
        # Emergency হটলাইন ১৬২২১
        # Support এর জন্য কল করুন 16456
        # Additional Mixed Patterns (Common Variations):
        # Hotline এ কল করুন ১৬২২১
        # Agent সেবার জন্য ১৬৫৬৭
        # Technical সাপোর্ট নম্বর 16456
        # Emergency সেবা হটলাইন ১৬৭৮৯
        # Customer care নম্বর ১৬৭৮৯
        # Support হটলাইন ১৬৪৫৬
        # Complaint করতে কল করুন 16345
        please call Service এর জন্য যোগাযোগ 16789

    """

    # test_lines ="""
    #     আমাদের হটলাইনে নম্বর কল করুন ১৬২২১, আমাদের হটলাইনে নম্বর কল করুন 16441
    #     ফোন নম্বর: 16021
    #     """
    print("Testing Extraction with Positions and Word Conversion:")
    print("=" * 80)
    
    for text in test_lines.split("\n"):
        if text.strip():
          print(f"\nOriginal Text: {text}")
          print("-" * 40)
          # Get detailed extraction results
          text = extractor.helpline_normalization(text)
          print("Final Normalized Text:", text)
          print("-" * 40)