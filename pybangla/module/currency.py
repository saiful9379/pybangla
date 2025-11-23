# -*- coding: utf-8 -*-
import re
from typing import Dict, List, Tuple

# =========================
# 1) Currency dictionaries
# =========================


# -------------------------
# Currency dictionaries (minimal for extraction)
# -------------------------
CURRENCY_WORDS_BN = {
    "টাকা": "টাকা",
    "ডলার": "ডলার",
    "ইউরো": "ইউরো",
    "ইয়েন": "ইয়েন",
    "ইয়েন": "ইয়েন",
    "পাউন্ড": "পাউন্ড",
    "রুপি": "রুপি",
    "রুবেল": "রুবেল",
    "লিরা": "লিরা",
    "ওন": "ওন",
    "বাহত": "বাহত",
    "হ্রিভনিয়া": "হ্রিভনিয়া",
    "হ্রিভনিয়া": "হ্রিভনিয়া",
    "সেডি": "সেডি",
    "কলন": "কলন",
    "গুয়ারানি": "গুয়ারানি",
    "টুগরিক": "টুগরিক",
    "মানাত": "মানাত",
    "লারি": "লারি",
    "আফগানি": "আফগানি",
    "বিটকয়েন": "বিটকয়েন",
    "বিটকয়েন": "বিটকয়েন",
    "ইথের": "ইথের",
    "শেকেল": "শেকেল",
    "য্লোটি": "য্লোটি",
    "ফোরিন্ট": "ফোরিন্ট",
    "র‌্যান্ড": "র‌্যান্ড",
    "দিরহাম": "দিরহাম",
    "রিয়াল": "রিয়াল",
    "দিনার": "দিনার",
}

# -------------------------
# Currency regex parts
# -------------------------
# Symbols incl. prefixed like US$, A$, C$, S$…
_SYMS = r"(?:\b(?:US|CA|AU|SG|HK|NZ|TW|A|C|S)\$|[ACUS]?\$|€|£|¥|₩|₹|৳|₽|₺|₪|฿|₦|₫|₡|₲|₴|₵|₮|₼|₾|¢|₣|₱|₯|₠|₤|₧)"
_CODES = r"\b(?:USD|EUR|JPY|CNY|RMB|KRW|INR|BDT|PKR|NPR|GBP|AUD|CAD|NZD|HKD|SGD|CHF|SEK|NOK|DKK|RUB|TRY|PLN|CZK|HUF|ILS|MXN|BRL|ZAR|SAR|AED|QAR|OMR|KWD|BHD|TND|DZD|LYD|MAD|EGP|GEL|AZN|AFN|IRR|UAH|GHS|PYG|CRC|NGN|THB|VND)\b"
_WORDS_BN = r"(?:" + "|".join(map(re.escape, CURRENCY_WORDS_BN.keys())) + r")"
_CUR = rf"(?:{_SYMS}|{_CODES}|{_WORDS_BN})"
# Grouping spaces (space / NBSP / thin space)
_GS = r"[\u0020\u00A0\u202F]"
_MULTIPLIER = r"(?:\s*(?:[kKmM]|[tT]|(?:[bB][nN])|[bB])\b)?"
_AMOUNT = (
    r"(?:"
    # 🔥 Loose multi-comma first (very permissive): >= 2 commas anywhere
    r"\d[\d,]*,(?:[\d,]*,)+\d+(?:[.,]\d+)?"
    r"|"
    # US style: 1,234.56 / 1 234.56
    rf"\d{{1,3}}(?:[,{_GS}]\d{{3}})+(?:\.\d+)?"
    r"|"
    # Indian style: 12,34,56,789.12 / 2,00,000(.99)
    r"\d{1,2}(?:,\d{2})*,\d{3}(?:\.\d+)?"
    r"|"
    # EU style: 1.234,56 / 1 234,56
    rf"\d{{1,3}}(?:[.{_GS}]\d{{3}})+(?:,\d+)?"
    r"|"
    # Plain: 1234 / 1234.56 / 1234,56
    r"\d+(?:[.,]\d+)?"
    r")"
    rf"{_MULTIPLIER}"
)

# Currency before/after amount
CURRENCY_REGEX = re.compile(
    rf"""(?xi)
    (?:
        (?P<currency1>{_CUR})\s*(?P<amount1>{_AMOUNT})
    )
    |
    (?:
        (?P<amount2>{_AMOUNT})\s*(?P<currency2>{_CUR})
    )
    """
)


def extract_currencies(text: str) -> Tuple[str, List[Dict]]:
    """
    Returns (text_with_inline_marks, extractions)
    extractions = [{match_text, amount_raw, currency_raw, span}]
    """
    out: List[str] = []
    last = 0
    extractions: List[Dict] = []

    for m in CURRENCY_REGEX.finditer(text):
        start, end = m.span()
        out.append(text[last:start])

        cur = m.group("currency1") or m.group("currency2")
        amt = m.group("amount1") or m.group("amount2")

        out.append(f"{amt} [{cur}]")  # visualize inline; replace with your logic
        last = end

        extractions.append(
            {
                "match_text": m.group(0),
                "amount_raw": amt,
                "currency_raw": cur,
                "span": (start, end),
            }
        )

    out.append(text[last:])
    return "".join(out), extractions

def format_amount_with_multiplier(amount_str: str):
    """
    Return a localized string for amounts with multipliers, e.g.
    '5.5k' -> '5.5 থাউসেন্ড'. If no multiplier is present, return the
    original string.
    """
    if not isinstance(amount_str, str):
        amount = str(amount_str)
    else:
        amount = amount_str

    amount = amount.strip()
    if not amount:
        return amount_str

    _whitespace_chars = "\u0020\u00A0\u202F"
    m = re.match(
        rf"^(?P<num>[\d{_whitespace_chars}\.,]+)(?:\s*(?P<mult>(?:k|m|b|bn|t))\b)?\s*$",
        amount,
        re.I,
    )
    if not m:
        return amount_str

    num = m.group("num") or ""
    mult = (m.group("mult") or "").lower()

    mapping = {
        "k": "থাউজ্যান্ড",
        "m": "মিলিয়ন",
        "b": "বিলিয়ন",
        "bn": "বিলিয়ন",
        "t": "ট্রিলিয়ন",
    }

    if not mult:
        return amount_str

    word = mapping.get(mult, mult)
    # Preserve the numeric part as captured (may include commas/decimals)
    return f"{num.strip()} {word.strip()}"


# -------------------------
# Quick test
# -------------------------
if __name__ == "__main__":
    samples = [
        # আপনার দেওয়া কেস — "লম্বা + বহু কমা"
        "6,543,21,789,01,23,45678,2050.8 ইউরো",
        "6,54321,78901,23,45678,2050.8 ইউরো",
        # আরও উদাহরণ
        "Mixed: A$2,000.99 or 3,000.50€",
        "$2,00,000.99 should match; also €3.000,50 and 1\u202F234,56 EUR.",
        "INR 12,34,56,789.12 and 12,34,56,789 টাকার হিসাব।",
        "US$1234.56, CHF 1234,56 এবং 134.56 USD — সব ধরুন।",
        "৳2,50,000.00 টাকাও আছে।",
        "1,23,45678,2050.8 ইউরো",
        "ইভেন্ট আয়োজন করতে কমপক্ষে $5.5k লাগবে।",
        "ইভেন্ট আয়োজন করতে কমপক্ষে $5.5 k লাগবে।",
        "কমপক্ষে $5.5 keno লাগবে।",
        "তোমার £12M k লাগবে।",
        "জরুরী বিতরণে ফি ৮,৬২৫.৬২৫ টাকা",
        "$15.2 k এক্সাম ফী লাগবে।",
        "তার NID নম্বর 1234567890123।",
    ]
    for s in samples:
        # First extract currency matches from the full text
        norm, info = extract_currencies(s)
        for ex in info:
            if re.search(r"(?i)(?:k|m|b|bn|t)\b", str(ex.get("amount_raw", ""))):
                try:
                    localized = format_amount_with_multiplier(ex["amount_raw"])
                except Exception:
                    localized = None

                if localized is not None:
                    ex["amount_raw"] = localized

        print("IN :", s)
        print("OUT:", norm)
        print("EX :", info)
        print("-" * 80)

# # =========================
# # 6) Demo
# # =========================
# if __name__ == "__main__":
#     samples = [
#         "$100",
#         "Price is 100円 only.",
#         "Cost: 1,000.50€",
#         "We acceptA $100 or no currency.",
#         "No currency here, just 2,500 in the text.",
#         "Value is €2,500.25 guaranteed.",
#         "New total: C$1500.75.",
#         "Refund: 500 no currency symbol.",
#         "Mixed: A$2,000.99 or 3,000.50€",
#         "この商品は1,200円です。支払い金額は$1,000.50でした。",
#         "請求額はCHF 1,234,567,890.987654321です。",
#         "振込額は200.000001 SARです。",
#         "請求額は30,75 €です。",
#         "দাম €30,75 অথবা $50",
#         "দয়া করে ¥1,000〜¥2,000 সীমার মধ্যে থাকুন।",
#         "50678.90 ডলার",
#         "2050.8 ইউরো"
#     ]
#     for s in samples:
#         norm, info = get_currency_extraction(s)
#         print("IN :", s)
#         print("OUT:", norm)
#         print("EX :", info)
#         print("-"*70)
