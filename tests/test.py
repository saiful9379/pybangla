import pybangla
nrml = pybangla.Normalizer()


# Test both approaches
sentences = [
    "বাংলা নম্বর হিসেবে পাসপোর্ট নম্বর এ০১২৩৪৫৬৭ ও ই১২৩৪৫৬৭৮।",
    "পাসপোর্ট নম্বর এ০১২৩৪৫৬৭ ও ই১২৩৪৫৬৭৮।",
    "পাসপোর্ট নম্বর এ০১২৩৪৫৬৭, ই১২৩৪৫৬৭৮, এ০১২৩৪৫৬৭, এ০১২৩৪৫৬৭।",
    "পাসপোর্ট নম্বর এ০১২৩৪৫৬৭, account number : ই১২৩৪৫৬৭৮, এ০১২৩৪৫৬৭, এ০১২৩৪৫৬৭।",
    "আমার পাসপোর্ট নং এ১২৩৪৫৬৭৮ এবং আমার স্ত্রীর পাসপোর্ট নং বি৯৮৭৬৫৪৩২১।"
]

for sentence in sentences:

  normalized_text = nrml.text_normalizer(sentence, all_operation=True)
  print("normalized_text : ", normalized_text)
    