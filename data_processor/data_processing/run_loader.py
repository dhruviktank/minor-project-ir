from collections import defaultdict

def load_run_file(file_path, max_k):
    run_grouped = defaultdict(list)
    doc_ids_needed = set()

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()

            qid = parts[0]
            docid = parts[2]
            score = float(parts[4])

            if len(run_grouped[qid]) < max_k:
                run_grouped[qid].append({
                    "docid": docid,
                    "score": score
                })
                doc_ids_needed.add(docid)

    return run_grouped, doc_ids_needed