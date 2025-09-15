import os
import json
import re
try:
    from .config import Config as cfg
except ImportError:
    from config import Config as cfg
base_path = os.path.dirname(os.path.abspath(__file__))


class SymbolNormalizer:
    def __init__(self):
        self.symbols_path = os.path.join(base_path, "db", "symbols_mapping.json")
        self.symbols_db = self.load_json()
        self.pattern = self.get_pattern()

    def load_json(self):
        """
        Load the digit and special character mapping from JSON file.

        Returns:
            dict: Data mapping for digits and special characters.
        """
        with open(self.symbols_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data
    
    def get_symbols_db(self):
        """
        Returns the symbols database for external use.

        Returns:
            dict: The symbols database.
        """
        return self.symbols_db

    def get_pattern(self):
        """
        Create a regex pattern to match all keys in the symbols database.

        Returns:
            re.Pattern: A compiled regex pattern for all symbols.
        """
        return re.compile('|'.join(re.escape(key) for key in self.symbols_db.keys()))

    def replace_match(self, match, lang):
        """
        Helper function to replace matched symbols with their translations.

        Args:
            match (re.Match): The matched object for a symbol.
            language (str): The target language ('en', 'bn', or 'ja').

        Returns:
            str: Translated text for the matched symbol.
        """
        symbol = match.group(0)
        return self.symbols_db.get(symbol, {}).get(lang, symbol)

    def sym_normalize(self, input_string, lang="bn"):
        """
        Replaces symbols in the input string with their translations in the specified language.

        Args:
            input_string (str): The string containing symbols to be replaced.
            language (str): The target language ('en', 'bn', or 'ja').

        Returns:
            str: The string with symbols replaced by their translations.
        """
        if lang not in ['en', 'bn', 'ja', 'ja_hiragana', 'ja_katakana', 'romaji']:
            raise ValueError("Language must be 'en', 'bn', 'ja', 'ja_hiragana', 'ja_katakana', or 'romaji'.")
        
        # print("inside sym_normalize : ", input_string, lang)
        # print(self.pattern.sub(lambda match: self.replace_match(match, lang), input_string))
        # Use a lambda to pass the language argument to replace_match
        input_string = self.pattern.sub(lambda match: self.replace_match(match, lang), input_string)
        
                # print("text : ", text)
        input_string = re.sub(cfg._whitespace_re, " ", input_string)
    
        input_string = re.sub(r"\s*,\s*", ", ", input_string)
        return input_string


if __name__ == "__main__":
    converter = SymbolNormalizer()

    lang = "romaji" # "en|ja_hiragana|ja_katakana|romaji"

    # Example usage
    examples = [
        {"input_text": "I have ¥100 and €50.", "language": "ja"},
        {"input_text": "The temperature is 25° today.", "language": "en"},
        {"input_text": "Bitcoin price is now ₿50000.", "language": "bn"},
        {"input_text": "This item costs $20 or £15.", "language": "ja"},
        {"input_text": "Add 50% to the amount.", "language": "bn"},
        {"input_text": "今日の気温は25°です。", "language": "en"},
        {"input_text": "আমি ¥100 এবং €50 আছে।", "language": "en"},
        {"input_text": "I earned $200 today.", "language": "ja"},
        {"input_text": "আমার কাছে $500 এবং ₹1000 আছে।", "language": "ja"},
        {"input_text": "今日は¥1000と€200を持っています。", "language": "bn"},
        {"input_text": "システィナ礼拝堂は、１４７３年に、バティカン宮殿内に建立された、壮大な礼拝堂です。", "language": "bn"},

    ]

    for example in examples:
        input_text = example["input_text"]
        # language = example["language"]
        output_text = converter.sym_normalize(input_text, lang)
        print(f"Input: {input_text}\nLanguage: {lang}\nOutput: {output_text}\n")

