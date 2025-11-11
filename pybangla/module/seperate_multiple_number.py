import re

def extract_consecutive_numbers_with_separators(text):
    """Extract consecutive numbers separated by spaces and/or hyphens"""
    # Pattern for Bengali consecutive numbers with spaces or hyphens
    bengali_pattern = r'[০-৯]+(?:[\s\-]+[০-৯]+)+'
    # Pattern for English consecutive numbers with spaces or hyphens  
    english_pattern = r'\d+(?:[\s\-]+\d+)+'
    # Combined pattern
    combined_pattern = f'({bengali_pattern})|({english_pattern})'
    matches = []
    for match in re.finditer(combined_pattern, text):
        matched_text = match.group(0)
        # Extract individual numbers (remove spaces and hyphens)
        if re.match(r'[০-৯]', matched_text):  # Bengali
            numbers = re.findall(r'[০-৯]+', matched_text)
            num_type = 'bengali'
        else:  # English
            numbers = re.findall(r'\d+', matched_text)
            num_type = 'english'
        matches.append({
            'text': matched_text,
            'start': match.start(),
            'end': match.end(),
            'span': match.span(),
            'count': len(numbers),
            'numbers': numbers,
            'type': num_type,
            'has_hyphen': '-' in matched_text,
            'separators': 'mixed' if '-' in matched_text and ' ' in matched_text else 'hyphen' if '-' in matched_text else 'space'
        })
    
    return matches

# Example usage
if __name__ == "__main__":
    test_text = """
    my phone number if ০১৭১৩৭২৭৩২৪
    # Phone numbers: ০১৭১৩ ৭২৭ ৩২৪
    # Mixed separators: ০১৭১৩ -৭২৭- ৩২৪
    # Multiple numbers: ৫৫১০ ৫৫ ৫৫১০ ৫৫১০ ৫৫ ৫৫১০
    # Single number: ৫৫১০
    # English: 123 456 789
    # English with hyphen: 123-456-789
    # Mixed: 123 -456- 789
    # Two numbers only: ১২৩ ৪৫৬
    # Four numbers: ১০০ ২০০ ৩০০ ৪০০
    আপনি বলেছেন: ০১৬৭৩ [পজ] ১ ১ ০ [পজ] ৭ ২ ০ তাহলে আপনার পুরো নম্বরটি হচ্ছে:
    """

    # test_text = """my phone number if ৫৫১০"""
    # Extract all patterns
    matches = extract_consecutive_numbers_with_separators(test_text)
    print("Found consecutive number patterns:")
    for match in matches:
        print(f"\nPattern: '{match['text']}'")
        print(f"Position: {match['span']}")
        print(f"Type: {match['type']}")
        print(f"Count: {match['count']} numbers")
        print(f"Numbers: {match['numbers']}")
        print(f"Separator type: {match['separators']}")