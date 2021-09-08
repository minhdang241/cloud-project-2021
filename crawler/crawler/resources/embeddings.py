def compute_embeddings(sent_model, desc):
    embedding = sent_model.encode(desc, convert_to_tensor=True)
    return embedding.tolist()