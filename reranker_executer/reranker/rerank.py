import torch
from .prompt_builder import build_robust_rankzephyr_prompt
from .parser import parse_ranking


def sliding_window_reranking(query_text, all_docs, model, tokenizer, window_size=5, stride=2):
    i = len(all_docs) - window_size

    while i >= 0:
        current_window = all_docs[i: i + window_size]

        prompt = build_robust_rankzephyr_prompt(query_text, current_window)

        inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to("cuda")
        input_length = inputs.input_ids.shape[1]

        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=50,
                do_sample=False,
                temperature=0.0,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id
            )

            generated_ids = output_ids[0][input_length:]
            response = tokenizer.decode(generated_ids, skip_special_tokens=True)

            print(response)

        ranked_indices = parse_ranking(response, len(current_window))

        new_window_order = [current_window[idx-1] for idx in ranked_indices]
        all_docs[i: i + window_size] = new_window_order

        del inputs, output_ids
        torch.cuda.empty_cache()

        i -= stride

    return all_docs