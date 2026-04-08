def build_robust_rankzephyr_prompt(query, docs):
    num = len(docs)

    prompt = "<|system|>\n"
    prompt += "You are RankLLM, an intelligent assistant that can rank passages based on their relevancy to the query.</s>\n"

    prompt += "<|user|>\n"
    prompt += f"I will provide you with {num} passages, each indicated by a numerical identifier []. "
    prompt += f"Rank the passages based on their relevance to the search query: {query}.\n"

    for i, (_, text) in enumerate(docs):
        prompt += f"[{i+1}] {text}\n"

    prompt += f"\nSearch Query: {query}.\n"
    prompt += f"Rank the {num} passages above based on their relevance to the search query. "
    prompt += "All the passages should be included and listed using identifiers, in descending order of relevance. "
    prompt += "The output format should be [] > [], e.g., [2] > [1], "
    prompt += "Answer concisely and directly and only respond with the ranking results, "
    prompt += "do not say any word or explain.</s>\n"

    prompt += "<|assistant|>\n"

    return prompt