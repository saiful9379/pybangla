import re
from typing import List, Tuple, Dict



replace_unit = {
    "." : "dot",
    "@": "at the rate",
    ":": "clone",
    "/": "slash"
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
    
    def extract_emails(self, text: str) -> List[str]:
        """Extract all email addresses from the text."""
        return self.email_pattern.findall(text)
    
    def extract_urls(self, text: str) -> List[str]:
        """Extract all URLs from the text."""
        urls = self.url_pattern.findall(text)
        # Filter out email domains that might be caught as URLs
        return [url for url in urls if '@' not in url]
    

# Simple function-based approach
def extract_emails(text: str) -> Tuple[List[str]]:
    """
    Extract emails and URLs from text.
    Returns a tuple of (emails, urls)
    """
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    
    return emails

def extract_url(text):

                                       # URL pattern
    url_pattern = (
        r'(?:(?:https?|ftp):\/\/)?'  # Optional protocol
        r'(?:www\.)?'  # Optional www
        r'(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+' # Domain
        r'[A-Za-z]{2,}'  # Top-level domain
        r'(?::[0-9]{1,5})?'  # Optional port
        r'(?:\/[^\s]*)?'  # Optional path
    )

    urls = re.findall(url_pattern, text)
    
    # Filter out email domains from URLs
    urls = [url for url in urls if '@' not in url]
                                       
    return urls

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
    extractor = EmailURLExtractor()
    for text in test_texts:
        print(f"\nText: {text}")
        emails = extractor.extract_emails(text)
        print(f"Emails: {emails}")
        # print(f"URLs: {urls}")