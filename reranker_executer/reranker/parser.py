import re

def parse_ranking(response, num_docs):
    found = re.findall(r'\[(\d+)\]', response)
    indices = [int(i) for i in found if i.isdigit()]

    indices = [i for i in indices if 1 <= i <= num_docs]

    seen = set()
    clean_indices = [x for x in indices if not (x in seen or seen.add(x))]

    all_idx = set(range(1, num_docs + 1))
    missing = list(all_idx - set(clean_indices))

    return clean_indices + missing