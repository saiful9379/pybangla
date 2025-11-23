import re


class UnitNormalization:
    def __init__(self):
        self.pattern = r"(\d+(?:\.\d+)?)\s?(sq\s?ft|sqft|ml|g|gm|kg|lb|l|cm|ft|tb|gb|kb)\b"

    # Unit conversion with plural handling
    def get_unit_full_form(self, quantity, unit_abbr):
        print([quantity, unit_abbr])
        unit_abbr = unit_abbr.lower()

        unit_names = {
            "en": {
                "ml": "milliliter",
                "g": "gram",
                "gm": "gram",
                "kg": "kilogram",
                "lb": "pound",
                "l": "liter",
                "cm": "centimeter",
                "tb": "terabyte",
                "gb": "gigabyte",
                "kb": "kilobyte",
                },
            "bn": {
                "ml": "মিলিলিটার",
                "g": "গ্রাম",
                "gm": "গ্রাম",
                "kg": "কেজি",
                "lb": "পাউন্ড",
                "l": "লিটার",
                "cm": "সেন্টিমিটার",
                "ft": "ফিট",
                "sqft": "স্কোয়ার ফিট",
                "sq ft": "স্কোয়ার ফিট",
                "tb": "টেরাবাইট",
                "gb": "গিগাবাইট",
                "kb": "কিলোবাইট",
            }
        }
        # Choose language based on unit_abbr
        language = "bn"
        
        if language == "bn":
            full_form = unit_names["bn"].get(unit_abbr, unit_abbr)
            
        elif language == "en":
            full_form = unit_names["en"].get(unit_abbr, unit_abbr)
            # Add 's' for plural if quantity is not 1
            if float(quantity) != 1:
                full_form += "s"
        print(full_form)
        return full_form

    def unit_processing(self, text):
        # Find all matches
        matches = []
        for match in re.finditer(self.pattern, text, re.IGNORECASE):
            quantity = match.group(1)
            unit_abbr = match.group(2)
            full_form = self.get_unit_full_form(quantity, unit_abbr)

            matches.append(
                {
                    "start": match.start(),
                    "end": match.end(),
                    "original": match.group(0),
                    "replacement": f"{quantity} {full_form}",
                }
            )
        # Replace from right to left to maintain positions
        modified_text = text
        for match in reversed(matches):
            modified_text = (
                modified_text[: match["start"]]
                + match["replacement"]
                + modified_text[match["end"] :]
            )
        return modified_text


if __name__ == "__main__":
    un = UnitNormalization()
    # Example usage
    text = " clean & clear face wash 50gb - 123456789"
    modified_text = un.unit_processing(text)
    print("Original text:")
    print(text)
    print("\nModified text:")
    print(modified_text)
