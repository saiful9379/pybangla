import json
import time
from fuzzywuzzy import fuzz

class matching_algorithm:
    def __init__(self):
        pass

    def read_json_file(self, file_path):
        """
        read json file
        """
        with open(file_path) as f:
            data = json.load(f)
        return data
    
    def mapping_branch_en_to_bn(self, data, include_code = True):
        if include_code:
            data = {"".join(key.split("_")[-1]):value[0] for key, value in data.items()}

        else:
            data = {key:value[0] for key, value in data.items()}
        # print(data)
        return data


    # Precompute a mapping of normalized aliases to branches
    def normalized_aliases_to_branches(self, machine_key):
        """
        normalize the matching key
        """
        alias_to_branch = {}
        for branch, aliases in machine_key.items():
            # print("branch and alises : ", branch, aliases )
            for alias in aliases:
                alias_to_branch[alias.strip()] = branch
        return alias_to_branch

    def fuzzy_match(self, input_string, alias_to_branch):

        """
        key match with input text
        """
        highest_ratio = -1
        best_match = None
        # Calculate similarity only for relevant aliases based on the input text
        for alias, branch in alias_to_branch.items():
            ratio = fuzz.ratio(input_string, alias)
            # print(ratio)
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match = branch
        
        return best_match, highest_ratio


if __name__== "__main__":

    branch_db_file_path = "./actions/db/branch_db.json"

    mg = matching_algorithm()
    machine_key = mg.read_json_file(branch_db_file_path)
    alias_to_branch = mg.normalized_aliases_to_branches(machine_key)
    branch_code_with_bn_branch_name = mg.mapping_branch_en_to_bn(machine_key)

    input_text_string = [
        "আমি শাহপরান গেট শাখা  ব্রাঞ্চ থেকে চেক নিতে চাই",
        "আমি কামরাঙ্গীর চর শাখা ব্রাঞ্চ থেকে চেক নিতে চাই",
        "আমি কুমিল্লা ইপিজেড সাব-শাখা ব্রাঞ্চ থেকে চেক নিতে চাই",
        "আমি কুমিল্লা শাখা থেকে চেক নিতে চাই"
    ]
    for text in input_text_string:
        s_time = time.time()
        best_matched_branch, matching_ratio = mg.fuzzy_match(text, alias_to_branch)

        splited_branch_code = best_matched_branch.split("_")
        code = splited_branch_code[-1]
        # branch_name = splited_branch_code[:-1]
        branch_name = " ".join(splited_branch_code[:-1])
        print(code)
        print(branch_name)
        print("procesing time : ", time.time()-s_time)
        # print("Best Matched Branch:", best_matched_branch)
        # print("Matching Ratio:", matching_ratio)