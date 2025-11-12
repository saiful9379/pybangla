import re
from typing import List, Tuple, Dict



email_replace_unit = {
    "." : {"en":"dot", "bn": "ডট"},
    "@": {"en":"at the rate", "bn": "অ্যাট দ্য রেট"},
    ":": {"en":"colon", "bn": "কলন"},
    "/": {"en":"slash", "bn": "স্ল্যাশ"}
    }

url_replace_unit = {
        'http://': {"bn": "এইচ, টি, টি, পি কোলন স্ল্যাশ, স্ল্যাশ", "en": "http clone slash slash"},
        'https://': {"bn": "এইচ, টি, টি, পি, এস কোলন স্ল্যাশ, স্ল্যাশ", "en": "https clone slash slash"},
        'www.': {"bn": "ডব্লিউ, ডব্লিউ, ডব্লিউ, ডট", "en": "www dot"},
        '.com': {"bn": "ডট কম", "en": "dot com"},
        '.org': {"bn": "ডট org", "en": "dot org"},
        '.net': {"bn": "ডট নেট", "en": "dot net"},
        '.edu': {"bn": "ডট edu", "en": "dot edu"},
        '.gov': {"bn": "ডট গভ", "en": "dot gov"},
        '.bd': {"bn": "ডট বিডি", "en": "dot bd"},
        '/': {"bn": "স্ল্যাশ", "en": "slash"},
        '-': {"bn": "ড্যাশ", "en": "dash"},
        '_': {"bn": "আন্ডারস্কোর", "en": "underscore"},
        '@': {"bn": "অ্যাট", "en": "at"},
        '.': {"bn": "ডট", "en": "dot"},
        ':': {"bn": "কোলন", "en": "colon"},
        "=" :{"bn": "একুয়াল", "en": "equals"},
        "?": {"bn": "কোয়েশ্চেন মার্ক", "en": "question mark"},
        "&": {"bn": "এন্ড", "en": "and"},
        "%": {"bn": "পারসেন্ট", "en": "percent"},
        "#": {"bn": "হ্যাশ", "en": "hash"},
    }

bn_number_map = {
    '0': 'জিরো', '1': 'ওয়ান', '2': 'টু', '3': 'থ্রি', '4': 'ফোর',
    '5': 'ফাইভ', '6': 'সিক্স', '7': 'সেভেন', '8': 'এইট', '9': 'নাইন',
    '০': 'শূন্য', '১': 'এক', '২': 'দুই', '৩': 'তিন', '৪': 'চার',
    '৫': 'পাঁচ', '৬': 'ছয়', '৭': 'সাত', '৮': 'আট', '৯': 'নয়'
}

en_number_map = {
    '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
    '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
}

class EmailURLExtractor:
    def __init__(self):
        # Email regex pattern
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        
        # URL regex pattern (handles http, https, ftp, and www)
        self.url_pattern = re.compile(
            r'(?:(?:https?|ftp):\/\/)?'  # Optional protocol
            r'(?:www\.)?'  # Optional www
            r'(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+' # Domain
            r'[A-Za-z]{2,}'  # Top-level domain
            r'(?::[0-9]{1,5})?'  # Optional port
            r'(?:\/[^\s]*)?'  # Optional path
        )

    def normalize_url(self, url: str, lang="bn") -> str:
        """Normalize URL for better pronunciation."""
        normalized = url

        # Replace URL components
        for component, replacement in url_replace_unit.items():
            # print("component : ", component, " replacement : ", replacement)
            normalized = normalized.replace(component, f" {replacement[lang]} ")

        # Clean up extra spaces
        normalized = ' '.join(normalized.split())

        return normalized.strip()

    def replace_numbers(self, normalized_url: str, lang="bn") -> str:
        number_matchs = re.findall(r'\d+', normalized_url)
        # print("number_match : ", number_matchs)
        
        if number_matchs:
            for number_match in number_matchs:
                number_str = number_match
                # number_str = number_match.group()
                if lang == "bn":
                    normalized_number = ' '.join(bn_number_map.get(digit, digit) for digit in number_str)
                else:
                    normalized_number = ' '.join(en_number_map.get(digit, digit) for digit in number_str)
                normalized_url = normalized_url.replace(number_str, " "+normalized_number+" ")
        # Replace the original number string with the normalized version
        return normalized_url

    def extract_emails(self, text: str, lang="bn") -> str:
        # Replace URL components
        for component, replacement in url_replace_unit.items():
            normalized = normalized.replace(component, replacement)
        
        # Clean up extra spaces
        normalized = ' '.join(normalized.split())
        
        return normalized.strip()

    def email_normalization(self, text: str, lang="bn") -> str:
        """Extract all email addresses from the text and replace them with normalized versions."""
        
        # Extract emails with their spans using finditer instead of findall
        email_matches = []
        for match in self.email_pattern.finditer(text):
            email_matches.append({
                'email': match.group(),
                'span': match.span(),  # (start, end) positions
                'start': match.start(),
                'end': match.end()
            })
        
        # print("Extracted emails with spans: ", [(m['email'], m['span']) for m in email_matches])
        
        # Sort matches in reverse order by start position to avoid position shifts during replacement
        email_matches.sort(key=lambda x: x['start'], reverse=True)
        
        # Process and replace each email
        for match in email_matches:
            email = match['email']
            start = match['start']
            end = match['end']
            
            # Normalize email for pronunciation
            normalized_email = email
            for char, replacement in email_replace_unit.items():
                if char in normalized_email:
                    normalized_email = normalized_email.replace(char, f" {replacement[lang]} ")
            
            normalized_email = normalized_email.strip()
            # print(f"Normalizing: {email} -> {normalized_email}")

            normalized_email = self.replace_numbers(normalized_email, lang)

            # Replace in text using span
            text = text[:start] +" "+normalized_email+" "+ text[end:]

        return text

    def url_normalization(self, text: str, lang="bn") -> str:
        """Extract all URLs from the text and replace them with normalized versions."""
        
        # Extract URLs with their spans using finditer
        url_matches = []
        for match in self.url_pattern.finditer(text):
            url_matches.append({
                'url': match.group(),
                'span': match.span(),
                'start': match.start(),
                'end': match.end()
            })
        
        # print("Extracted URLs with spans: ", [(m['url'], m['span']) for m in url_matches])
        
        # Sort matches in reverse order by start position
        url_matches.sort(key=lambda x: x['start'], reverse=True)
        
        # Process and replace each URL
        for match in url_matches:
            url = match['url']
            start = match['start']
            end = match['end']
            # Normalize URL for pronunciation
            normalized_url = self.normalize_url(url, lang)
            # print(f"Normalizing URL: {url} -> {normalized_url}")

            # extract number from url and replace with words
            normalized_url = self.replace_numbers(normalized_url, lang)

            # Replace in text using span
            text = text[:start] + normalized_url + text[end:]
        return text



# Example usage
if __name__ == "__main__":
    # Test sentences
    test_texts = [
        "Contact us at info@example.com or visit https://www.example.com",
        "Send email to john.doe@company.org and check www.company.org/about",
        "Multiple contacts: sales@site.com, support@site.co.uk, marketing@site.net",
        "Visit http://github.com/user/repo or ftp://files.server.com",
        "My email is test.user+tag@gmail.com and website is example.io",
        "Check out https://subdomain.example.com:8080/path/to/page?query=1"
    ]
    
    # Using the class
    # print("Using EmailURLExtractor class:")
    # print("-" * 50)
    lang = "bn"
    extractor = EmailURLExtractor()
    for text in test_texts:
        print(f"\nText: {text}")
        text = extractor.email_normalization(text, lang=lang)
        text = extractor.url_normalization(text, lang=lang)

        print(f"output text : {text}")
        print("----------------------")
        # print(f"URLs: {urls}")