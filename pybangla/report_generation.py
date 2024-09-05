import pandas as pd
import time
import csv
import difflib

import time
from module.main import Normalizer

nrml = Normalizer()


def read_test_file(file_path, lj_speach=True):
    """
    read txt file
    """
    with open(file_path, "r") as file:
        # Read all lines from the file
        data = [i for i in file.read().split("\n") if i]

    if lj_speach:
        data_list = []
        for i in data:
            audio, text = i.split("|")[0], i.split("|")[1:]
            data_list.append((" ".join(text)).strip())
    else:
        data_list = data
    return data_list


def read_excel_file(file_path, sheet_names):

    # Read the specified sheets from the Excel file
    sheets = pd.read_excel(file_path, sheet_name=sheet_names)

    # If you need the DataFrames in a list instead of a dictionary
    sheets_list = [sheets[sheet] for sheet in sheet_names]

    # Display the DataFrames
    text_list = []
    for i, df in enumerate(sheets_list):
        df_filled = df.fillna("")
        # print(f"\nData from {sheet_names[i]}:")
        texts = df_filled.Sentences.tolist()
        text_list.extend(texts)
    text_list = [i for i in text_list if i]
    return text_list


def csv_log_generation(data, header, output_path="report/pybangla_report_csv.csv"):
    with open(output_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header row
        writer.writerows(data)  # Write the data rows`


def find_changes(string1, string2):
    # Split the strings into words
    words1, words2 = string1.split(), string2.split()
    # Use difflib to find differences
    diff = difflib.ndiff(words1, words2)
    added_chunk, added_chunks, removed_chunk, removed_chunks = [], [], [], []
    for change in diff:
        if change.startswith("+ "):
            added_chunk.append(change[2:])
            if removed_chunk:
                removed_chunks.append(" ".join(removed_chunk))
                removed_chunk = []
        elif change.startswith("- "):
            removed_chunk.append(change[2:])
            if added_chunk:
                added_chunks.append(" ".join(added_chunk))
                added_chunk = []
        else:
            if added_chunk:
                added_chunks.append(" ".join(added_chunk))
                added_chunk = []
            if removed_chunk:
                removed_chunks.append(" ".join(removed_chunk))
                removed_chunk = []
    # Append any remaining chunks
    if added_chunk:
        added_chunks.append(" ".join(added_chunk))
    if removed_chunk:
        removed_chunks.append(" ".join(removed_chunk))

    return removed_chunks, added_chunks


# # Example usage
# string1 = "উদাহরণস্বরূপ, আপনার মোটরযানের রেজিস্ট্রেশন নাম্বার ঢাকা মেট্রো-গ-12-1212 এবং টাকা জমা রশিদের ট্রানজেকশন নাম্বার 2001011325989"
# string2 = "উদাহরণস্বরূপ, আপনার মোটরযানের রেজিস্ট্রেশন নাম্বার ঢাকা মেট্রো গ-বারো-বারোবারো এবং টাকা জমা রশিদের ট্রানজেকশন নাম্বার দুই লক্ষ এক শত এক কোটি তেরো লক্ষ পঁচিশ হাজার নয় শত ঊননব্বই"

# string1= "৬/৯/১৯৯৬ বাংলাদেশের পাসপোর্টের অভ্যন্তরে ইস্যু করানোর সময় 10/12/24"
# string2 = "ছয় সেপ্টেম্বর উনিশশো ছিয়ানব্বই বাংলাদেশের পাসপোর্টের অভ্যন্তরে ইস্যু করানোর সময় দশ বারো চব্বিশ"


if __name__ == "__main__":

    # file_path = "./test_data/evaluation_data.xlsx"
    file_path = "./test_data/metadata_udoy_lj.txt"
    # sheet_names = [
    #     'saiful',
    # ]
    # texts = read_excel_file(file_path, sheet_names)
    texts = read_test_file(file_path)
    # print(len(texts))

    index = 0
    s_time = time.time()
    header = ["Input_Text", "Process_Text", "Status", "Before Replace", "After Replace"]
    process_list = []
    for text in texts:
        print("input  : ", index, text)
        p_text = nrml.text_normalizer(text)
        print("process text : ", p_text)
        removed_chunks, added_chunks = find_changes(text, p_text)
        # Output the results
        print(f"Removed chunks: {removed_chunks}")
        print(f"Added chunks: {added_chunks}")
        process_list.append(
            [text, p_text, text == p_text, removed_chunks, added_chunks]
        )
        index += 1
    print("time : ", time.time() - s_time)
    csv_log_generation(process_list, header)
