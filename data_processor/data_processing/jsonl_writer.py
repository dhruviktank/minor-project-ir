import json

def write_jsonl(output_path, run_grouped, query_map, doc_map):
    with open(output_path, "w", encoding="utf-8") as out:

        for qid, docs in run_grouped.items():

            query_text = query_map.get(qid, "")

            candidates = []

            for d in docs:
                docid = d["docid"]

                candidates.append({
                    "docid": docid,
                    "score": d["score"],
                    "doc": {
                        "contents": doc_map.get(docid, "")
                    }
                })

            final_obj = {
                "query": {
                    "text": query_text,
                    "qid": int(qid)
                },
                "candidates": candidates
            }

            out.write(json.dumps(final_obj, ensure_ascii=False) + "\n")