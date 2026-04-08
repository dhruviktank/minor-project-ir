import json
import os

def load_processed_qids(output_file):
    processed_qids = set()

    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.split()
                if parts:
                    processed_qids.add(int(parts[0]))
        print(f"Resuming session: {len(processed_qids)} queries already processed. Skipping them...")
    else:
        print("No existing output file found. Starting fresh.")

    return processed_qids


def load_target_qids(qrel_file):
    process_qids = set()

    if os.path.exists(qrel_file):
        with open(qrel_file, 'r', encoding='utf-8') as f:
            for line in f:
                process_qids.add(int(line.split()[0]))

    return process_qids


def load_data_generator(file_path, processed_qids, process_qids):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            qid = data['query']['qid']

            if qid in processed_qids or qid not in process_qids:
                continue

            query_text = data['query']['text']

            current_docs = []
            for cand in data['candidates']:
                docid = cand['docid']
                text = cand['doc']['contents'][:800]
                current_docs.append((docid, text))

            yield qid, query_text, current_docs

def load_and_split_qids(qrel_file, split="full"):
    qids = []

    if not qrel_file:
        return set()

    with open(qrel_file, 'r', encoding='utf-8') as f:
        for line in f:
            qids.append(int(line.strip()))

    qids = sorted(qids)

    if split == "first_half":
        mid = len(qids) // 2
        qids = qids[:mid]

    elif split == "second_half":
        mid = len(qids) // 2
        qids = qids[mid:]

    # else: full → no change

    print(f"Using {len(qids)} queries after applying split='{split}'")

    return set(qids)