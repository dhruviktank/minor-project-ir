import csv

def load_queries(file_path, lang_name):
    query_map = {}

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            query_map[row["id"]] = row["translated_" + lang_name.lower()]

    return query_map