import re
from typing import Dict, Tuple, Optional, List
from num2words import num2words
# try:
#     from .config import Config as cfg
# except ImportError:
#     from config import Config as cfg
class NumberNormalizationService:
    def __init__(self):
        # Bengali to English digit mapping
        self.mapping_normalization = {
            '0': 'জিরো', '1': 'ওয়ান', '2': 'টু', '3': 'থ্রি', '4': 'ফোর', 
            '5': 'ফাইভ', '6': 'সিক্স', '7': 'সেভেন', '8': 'এইট', '9': 'নাইন',
            '০': 'শূন্য', '১': 'এক', '২': 'দুই', '৩': 'তিন', '৪': 'চার',
            '৫': 'পাঁচ', '৬': 'ছয়', '৭': 'সাত', '৮': 'আট', '৯': 'নয়'
        }


        # Month names in Bengali and English
        self.month_names = [
            'জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন',
            'জুলাই', 'আগস্ট', 'সেপ্টেম্বর', 'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর',
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december',
            'jan', 'feb', 'mar', 'apr', 'may', 'jun',
            'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
        ]
        
        # Date pattern to exclude from normalization
        # Matches 1-2 digits (date) followed by month name
        self.date_pattern = r'([০-৯\d]{1,2})\s*(' + '|'.join(self.month_names) + r')'

        # self.passport_pattern = r'(?i)(?:e-passport|ই-পাসপোর্ট|e\s+passport|ই\s+পাসপোর্ট|passport|পাসপোর্ট)\s*(?:id|আইডি|নম্বর|নাম্বার|নং|number|no)?\s*[:=\-]?\s*([A-Za-z\u0985-\u09B9]?[\s\-]?[\u09E6-\u09EF0-9]+)'
        self.passport_pattern = r'(?i)(?:e-passport|ই-পাসপোর্ট|e\s+passport|ই\s+পাসপোর্ট|passport|পাসপোর্ট)\s*(?:id|আইডি|নম্বর|নাম্বার|নং|number|no)?\s*[:=\-]?\s*([A-Za-z\u0985-\u09B9]?[\s\-]?[\u09E6-\u09EF0-9]{7,9}(?:\s*ও\s*[A-Za[z\u0985-\u09B9]?[\s\-]?[\u09E6-\u09EF0-9]{7,9})*)'

        self.number_pattern = r'([A-Za-z\u0985-\u09B9]?[\s\-]?[\u09E6-\u09EF0-9]{7,9})'

        
        # Updated field patterns to handle alphanumeric identifiers
        self.field_patterns = [
            # Account variations
            (r'(?i)(ভোটার|একাউন্ট|account|a/c|A/C|a c|A C|acc|acct|হিসাব)\s*(নম্বর|নাম্বার|নং|ন\.|number|no|id|আইডি\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'account_number'),
            
            # Receipt variations
            (r'(?i)(রিসিপ্ট|রশিদ|রসিদ|receipt|ricipt|rcpt|rec)\s*(নম্বর|নাম্বার|নং|number|no|id|আইডি\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'receipt_number'),
            
            # Transaction variations
            (r'(?i)(ট্রানজেকশন|লেনদেন|টিকেট|transaction|transcrition|trans|txn|trx)\s*(নম্বর|নাম্বার|নং|number|no|id|আইডি\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'transaction_number'),
            
            # Slip variations
            (r'(?i)(শ্লিপ|স্লিপ|চেক|slip|cilip)\s*(নম্বর|নাম্বার|নং|number|no|আইডি|id\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'slip_number'),
            
            # Card variations
            (r'(?i)(কার্ড|card)\s*(নম্বর|নাম্বার|number|নং|no|id|আইডি\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'card_number'),
            
            # Token variations
            (r'(?i)(টোকেন|token)(?:\s*id)?\s*(নম্বর|নাম্বার|নং|number|no|আইডি|id\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'token_number'),
            
            # Bill variations
            (r'(?i)(বিল|bill)\s*(নম্বর|নাম্বার|নং|number|no|আইডি|id\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'bill_number'),
            
            # Invoice variations - UPDATED to handle alphanumeric patterns
            (r'(?i)(চালান|ইনভয়েস|invoice|inv)\s*(নম্বর|নাম্বার|নং|number|no|আইডি|id\.?)?\s*:?\s*([A-Z]*-?[০-৯\d\-\s\.]+)', 'invoice_number'),
            
            # Voucher variations
            (r'(?i)(ভাউচার|voucher)\s*(নম্বর|নাম্বার|নং|number|no|আইডি|id\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'voucher_number'),
            
            # Order variations - UPDATED to handle alphanumeric patterns
            (r'(?i)(অর্ডার|order)\s*(নম্বর|নাম্বার|নং|number|no|আইডি|id\.?)?\s*:?\s*([A-Z]*-?[০-৯\d\-\s\.]+)', 'order_number'),
            
            # Reference variations - UPDATED to handle alphanumeric patterns
            (r'(?i)(রেফারেন্স|reference|ref)\s*(নম্বর|নাম্বার|নং|number|no|আইডি|id\.?)?\s*:?\s*([A-Z]*-?[০-৯\d\-\s\.]+)', 'reference_number'),
            
            # Payment variations
            (r'(?i)(পেমেন্ট|payment)(?:\s*(?:id|আইডি|নম্বর|নাম্বার|number))?\s*:?\s*([০-৯\d\-\s\.]+)', 'payment_id'),
            
            # Tracking variations - UPDATED to handle alphanumeric patterns
            (r'(?i)(ট্র্যাকিং|tracking|track)\s*(নম্বর|নাম্বার|নং|number|no|আইডি|id\.?)?\s*:?\s*([A-Z]*-?[০-৯\d\-\s\.]+)', 'tracking_number'),
            
            # Customer variations
            (r'(?i)(গ্রাহক|কাস্টমার|customer|cust)\s*(id|আইডি|নম্বর|number|no)?\s*:?\s*([০-৯\d\-\s\.]+)', 'customer_id'),
            # Passport variations
            (r'(?i)(e-passport|ই-পাসপোর্ট|e passport|ই পাসপোর্ট|passport|পাসপোর্ট)\s*(id|আইডি|নম্বর|নাম্বার|নং|number|no)?\s*:?-?\s*([A-Zএ-ঔ]?[০-৯0-9]+)', 'passport_id')
        ]



    def extract_passport_unicode(self, text):
        """
        Extract using Unicode ranges for Bengali characters
        Returns a list of dicts with passport number and its span
        """
        # Example: self.passport_pattern could be something like r"[A-Z0-9\u0985-\u09EF]{8,10}"
        matches = re.finditer(self.passport_pattern, text)

        sorted_matches = sorted(matches, key=lambda m: m.start(),  reverse=True)

        # print("sorted_matches : ", sorted_matches)

        # extracted_passports = []
        for match in sorted_matches:
            string_pass = match.group(0)
            index_span = match.span()

            # print("Found passport number:", string_pass, " at position:", index_span)
            # Extract digits from the cleaned passport string
            digits = re.findall(self.number_pattern, string_pass)
            

            # print("digits:", digits)            
            for digit in digits:
                words = []
                for d in digit:
                    if d in self.mapping_normalization:
                        words.append(self.mapping_normalization[d])
                    else:
                        words.append(d)
                normalize_string = (", ".join(words))
                # print("normalize_string:", digit , "->", normalize_string)

                string_pass = string_pass.replace(digit, " "+normalize_string+" ")

            text = text[:index_span[0]] + " "+string_pass+" "+ text[index_span[1]:]

        # if have multiple comma then replace with one comma
        text = re.sub(r',\s*,+', ', ', text)

        return text

    
    def extract_field_and_number_with_spans(self, text: str) -> List[Tuple[str, str, str, Tuple[int, int]]]:
        """Extract field name, clean number, original number format and span position from text"""
        extractions = []
        
        for pattern, field_name in self.field_patterns:
            for match in re.finditer(pattern, text):
                # Find the last non-None group that contains numbers
                number_text_original = None
                number_start = None
                number_end = None
                
                for i in range(len(match.groups()), 0, -1):
                    group = match.group(i)
                    if group and re.search(r'[০-৯\d]', group):
                        number_text_original = group.strip()
                        # Get the span of this specific group
                        number_start = match.start(i)
                        number_end = match.end(i)
                        break
                
                if number_text_original and number_start is not None:
                    # For alphanumeric IDs, extract only the numeric part
                    # but keep the original format for replacement
                    numeric_parts = re.findall(r'[০-৯\d]+', number_text_original)
                    if numeric_parts:
                        # Join all numeric parts
                        clean_number = ''.join(numeric_parts)
                        # Convert Bengali digits to English
                        clean_number = self.convert_bengali_to_english(clean_number)
                        
                        if clean_number:
                            # Adjust span to match the actual position of the number in the original text
                            actual_start = text.find(number_text_original, number_start)
                            if actual_start != -1:
                                actual_end = actual_start + len(number_text_original)
                                extractions.append((field_name, clean_number, number_text_original, (actual_start, actual_end)))
        
        return extractions
    
    def extract_field_and_number(self, text: str) -> Optional[Tuple[str, str, str]]:
        """Extract field name, clean number, and original number format from text (backward compatibility)"""
        extractions = self.extract_field_and_number_with_spans(text)
        if extractions:
            return extractions[0][:3]  # Return first match without span
        return None
    
    def convert_bengali_to_english(self, text: str) -> str:
        """Convert Bengali digits to English digits"""
        bengali_to_english = {
            '০': '0', '১': '1', '২': '2', '৩': '3', '৪': '4',
            '৫': '5', '৬': '6', '৭': '7', '৮': '8', '৯': '9'
        }
        for bengali, english in bengali_to_english.items():
            text = text.replace(bengali, english)
        return text
    
    def number_to_words_with_format(self, number: str, original_format: str) -> str:
        """Convert number to words while preserving the original format structure"""
        # If the original has a prefix (like INV-, ORD-, etc.), preserve it
        prefix_match = re.match(r'^([A-Z]+-)', original_format)
        prefix = prefix_match.group(1) if prefix_match else ''
        
        # Convert the numeric part to words
        words = []
        for digit in number:
            if digit in self.mapping_normalization:
                words.append(self.mapping_normalization[digit])
            else:
                words.append(digit)
        
        # If there was a prefix, add it back
        if prefix:
            return prefix + ', '.join(words)
        else:
            return ', '.join(words)
        
    def date_patter_procesing(self, text: str):
        """Find positions of date numbers that should not be normalized"""
        exclude_positions = []

        matches = re.finditer(self.date_pattern, text, re.IGNORECASE)

        sorted_matches = sorted(matches, key=lambda m: m.start(),  reverse=True)

        # Find all date patterns
        for match in sorted_matches:
            # Get the position of the date number
            word = match.group(1)
            date_start = match.start(1)
            date_end = match.end(1)
            exclude_positions.append((date_start, date_end))
            # print("Found date to exclude:", word)
            #  need to check bangla number or english number
            lang = 'bn'
            if re.search(r'[০-৯]', word):
                lang = 'bn'
                word_in_bengali = num2words(word, lang=lang)
            elif re.search(r'[0-9]', word):
                lang = 'en'
                word_in_bengali = num2words(word, lang=lang)
                # word_in_bengali = cfg._bangla_numeric_words[word_in_en]

            # Replace the date number with its word form in the text
            text = text[:date_start] + " "+word_in_bengali +" "+ text[date_end:]
            # print("Replaced date number with words:", text)


        return text
    
    def number_to_words(self, number: str) -> str:
        """Convert number digits to Bengali words"""
        words = []
        for digit in number:
            if digit in self.mapping_normalization:
                words.append(self.mapping_normalization[digit])
            else:
                words.append(digit)
        return ', '.join(words)
    
    def replace_numbers_with_words(self, text: str) -> str:
        """Replace numbers in text with Bengali words using span-based replacement"""
        # Handle date pattern processing first
        text = self.date_patter_procesing(text)

        text = self.extract_passport_unicode(text)

        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            processed_line = line
            
            # Extract all field and number matches with spans
            extractions = self.extract_field_and_number_with_spans(line)
            
            # print("extractions with spans: ", extractions)
            
            if extractions:
                # Sort extractions by span position in reverse order to prevent index shifting
                sorted_extractions = sorted(extractions, key=lambda x: x[3][0], reverse=True)
                
                # print("sorted_extractions: ", sorted_extractions)
                
                # Process each extraction from right to left
                for field_name, clean_number, original_number_format, span in sorted_extractions:
                    start_pos, end_pos = span
                    
                    # Check if the original format has a letter prefix
                    if re.match(r'^[A-Z]+-', original_number_format):
                        # Use special formatting for alphanumeric IDs
                        words = self.number_to_words_with_format(clean_number, original_number_format)
                    else:
                        # Regular number conversion
                        words = self.number_to_words(clean_number)
                    
                    # Replace using span positions
                    processed_line = processed_line[:start_pos] + words + processed_line[end_pos:]
                    
                    # print(f"Replaced '{original_number_format}' at position {start_pos}-{end_pos} with '{words}'")
            
            processed_lines.append(processed_line)
        
        return ' '.join(processed_lines)


# Example usage
if __name__ == "__main__":
    service = NumberNormalizationService()
    
    # Test the problematic cases
    test_cases = [
    "একাউন্ট নম্বর ১২৩৪৫৬৬",
    "account number 1234567890",
    "রিসিপ্ট  নম্বর 123452",
    "ricipt number 123456677989",
    "রশিদ  নম্বর 8904390",
   " ট্রানজেকশন নাম্বার 893023",
    "transcrition number 12338902983",
    "শ্লিপ নম্বর 1234567890123",
    "cilip number 1234567890123",
    "card number 1234567890123",
    "token id number 1234567890123",
    "টোকেন নম্বর  ৪৫৬৭৮০৩৪৫",
    "বিল নম্বর  ৪৫৬৭৮০৩৪৫ hello how are you",
    "bill number 456780345",
    "চালান নম্বর  ৪৫৬৭৮০৩৪৫",
    "invoice number 456780345",
    "আমার একাউন্ট নম্বর ১২৩৪৫৬৭৮৯০ থেকে টাকা কেটে নিয়েছে।",
    "Please transfer the amount to account number 1234567890 before 5 PM.",
    "গ্রাহকের A/C নং: ৯৮৭৬৫৪৩২১০ এ জমা করুন।",
    "Your savings acc no. 123-456-7890 has been credited with BDT 5000.",
    "আপনার হিসাব নাম্বার: ১২৩৪ ৫৬৭৮ ৯০১২ সফলভাবে খোলা হয়েছে।",
    "The loan amount will be deducted from ACCT NUMBER: 1234.5678.9012 monthly.",
    "আপনার একাউন্ট নম্বর ১২৩৪৫৬৬ সংরক্ষণ করুন।",
    "Account No. 987-654-3210 is linked to your mobile number.",
    "আপনার রিসিপ্ট নম্বর ৪৫৬৭৮৯০১২৩ সংরক্ষণ করুন ভবিষ্যতের জন্য।",
    "রশিদ নং: ১২৩৪৫৬ দেখিয়ে আপনার পণ্য সংগ্রহ করুন।",
    "মূল রসিদ নাম্বার ৯৮৭-৬৫৪-৩২১ ছাড়া রিটার্ন সম্ভব নয়।",
    "Your payment receipt number: 123456789 has been generated successfully.",
    "অনুগ্রহ করে Ricipt Number 876543210 টি প্রিন্ট করে রাখুন।",
    "The rcpt no. 555-666-777 is required for warranty claims.",
    "আপনার রিসিপ্ট নম্বর ৪৫৬৭৮৯০১২৩ সংরক্ষণ করুন ভবিষ্যতের জন্য।",
    "রশিদ নং: ১২৩৪৫৬ দেখিয়ে আপনার পণ্য সংগ্রহ করুন।",
    "মূল রসিদ নাম্বার ৯৮৭-৬৫৪-৩২১ ছাড়া রিটার্ন সম্ভব নয়।",
    "Your payment receipt number: 123456789 has been generated successfully.",
    "অনুগ্রহ করে Ricipt Number 876543210 টি প্রিন্ট করে রাখুন।",
    "The rcpt no. 555-666-777 is required for warranty claims.",
    "আপনার রিসিপ্ট নম্বর ৪৫৬৭৮৯০১২৩ সংরক্ষণ করুন ভবিষ্যতের জন্য।",
    "রশিদ নং: ১২৩৪৫৬ দেখিয়ে আপনার পণ্য সংগ্রহ করুন।",
    "মূল রসিদ নাম্বার ৯৮৭-৬৫৪-৩২১ ছাড়া রিটার্ন সম্ভব নয়।",
    "Your payment receipt number: 123456789 has been generated successfully.",
    "অনুগ্রহ করে Ricipt Number 876543210 টি প্রিন্ট করে রাখুন।",
    "The rcpt no. 555-666-777 is required for warranty claims.",
    "আপনার ট্রানজেকশন নম্বর 891২৩৪৫৬৭৮ দিয়ে অভিযোগ করুন।",
    "আজকের লেনদেন নং: ৭৮৯০১২৩৪৫৬ সফল হয়েছে।",
    "Your transaction number 123456789012 has been processed at 2:30 PM.",
    "Failed transcrition number 999-888-777-666 will be reversed within 7 days.",
    "দয়া করে Trans No. ৬৫৪৩২১০৯৮৭ রেফারেন্স হিসাবে ব্যবহার করুন।",
    "TXN নাম্বার: 111222333444 এর জন্য ১০ টাকা চার্জ কাটা হয়েছে।",
    "আপনার ট্রানজেকশন নম্বর 891২৩৪৫৬৭৮ দিয়ে অভিযোগ করুন।",
    "আজকের লেনদেন নং: ৭৮৯০১২৩৪৫৬ সফল হয়েছে।",
    "Your transaction number 123456789012 has been processed at 2:30 PM.",
    "Failed transcrition number 999-888-777-666 will be reversed within 7 days.",
    "ব্যাংক শ্লিপ নম্বর ৩৪৫৬৭৮৯০১২ জমা দেওয়া হয়েছে।",
    "আপনার জমা স্লিপ নং: ৯৮৭৬৫৪৩২১০ অনুমোদন করা হয়েছে।",
    "Please keep the deposit slip number 123-456-789 for your records.",
    "উত্তোলন cilip number 555666777888 প্রসেসিং এ আছে।",
    "Deposit slip no. 123456789012 has been verified.",
    "আপনার শ্লিপ নম্বর ৩৪৫৬৭৮৯০১২ জমা দেওয়া হয়েছে।",
    "আপনার কার্ড নম্বর ১২৩৪৫৬৭৮৯০১২৩ দিয়ে পেমেন্ট সফল হয়েছে।",
    "Card number 9876-5432-1098-7654 is valid until 12/25.",
    "আপনার কার্ড নম্বর ৪৫৬৭ ৮৯০১ ২৩৪৫ ৬৭৮৯ দিয়ে পেমেন্ট করুন।",
    "Your new card number 1234-5678-9012-3456 will be activated within 24 hours.",
    "অনুগ্রহ করে Card নং ৯৮৭৬৫৪৩২১০৯৮৭৬ এর CVV দিন।",
    "Credit card no. 1234 5678 9012 3456 has been blocked due to suspicious activity.",
    "আপনার কার্ড নম্বর ১২৩৪৫৬৭৮৯০১২৩ দিয়ে পেমেন্ট সফল হয়েছে।",
    "Card number 9876-5432-1098-7654 is valid until 12/25.",
    "আপনার কার্ড নম্বর ৪৫৬৭ ৮৯০১ ২৩৪৫ ৬৭৮৯ দিয়ে পেমেন্ট করুন।",
    "Your new card number 1234-5678-9012-3456 will be activated within 24 hours.",
    "অনুগ্রহ করে Card নং ৯৮৭৬৫৪৩২১০৯৮৭৬ এর CVV দিন।",
    "Credit card no. 1234 5678 9012 3456 has been blocked due to suspicious activity.",
    "আপনার টোকেন নম্বর ৫৬৭৮৯০১২৩৪ দিয়ে লগইন করুন।",
    "Security token ID number 123456789012 expires at midnight.",
    "নতুন Token নং: ৯৮৭-৬৫৪-৩২১ জেনারেট করা হয়েছে।",
    "আপনার টোকেন নম্বর ৫৬৭৮৯০১২৩৪ দিয়ে লগইন করুন।",
    "এই মাসের বিল নম্বর ৮৯০১২৩৪৫৬৭ এর বকেয়া ৫০০০ টাকা।",
    "Your electricity bill number 202401-123456 is due on 15th January.",
    "বিল নং: ৭৮৯০১২৩৪৫৬ অনলাইনে পরিশোধ করা যাবে।",
    "আপনার বিদ্যুৎ বিল নম্বর ২০২৪০১-১২৩৪৫৬ ১৫ জানুয়ারি তারিখে পরিশোধ করতে হবে।",
    "আমাদের চালান নম্বর ৬৭৮৯০১২৩৪৫ অনুযায়ী পেমেন্ট করুন।",
    "Invoice number INV-2024-123456 has been sent to your email.",
    "মূল inv নং ৪৫৬৭৮৯০১২৩ ছাড়া পণ্য ফেরত নেওয়া হবে না।",
    "আপনার ইনভয়েস নম্বর ১২৩৪৫৬৭৮৯০১২ বৈধ।",
    "আপনার ভাউচার নম্বর ৩৪৫৬৭৮৯০১২ ৩১ ডিসেম্বর পর্যন্ত বৈধ।",
    "Gift voucher number 123-456-789-012 can be redeemed online.",
    "ভাউচার নং: ৯৮৭৬৫৪৩২১০ ব্যবহার করে ২০% ছাড় পাবেন।",
    "আপনার ভাউচার নম্বর ৩৪৫৬৭৮৯০১২ ৩১ ডিসেম্বর পর্যন্ত বৈধ।",
    "Gift voucher number 123-456-789-012 can be redeemed online.",
    "ভাউচার নং: ৯৮৭৬৫৪৩২১০ ব্যবহার করে ২০% ছাড় পাবেন।",
    "আপনার ভাউচার নম্বর ৩৪৫৬৭৮৯০১২ ৩১ ডিসেম্বর পর্যন্ত বৈধ।",
    "আপনার অর্ডার নম্বর ৮৯০১২৩৪৫৬৭ ট্র্যাক করুন।",
    "Your order number ORD-2024-123456 has been shipped today.",
    "অর্ডার নং: ৬৭৮৯০১২৩৪৫ এর ডেলিভারি ৩ দিনের মধ্যে হবে।",
    "আমার অর্ডার নাম্বার ১২৩৪৫৬৭৮৯০১২ বাতিল করতে চাই।",
    "Order No. 987-654-3210 has been delivered successfully.",
    "অর্ডার নম্বর: ৫৬৭৮৯০১২৩৪৫ এর ডেলিভারি ৩ দিনের মধ্যে হবে।",
    "দয়া করে রেফারেন্স নম্বর ৪৫৬৭৮৯০১২৩ উল্লেখ করুন।",
    "Use reference number REF-123-456-789 for all correspondence.",
    "আপনার Ref নং: ৯৮৭৬৫৪৩২১০ দিয়ে স্ট্যাটাস চেক করুন।",
    "পেমেন্ট আইডি ১২৩৪৫৬৭৮৯০১২ নিশ্চিত হয়েছে BDT ১০,০০০ এর জন্য।",
    "আপনার পেমেন্ট আইডি ৭৮৯০১২৩৪৫৬ সেভ করে রাখুন।",
    "Payment ID 123456789012 confirmed for BDT 10,000.",
    "পেমেন্ট নম্বর: ৫৬৭-৮৯০-১২৩ দিয়ে রিফান্ড ট্র্যাক করুন।",
    "আপনার ট্র্যাকিং নম্বর ১২৩৪৫৬৭৮৯০১২ দিয়ে পণ্য ট্র্যাক করুন।",
    "পার্সেল ট্র্যাকিং নম্বর ৬৭৮৯০১২৩৪৫৬৭৮ দিয়ে খুঁজুন।",
    "Your tracking number TRK-123-456-789-012 shows delivery tomorrow.",
    "ট্র্যাকিং নং: ৪৫৬৭৮৯০১২৩৪৫ অনলাইনে চেক করুন।",
    "আপনার ট্র্যাকিং নম্বর ১২৩৪৫৬৭৮৯০১২ দিয়ে পণ্য ট্র্যাক করুন।",
    "পার্সেল ট্র্যাকিং নম্বর ৬৭৮৯০১২৩৪৫৬৭৮ দিয়ে খুঁজুন।",
    "আপনার গ্রাহক আইডি ৯০১২৩৪৫৬৭৮ প্রোফাইলে আপডেট করুন।",
    "Customer ID 123456789012 is eligible for premium benefits.",
    "কাস্টমার নম্বর: ৭৮৯-০১২-৩৪৫৬ দিয়ে লগইন করুন।",
    "Your customer ID 123-456-789-012 is valid.",
    "আমার account নম্বর ১২৩৪৫৬৭৮৯০ থেকে টাকা transfer করুন।",
    "নতুন receipt নং: 987654321 জেনারেট হয়েছে।",
    "আপনার transaction নাম্বার ৫৬৭৮৯০ সফল হয়েছে।",
    "Havit HV-SC055 Laptop Cleaning Kit - HV-SC055 and the number is the 12345 and my acound amount is 1234567"
    ]

    test_cases = [
        "hello পাসপোর্ট নম্বর ই১২৩৪৫৬৭৭, hi পাসপোর্ট নম্বর ই১২৩৪৫৬৭৭,",
        "passport number: A12345678 and amar account number A23456781 ",
        "ই-পাসপোর্ট আইডি: উ৯৮৭৬৫৪৩২",
        "e-passport no: ক১২৩৪৫৬৭৮",
        "পাসপোর্ট: অ৯৯৯৯৯৯৯৯",
        "পাসপোর্ট নম্বর ই১২৩৪৫৬৭৭"
        "পাসপোর্ট নম্বর স১২৩৪৫৬৭৭",
        "hello পাসপোর্ট নম্বর ই১২৩৪৫৬৭৭, hi পাসপোর্ট নম্বর ই১২৩৪৫৬৭৭,",
        "Your customer ID 123-456-789-012 is valid.",
        "আমার পাসপোর্ট নম্বর A01234567 এবং তার পাসপোর্ট নম্বর 987654321।",
        "নতুন ই-পাসপোর্ট নম্বর E12345678 ইস্যু করা হয়েছে।",
        "তিনি পুরাতন পাসপোর্ট নম্বর 1234567 ব্যবহার করেছেন।",
        "মেশিন রিডেবল পাসপোর্ট নম্বর B76543210।",
        "তার পাসপোর্ট নম্বর P87654321 ছিল।",
        "তার পাসপোর্ট নম্বর P০১২৩৪৫৬৭ ছিল।",
        "বাংলা নম্বর হিসেবে পাসপোর্ট নম্বর এ০১২৩৪৫৬৭ ও ই১২৩৪৫৬৭৮।",
        "পাসপোর্ট নম্বর এ০১২৩৪৫৬৭ ও ই১২৩৪৫৬৭৮।"   
    ]
    
    print("Testing Alphanumeric Number Normalization\n")
    print("=" * 80)

    print("testing data : ", len(test_cases))
    
    for i, test_text in enumerate(test_cases):
        print("index : ", i)
        print(f"Input: {test_text}")
        replaced = service.replace_numbers_with_words(test_text)
        print(f"Output: {replaced}")
        print("-" * 80)