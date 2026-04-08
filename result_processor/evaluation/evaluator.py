from ranx import Qrels, Run, evaluate

def evaluate_run(qrels_path, run_path):
    qrels = Qrels.from_file(qrels_path, kind="trec")
    run = Run.from_file(run_path, kind="trec")

    run_qids = set(run.qrels.keys()) if hasattr(run, "qrels") else set(run.run.keys())

    filtered_qrels_dict = {qid: qrels.qrels[qid] for qid in qrels.qrels if qid in run_qids}
    print(len(filtered_qrels_dict))

    filtered_qrels = Qrels(filtered_qrels_dict)

    metrics = [
        "precision@10", "recall@10",
        "precision@100", "recall@100",
        "ndcg@10", "ndcg@100",
        "map", "mrr"
    ]

    results = evaluate(filtered_qrels, run, metrics, make_comparable=True)

    print("--- Evaluation Summary ---")
    for metric, value in results.items():
        print(f"{metric.upper()}: {value:.4f}")