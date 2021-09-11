import argparse
import json
import logging
from collections import defaultdict

import psycopg2
import torch
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--job', action='store_true')
    args = parser.parse_args()
    conn = None
    descriptions = []
    try:
        conn = psycopg2.connect(
            dbname="cloud",
            user="postgres",
            password="nB7geYEjbFT3UBUKJqfKkPuHpkKsUVsWmaDcrTdd6d6HpkKsUVsWmDaQDxJqfKkPu",
            host="localhost",
            port="10000",
        )

        cur = conn.cursor()
        cur.execute(f'SELECT career_id FROM "Careers"')
        rows = cur.fetchall()
        hash_map = defaultdict(list)
        for row in rows:
            career_id = row[0]
            cur.execute(f'SELECT preprocessed_description FROM "Jobs" WHERE career_id={career_id}')
            results = cur.fetchall()
            for res in results:
                hash_map[career_id].append(res[0])

        sent_model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
        rows = []
        for k, v in hash_map.items():
            embedding = sent_model.encode(v, convert_to_tensor=True)
            avg_embed = torch.mean(embedding, dim=0)
            row_vals = {f'career_id': k, 'embeddings': json.dumps(avg_embed.tolist())}
            rows.append(row_vals)

        logging.debug(len(rows))
        cur.executemany(
            f'''
                UPDATE "Careers"
                SET
                    embeddings = %(embeddings)s
                WHERE
                    career_id = %(career_id)s
            ''', tuple(rows)
        )
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
