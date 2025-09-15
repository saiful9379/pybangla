import re
from typing import Dict, Tuple, Optional

class NumberNormalizationService:
    def __init__(self):
        # Bengali to English digit mapping
        self.mapping_normalization = {
            '0': 'জিরো', '1': 'ওয়ান', '2': 'টু', '3': 'থ্রি', '4': 'ফোর', 
            '5': 'ফাইভ', '6': 'সিক্স', '7': 'সেভেন', '8': 'এইট', '9': 'নাইন',
            '০': 'শূন্য', '১': 'এক', '২': 'দুই', '৩': 'তিন', '৪': 'চার',
            '৫': 'পাঁচ', '৬': 'ছয়', '৭': 'সাত', '৮': 'আট', '৯': 'নয়'
        }
        
        # Field normalization patterns - updated to capture numbers
        self.field_patterns = [
            # Account variations with number capture
            (r'(?i)(একাউন্ট|account|a/c|A/C|a c|A C|acc|acct|হিসাব)\s*(নম্বর|নাম্বার|নং|ন\.|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'account_number'),
            
            # Receipt variations with number capture
            (r'(?i)(রিসিপ্ট|রশিদ|রসিদ|receipt|ricipt|rcpt|rec)\s*(নম্বর|নাম্বার|নং|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'receipt_number'),
            
            # Transaction variations with number capture
            (r'(?i)(ট্রানজেকশন|লেনদেন|transaction|transcrition|trans|txn|trx)\s*(নম্বর|নাম্বার|নং|number|no|id\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'transaction_number'),
            
            # Slip variations with number capture
            (r'(?i)(শ্লিপ|স্লিপ|slip|cilip)\s*(নম্বর|নাম্বার|নং|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'slip_number'),
            
            # Card variations with number capture
            (r'(?i)(কার্ড|card)\s*(নম্বর|নাম্বার|number|নং|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'card_number'),
            
            # Token variations with number capture
            (r'(?i)(টোকেন|token)(?:\s*id)?\s*(নম্বর|নাম্বার|নং|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'token_number'),
            
            # Bill variations with number capture
            (r'(?i)(বিল|bill)\s*(নম্বর|নাম্বার|নং|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'bill_number'),
            
            # Invoice variations with number capture
            (r'(?i)(চালান|ইনভয়েস|invoice|inv)\s*(নম্বর|নাম্বার|নং|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'invoice_number'),
            
            # Voucher variations with number capture
            (r'(?i)(ভাউচার|voucher)\s*(নম্বর|নাম্বার|নং|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'voucher_number'),
            
            # Order variations with number capture
            (r'(?i)(অর্ডার|order)\s*(নম্বর|নাম্বার|নং|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'order_number'),
            
            # Reference variations with number capture
            (r'(?i)(রেফারেন্স|reference|ref)\s*(নম্বর|নাম্বার|নং|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'reference_number'),
            
            # Payment variations with number capture
            (r'(?i)(পেমেন্ট|payment)(?:\s*(?:id|আইডি|নম্বর|নাম্বার|number))?\s*:?\s*([০-৯\d\-\s\.]+)', 'payment_id'),
            
            # Tracking variations with number capture
            (r'(?i)(ট্র্যাকিং|tracking|track)\s*(নম্বর|নাম্বার|নং|number|no\.?)?\s*:?\s*([০-৯\d\-\s\.]+)', 'tracking_number'),
            
            # Customer variations with number capture
            (r'(?i)(গ্রাহক|কাস্টমার|customer|cust)\s*(id|আইডি|নম্বর|number)?\s*:?\s*([০-৯\d\-\s\.]+)', 'customer_id'),
        ]
        
        # Number extraction patterns
        self.number_patterns = [
            r'[\d০-৯]+[\s\-\.]*[\d০-৯]*[\s\-\.]*[\d০-৯]*',  # Matches numbers with separators
            r'#\s*([\d০-৯]+)',  # Numbers with # prefix
            r':\s*([\d০-৯]+)',  # Numbers after colon
        ]
        
    def extract_field_and_number(self, text: str) -> Optional[Tuple[str, str]]:
        """Extract field name and number from text using field patterns"""
        for pattern, field_name in self.field_patterns:
            match = re.search(pattern, text)
            if match:
                # For most patterns, the number is in the last group
                # Find the last non-None group that contains numbers
                number_text = None
                for i in range(len(match.groups()), 0, -1):
                    group = match.group(i)
                    if group and re.search(r'[০-৯\d]', group):
                        number_text = group.strip()
                        break
                
                if number_text:
                    # Convert Bengali digits first
                    # number_text = self.convert_bengali_to_english(number_text)
                    clean_number = re.sub(r'[^\d]', '', number_text)
                    if clean_number:
                        return (field_name, clean_number)
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
    
    def number_to_words(self, number: str) -> str:
        """Convert number digits to Bengali words"""
        words = []
        for digit in number:
            if digit in self.mapping_normalization:
                words.append(self.mapping_normalization[digit])
            else:
                words.append(digit)
        return ', '.join(words)

    def convert_bengali_digits(self, text: str) -> str:
        """Convert Bengali digits to English digits - legacy method"""
        return self.convert_bengali_to_english(text)
    
    def normalize_field_name(self, text: str) -> Optional[str]:
        """Normalize field names to standard format"""
        for pattern, replacement in self.field_patterns:
            if re.search(pattern, text):
                return replacement
        return None
    
    def extract_number(self, text: str) -> Optional[str]:
        """Extract and clean number from text"""
        # First try field patterns
        result = self.extract_field_and_number(text)
        if result:
            return result[1]
        
        # First convert Bengali digits
        text = self.convert_bengali_to_english(text)
        
        # Try each number pattern
        for pattern in self.number_patterns:
            match = re.search(pattern, text)
            if match:
                # Clean the extracted number
                number = match.group(0) if match.group(0) else match.group(1)
                # Remove all non-digit characters
                clean_number = re.sub(r'[^\d]', '', number)
                if clean_number:
                    return clean_number
        
        # Fallback: extract all digits from the text
        all_digits = re.findall(r'\d+', text)
        if all_digits:
            return ''.join(all_digits)
        
        return None
    
    def normalize_line(self, line: str) -> Optional[Tuple[str, str]]:
        """Normalize a complete line to (field_name, value) tuple"""
        # Clean the line
        line = line.strip()
        if not line:
            return None
        
        # Try to extract field and number directly
        result = self.extract_field_and_number(line)
        if result:
            return result
        
        # Fallback: Find field name and extract number separately
        field_name = self.normalize_field_name(line)
        if not field_name:
            return None
        
        # Extract number
        number = self.extract_number(line)
        if not number:
            return None
        
        return (field_name, number)
    
    def normalize_text(self, text: str) -> Dict[str, str]:
        """Normalize entire text and return dictionary of field:value pairs"""
        results = {}
        lines = text.split('\n')
        
        for line in lines:
            normalized = self.normalize_line(line)
            if normalized:
                field_name, value = normalized
                results[field_name] = value
        
        return results
    
    def replace_numbers_with_words(self, text: str) -> str:
        """Replace numbers in text with Bengali words"""
        result_text = text

        # print("number service:", result_text)
        
        # Process each line
        lines = text.split('\n')
        processed_lines = []
        # print("Processing lines for number to words conversion:")
        # print(lines)
        
        for line in lines:
            processed_line = line
            # Try to extract field and number
            extraction = self.extract_field_and_number(line)

            # print("extration : ", extraction)

            if extraction:
                field_name, number = extraction

                # print(f"Field: {field_name}, Number: {number}")
                # Convert number to words
                words = self.number_to_words(number)

                # print("words : ", words)
                
                # Find the number pattern in the line and replace with words
                # for pattern, _ in self.field_patterns:
                #     match = re.search(pattern, line)
                #     print("match : ", match)
                #     # if match and len(match.groups()) >= 3 and match.group(3):
                #     if match is not None:
                #         print("if condition:", match.group(3))
                #         # Replace the number part with words
                # original_number = match.group(3).strip()
                #         print("original_number : ", original_number)
                processed_line = line.replace(number, words)
                        # break
            
            processed_lines.append(processed_line)
        
        return '\n'.join(processed_lines)


# Example usage
if __name__ == "__main__":
    service = NumberNormalizationService()
    
    # Test data
    test_text = """
    একাউন্ট নম্বর ১২৩৪৫৬৬
    account number 1234567890
    রিসিপ্ট  নম্বর 123452
    ricipt number 123456677989
    রশিদ  নম্বর 8904390
    ট্রানজেকশন নাম্বার 893023
    transcrition number 12338902983
    শ্লিপ নম্বর 1234567890123
    cilip number 1234567890123
    card number 1234567890123
    token id number 1234567890123
    টোকেন নম্বর  ৪৫৬৭৮০৩৪৫
    বিল নম্বর  ৪৫৬৭৮০৩৪৫ hello how are you
    bill number 456780345
    চালান নম্বর  ৪৫৬৭৮০৩৪৫
    invoice number 456780345
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
    "Havit HV-SC055 Laptop Cleaning Kit - HV-SC055 and the number is the 12345"
    """

    # test_text = """
    # আপনার ইনভয়েস নম্বর ১২৩৪৫৬৭৮৯০১২ বৈধ।
    # আপনার টোকেন নম্বর ৫৬৭৮৯০১২৩৪ দিয়ে লগইন করুন।
    # নতুন Token নং: ৯৮৭-৬৫৪-৩২১ জেনারেট করা হয়েছে।
    # Security token ID number 123456789012 expires at midnight.
    # আপনার টোকেন নম্বর ৫৬৭৮৯০১২৩৪ দিয়ে লগইন করুন।
    # আজকের লেনদেন নং: ৭৮৯০১২৩৪৫৬ সফল হয়েছে।
        # গ্রাহকের A/C নং: ৯৮৭৬৫৪৩২১০ এ জমা করুন।
    # "গ্রাহকের A/C নং: ৯৮৭৬৫৪৩২১০ এ জমা করুন।",
    # """

    """
    this type of patter solved by product number
    Use reference number REF-123-456-789 for all correspondence.
    Your tracking number TRK-123-456-789-012 shows delivery tomorrow.
    
    """

    test_text = """

    "পেমেন্ট আইডি ১২৩৪৫৬৭৮৯০১২ নিশ্চিত হয়েছে BDT ১০,০০০ এর জন্য।",

    """
    
    # Process the text
    for text in test_text.split('\n'):
        text = text.strip()
        if text:
            print("Input: ", text)
            # normalized = service.normalize_text(text)
            # print("Normalized: ", normalized)
            replaced = service.replace_numbers_with_words(text)
            print("Replaced with words: ", replaced)
            print("-" * 40)
