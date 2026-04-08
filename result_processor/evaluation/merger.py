import pandas as pd

def merge_results(file_kaggle, file_colab, merged_output):
    columns = ['qid', 'q0', 'docid', 'rank', 'score', 'run_id']

    df_k = pd.read_csv(file_kaggle, sep='\\s+', names=columns, header=None)
    df_c = pd.read_csv(file_colab, sep='\\s+', names=columns, header=None)

    combined_df = pd.concat([df_k, df_c], ignore_index=True)

    deduplicated_df = combined_df.drop_duplicates(subset=['qid', 'docid'], keep='first')

    deduplicated_df = deduplicated_df.sort_values(by=['qid', 'score'], ascending=[True, False])

    deduplicated_df.to_csv(merged_output, sep=' ', index=False, header=False)

    print(f"Merge Complete!")
    print(f"Kaggle rows: {len(df_k)}")
    print(f"Colab rows: {len(df_c)}")
    print(f"Final deduplicated rows: {len(deduplicated_df)}")
    print(f"Total Unique Queries: {deduplicated_df['qid'].nunique()}")