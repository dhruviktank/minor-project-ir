import argparse

from reranker.model_loader import load_rankzephyr
from reranker.data_loader import load_processed_qids, load_and_split_qids
from reranker.runner import run_reranking


QREL_FILES = {
    "dl19": "/content/drive/MyDrive/MinorProject/qrel_dl19.txt",
    "dl20": "/content/drive/MyDrive/MinorProject/qrel_dl20.txt"
}


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_file", required=True)

    parser.add_argument(
        "--qrel_type",
        choices=["dl19", "dl20"],
        required=True,
        help="Choose qrel dataset"
    )

    parser.add_argument(
        "--split",
        choices=["full", "first_half", "second_half"],
        default="full",
        help="Process subset of qrel ids"
    )

    parser.add_argument("--window_size", type=int, default=5)
    parser.add_argument("--stride", type=int, default=2)

    args = parser.parse_args()

    # ✅ Get correct qrel file automatically
    qrel_file = QREL_FILES[args.qrel_type]

    print(f"Using QREL: {args.qrel_type} -> {qrel_file}")

    # Load model
    model, tokenizer = load_rankzephyr()

    # Load processed qids
    processed_qids = load_processed_qids(args.output_file)

    # Load and split qids
    process_qids = load_and_split_qids(qrel_file, args.split)

    # Run pipeline
    run_reranking(
        args.input_file,
        args.output_file,
        model,
        tokenizer,
        process_qids,
        processed_qids,
        args.window_size,
        args.stride
    )


if __name__ == "__main__":
    main()