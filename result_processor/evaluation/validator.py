import json
import os

def validate_results(source_path, result_path, qrels_path, expected_docs_per_query=20):
    source_qids = set()

    # --- Load source qids ---
    if not os.path.exists(source_path):
        print(f"Error: Source file not found at {source_path}")
        return

    with open(source_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            source_qids.add(int(data['query']['qid']))

    # --- Load qids from qrels file ---
    if not os.path.exists(qrels_path):
        print(f"Error: Qrels file not found at {qrels_path}")
        return

    qrel_qids = set()
    with open(qrels_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 4:
                qid = int(parts[0])
                qrel_qids.add(qid)

    # 🔥 Filter only qrel queries
    source_qids = source_qids & qrel_qids

    print(f"Filtering validation to {len(source_qids)} QREL queries")

    # --- Load result counts ---
    result_counts = {}

    if not os.path.exists(result_path):
        print(f"Error: Result file not found at {result_path}")
        return

    with open(result_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            if parts:
                qid = int(parts[0])
                result_counts[qid] = result_counts.get(qid, 0) + 1

    result_qids = set(result_counts.keys())

    # --- Compare ---
    missing_qids = source_qids - result_qids
    extra_qids = result_qids - source_qids

    incomplete_qids = {
        qid: count for qid, count in result_counts.items()
        if count < expected_docs_per_query and qid in source_qids
    }

    # --- REPORT ---
    print("-" * 30)
    print("VALIDATION REPORT")
    print("-" * 30)
    print(f"Total Source Queries:   {len(source_qids)}")
    print(f"Total Result Queries:   {len(result_qids)}")

    if not missing_qids:
        print("✅ SUCCESS: All source Query IDs are present.")
    else:
        print(f"❌ MISSING: {len(missing_qids)} queries are missing from the result.")
        print(f"   Missing IDs: {sorted(list(missing_qids))}")

    if incomplete_qids:
        print(f"⚠️  INCOMPLETE: {len(incomplete_qids)} queries have fewer than {expected_docs_per_query} docs.")
        for qid, count in list(incomplete_qids.items())[:5]:
            print(f"   QID {qid}: found {count} docs.")
    else:
        print(f"✅ COMPLETE: All queries have at least {expected_docs_per_query} documents.")

    if extra_qids:
        print(f"ℹ️  Note: Found {len(extra_qids)} Query IDs in results that weren't in filtered source.")