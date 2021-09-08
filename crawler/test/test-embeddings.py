import psycopg2
from collections import defaultdict
from sentence_transformers import SentenceTransformer



def compute_embeddings(model, desc):
    embedding = model.encode(desc, convert_to_tensor=True)
    return embedding.tolist()




conn = psycopg2.connect(
    dbname="cloud",
    user="postgres",
    password="nB7geYEjbFT3UBUKJqfKkPuHpkKsUVsWmaDcrTdd6d6HpkKsUVsWmDaQDxJqfKkPu",
    host="host.docker.internal",
    port="10000",
)
cur = conn.cursor()
cur.execute('select preprocessed_description from "Jobs" limit 1')
row = cur.fetchone()
cur.close()
conn.close()
sent_model = SentenceTransformer('paraphrase-MiniLM-L12-v2')

embeddings = compute_embeddings(sent_model, row[0])
print(embeddings)
