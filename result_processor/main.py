import argparse

from evaluation.merger import merge_results
from evaluation.evaluator import evaluate_run
from evaluation.validator import validate_results


def main():
    parser = argparse.ArgumentParser(description="Merge, Evaluate, and Validate IR Results")

    # --- File Inputs ---
    parser.add_argument("--file_1", required=True, help="Path to first half result file")
    parser.add_argument("--file_2", required=True, help="Path to second half result file")
    parser.add_argument("--merged_output", required=True, help="Path to save merged output")

    parser.add_argument("--qrels_path", required=True, help="Path to qrels file")
    parser.add_argument("--source_jsonl", required=True, help="Path to source JSONL file")

    args = parser.parse_args()

    # 1. Merge
    merge_results(
        args.file_1,
        args.file_2,
        args.merged_output
    )

    # 2. Evaluate
    evaluate_run(
        args.qrels_path,
        args.merged_output
    )

    # 3. Validate
    validate_results(
        args.source_jsonl,
        args.merged_output,
        args.qrels_path
    )


if __name__ == "__main__":
    main()


# python3 main.py \
#   --file_1 ../results/hi_en/dl19/hi_en_colab.txt \
#   --file_2 ../results/hi_en/dl19/hi_en_kaggle.txt \
#   --merged_output hi_en_dl19_results.txt \
#   --qrels_path qrels/qrel_dl19.qrels \
#   --source_jsonl ../dataset/index_for_llm/hi_en.jsonl