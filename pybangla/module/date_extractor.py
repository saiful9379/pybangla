import re


class DateExtractor:
    """
    Extracts English or Bangla date from string.

    Args:
        sentence (str): The input string.

    Returns:
        list: A list containing all the dates found in the sentence.
    """

    @staticmethod
    def get_regex_patterns():
        en_month_name = [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "june",
            "july",
            "aug",
            "sept",
            "oct",
            "nov",
            "dec",
        ]
        bn_month_name = [
            "জানুয়ারি",
            "ফেব্রুয়ারি",
            "মার্চ",
            "এপ্রিল",
            "মে",
            "জুন",
            "জুলাই",
            "অগাস্ট",
            "আগস্ট",
            "সেপ্টেম্বর",
            "অক্টোবর",
            "নভেম্বর",
            "ডিসেম্বর",
        ]

        en_dd_mm_yy = "\\d{1,4}(( )+)?[-\\/,.;: ](( )+)?\\d{1,4}(( )+)?[-\\/,.;: ](( )+)?\\d{1,4}\\b"
        en_number_month_year = (
            "\\d{1,2}[-\\/,.;: ](( )+)?("
            + "|".join(en_month_name)
            + ")[a-z]{0,6}((( )+)?[-\\/,.;: ](( )+)?\\d{1,4})?\\b"
        )
        en_month_number_year = (
            "("
            + "|".join(en_month_name)
            + ")[a-z]{0,6}(( )+)?[-\\/,.;: ](( )+)?\\d{1,2}([-\\/,.;: ](( )+)?\\d{1,4})?\\b"
        )
        en_month_year = (
            "("
            + "|".join(en_month_name)
            + ")[a-z]{0,6}(( )+)?[-\\/,.;: ](( )+)?\\d{1,4}\\b"
        )
        # en_plain_date ='\\d{8}\\b'

        bn_dd_mm_yy = "[০-৯]{1,4}(( )+)?[-\\/,.;: ](( )+)?[০-৯]{1,4}(( )+)?[-\\/,.;: ](( )+)?[০-৯]{1,4}"
        bn_number_month_year = (
            "[০-৯]{1,2}[-\\/,.;: ](( )+)?("
            + "|".join(bn_month_name)
            + ")((( )+)?[-\\/,.;: ](( )+)?[০-৯]{1,4})?"
        )
        bn_month_number_year = (
            "("
            + "|".join(bn_month_name)
            + ")(( )+)?[-\\/,.;: ][০-৯]{1,2}(?![০-৯])((( )+)?[-\\/,.;: ](( )+)?[০-৯]{1,4})?"
        )
        bn_month_year = (
            "(" + "|".join(bn_month_name) + ")(( )+)?[-\\/,.;: ](( )+)?[০-৯]{1,4}"
        )
        bn_year_date_num_month_name = (
            "[০-৯]{1,4}(( )+)?[-\\/,.;: ](( )+)?(সালে|সালের)(( )+)?[-\\/,.;: ]?[০-৯]{1,2}(( )+)?[-\\/,.;: ]?(( )+)?("
            + "|".join(bn_month_name)
            + ")?"
        )
        # bn_plain_date = "[০-৯]{8}"

        en_regex = "|".join(
            [en_dd_mm_yy, en_number_month_year, en_month_number_year, en_month_year]
        )  # , en_plain_date])
        bn_regex = "|".join(
            [
                bn_dd_mm_yy,
                bn_number_month_year,
                bn_month_number_year,
                bn_month_year,
                bn_year_date_num_month_name,
            ]
        )  # , bn_plain_date])
        combined_regex = en_regex + "|" + bn_regex
        return combined_regex

    def __init__(self) -> None:
        self.date_regex = self.get_regex_patterns()

    def get_dates(self, sentence):
        dates = re.finditer(self.date_regex, sentence, re.IGNORECASE)
        return [date.group() for date in dates]


if __name__ == "__main__":

    English_sentences = [
        "I'm planning a beach vacation in July 2023.",
        "The conference is scheduled for September 05, 2023.",
        "We'll have a family gathering on December 25, 2023, for Christmas.",
        "My sister's wedding is on March 18, 2023.",
        "I'm looking forward to my birthday on August 12, 2023.",
        "Let's go skiing in February 2023.",
        "Our company picnic is set for June 30, 2023.",
        "I have an important exam on May 10, 2023.",
        "The new semester starts in January 2023.",
        "We're planning a road trip in April 2023.",
        "I'll be moving to a new apartment in October 2023.",
        "Mark your calendar for November 05, 2023, it's Diwali.",
        "I'm excited for the summer camp in July 2023.",
        "The concert tickets for March 25, 2023, are selling fast.",
        "Let's have a barbecue party in August 2023.",
        "I'll be visiting my grandparents in May 2023.",
        "I'm attending a wedding in September 2023.",
        "We're planning a trip to Europe in June 2023.",
        "I have a doctor's appointment on April 10, 2023.",
        "The company's annual meeting is in February 2023.",
        "We're celebrating Valentine's Day on February 14, 2023.",
        "My graduation ceremony is on June 15, 2023.",
        "I'm starting a new job in March 2023.",
        "I'm planning to go hiking in the mountains in May 2023.",
        "The school play is scheduled for November 2023.",
        "Let's go pumpkin picking in October 2023.",
        "I have a dentist appointment in January 2023.",
        "The summer festival is in July 2023.",
        "We're hosting a Thanksgiving dinner in November 2023.",
        "I'm going to a music festival in April 2023.",
    ]
    template_provided = [
        "০১-এপ্রিল/২০২৩",
        "১ এপ্রিল ২০২৩",
        "2023-04-05 df",
        "06-04-2023 df",
        "04/01/2023 er",
        "07 April, 2023 er",
        "Apr 1, 2023 er",
        "2023/04/01 er",
        "01-Apr-2023 erv",
        "01-Apr/2023 sere",
        # "20230401 ",
        # "20042024 ",
    ]
    Bangla_sentences = [
        "১৯৯৬ সালের ৬তারিখে নির্ধারিত করা হয়েছে.",
        "১৯৯৬ সালের৬ সেপ্টেম্বর ভ্রমণ পরিকল্পনা করছি.",
        "আমি জুলাই ২০২৩ তে একটি সমুদ্র ভ্রমণ পরিকল্পনা করছি.",
        "সম্মেলনটি সেপ্টেম্বর ০৫ ২০২৩ তারিখে নির্ধারিত করা হয়েছে.",
        "আমরা খ্রীষ্টমাসের জন্য ডিসেম্বর ২৫ ২০২৩ তারিখে পরিবারের সংগঠন করব.",
        "আমার বোনের বিয়ে ১৮ মার্চ, ২০২৩ তারিখে.",
        "আমি আগামী ১২ আগস্ট, ২০২৩ তারিখে আমার জন্মদিনে দেখা করছি.",
        "আমরা ফেব্রুয়ারি ২০২৩ তে স্কিউইং যাব.",
        "আমাদের কোম্পানির পিকনিকটি জুন ৩০ ২০২৩ তারিখে নির্ধারিত হয়েছে.",
        "আমার গুরুত্বপূর্ণ পরীক্ষা ১০ মে, ২০২৩ তারিখে.",
        "নতুন সেমিস্টার শুরু হয় জানুয়ারি ২০২৩ তারিখে.",
        "আমরা এপ্রিল ২০২৩ তে একটি রোড ট্রিপ পরিকল্পনা করছি.",
        "আমি অক্টোবর ২০২৩ তারিখে একটি নতুন অ্যাপার্টমেন্টে যাচ্ছি.",
        "আপনার ক্যালেন্ডারের মার্ক নভেম্বর ০৫, ২০২৩, এটি দীপাবলি.",
        "আমি জুলাই ২০২৩ তারিখে গরম শিবিরের জন্য উৎসাহিত.",
        "মার্চ ২৫, ২০২৩ তারিখের কনসার্ট টিকেটগুলি দ্রুত বিক্রয় হচ্ছে.",
        "আগস্ট ২০২৩ তারিখে একটি বারবিকিউ পার্টি আয়োজন করা হবে.",
        "আমি মে ২০২৩ তারিখে আমার নানা-নানির কাছে যাচ্ছি.",
        "আমি সেপ্টেম্বর ২০২৩ তারিখে একটি বিয়ে অনুষ্ঠানে যাচ্ছি.",
        "আমরা জুন ২০২৩ তে ইউরোপে একটি ভ্রমণ পরিকল্পনা করছি.",
        "আমার ডেন্টিস্টের অ্যাপয়েন্টমেন্ট এপ্রিল ১০, ২০২৩ তারিখে.",
        "কোম্পানির বার্ষিক সভা ফেব্রুয়ারি ২০২৩ তারিখে হয়.",
        "আমার অনুষ্ঠান সমাপন হয়েছে জুন ১৫, ২০২৩ তারিখে.",
        "আমি মার্চ ২০২৩ তারিখে একটি নতুন চাকরি শুরু করছি.",
        "আমি মে ২০২৩ তারিখে পাহাড়ে ট্রেকিং করতে যাচ্ছি.",
        "বিদ্যালয়ের নাটকটি নভেম্বর ২০২৩ তারিখে নির্ধারিত হয়েছে.",
        "আমরা অক্টোবর ২০২৩ তার",
        "১৯৯৬ সালের ৬ সেপ্টেম্বর",
    ]

    combined_sentences = English_sentences + template_provided + Bangla_sentences
    date_extractor = DateExtractor()

    for sentence in combined_sentences:
        dates = date_extractor.get_dates(sentence)
        print(f"Input: {sentence}: Output: {dates}")

    # print(f"Input: {sentence}: Output: {[date.group() for date in dates]}")
