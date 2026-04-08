from tqdm import tqdm
from .rerank import sliding_window_reranking


def run_reranking(input_file, output_file, model, tokenizer, process_qids, processed_qids,
                  window_size=5, stride=2):

    with open(output_file, 'a', encoding='utf-8') as f_out:

        remaining_count = len(process_qids) - len(processed_qids)

        from .data_loader import load_data_generator

        for qid, query_text, current_docs in tqdm(
            load_data_generator(input_file, processed_qids, process_qids),
            total=remaining_count,
            desc="Reranking Queries"
        ):

            if len(current_docs) < 2:
                continue

            original_top_3 = [str(d[0]) for d in current_docs[:3]]

            try:
                final_ranked_docs = sliding_window_reranking(
                    query_text,
                    current_docs,
                    model,
                    tokenizer,
                    window_size,
                    stride
                )

                final_top_3 = [str(d[0]) for d in final_ranked_docs[:3]]

                if original_top_3 == final_top_3:
                    print(f"\n[Warning] QID {qid}: No change in Top 3 order.")
                    print(f"  Original: {original_top_3}")
                    print(f"  Final:    {final_top_3}")
                else:
                    print(f"\n[Success] QID {qid}: Order changed!")
                    print(f"  Before: {original_top_3}")
                    print(f"  After:  {final_top_3}")

                for rank, (docid, _) in enumerate(final_ranked_docs):
                    f_out.write(f"{qid} Q0 {docid} {rank+1} {100-rank} RankZephyr_Slide\n")

                f_out.flush()

            except Exception as e:
                print(f"\nError processing QID {qid}: {e}")
                continue

    print(f"Success! Reranked remaining queries. Results saved to {output_file}")