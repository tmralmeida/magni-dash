from typing import List


def get_files_name_mapping(files_target: List[str]):
    splitted_file_name = list(map(lambda x: x.split("SC6"), files_target))
    scenarios6a_files = [
        sample for sample in splitted_file_name if list(sample[1])[0] == "A"
    ]
    scenarios6b_files = [
        sample for sample in splitted_file_name if list(sample[1])[0] == "B"
    ]
    options_per_scenario = {
        "SC6".join([file6a[0], file6a[1][1:]]): (
            "SC6".join(file6a),
            "SC6".join(file6b),
        )
        for file6a in scenarios6a_files
        for file6b in scenarios6b_files
        if list(file6a[1])[1:] == list(file6b[1])[1:] and file6a[0] == file6b[0]
    }

    return options_per_scenario
