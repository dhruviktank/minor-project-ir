def load_documents(file_path, doc_ids_needed):
    doc_map = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t", 1)

            if len(parts) < 2:
                continue

            pid = parts[0].strip()
            text = parts[1].strip()

            if pid in doc_ids_needed:
                doc_map[pid] = text

            if len(doc_map) == len(doc_ids_needed):
                break

    return doc_map