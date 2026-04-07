import argparse

from data_processing.query_loader import load_queries
from data_processing.run_loader import load_run_file
from data_processing.doc_loader import load_documents
from data_processing.jsonl_writer import write_jsonl


LANG_MAP = {
    "bn": "Bengali",
    "en": "English",
    "kn": "Kannada",
    "hi": "Hindi",
    "gu": "Gujarati"
}


def preview_collection(file_path, start=300, end=320):
    with open(file_path, "r", encoding="utf-8") as f:
        for i in range(start, end):
            line = f.readline()
            if not line:
                break
            print(line.strip())


def run_pipeline(lang, query_path, run_path, collection_path, output_path, max_k=100):
    if lang not in LANG_MAP:
        raise ValueError(f"Unsupported language: {lang}")

    lang_name = LANG_MAP[lang]

    # Step 1: Load queries
    query_map = load_queries(query_path, lang_name)

    # Step 2: Load run file
    run_grouped, doc_ids_needed = load_run_file(run_path, max_k)

    # Step 3: Load documents
    doc_map = load_documents(collection_path, doc_ids_needed)

    # Step 4: Write JSONL
    write_jsonl(output_path, run_grouped, query_map, doc_map)

    print(f"Generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="IR to LLM JSONL pipeline (single language)")

    parser.add_argument(
        "--lang",
        required=True,
        help="Language code (bn, en, kn, hi, gu)"
    )

    parser.add_argument(
        "--query_path",
        required=True,
        help="Path to query CSV"
    )

    parser.add_argument(
        "--run_path",
        required=True,
        help="Path to run file"
    )

    parser.add_argument(
        "--collection_path",
        required=True,
        help="Path to collection.tsv"
    )

    parser.add_argument(
        "--output_path",
        required=True,
        help="Output JSONL file path"
    )

    parser.add_argument(
        "--max_k",
        type=int,
        default=100,
        help="Top-K documents per query"
    )

    parser.add_argument(
        "--preview_collection",
        action="store_true",
        help="Preview collection content"
    )

    args = parser.parse_args()

    # Handle preview mode
    if args.preview_collection:
        preview_collection(args.collection_path)
        return  # stop after preview

    # Run pipeline
    run_pipeline(
        lang=args.lang,
        query_path=args.query_path,
        run_path=args.run_path,
        collection_path=args.collection_path,
        output_path=args.output_path,
        max_k=args.max_k
    )


if __name__ == "__main__":
    main()