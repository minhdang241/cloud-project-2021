from sentence_transformers import SentenceTransformer


sent_model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

def compute_embeddings(desc):
    embedding = sent_model.encode(desc, convert_to_tensor=True)
    return embedding.tolist()