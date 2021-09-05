import argparse
import json
import logging

import psycopg2
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
        if args.job:
            id_name = 'job_id'
            table_name = 'Jobs'
        else:
            id_name = 'course_id'
            table_name = 'Courses'

        cur.execute(f'SELECT {id_name}, preprocessed_description FROM "{table_name}"')

        rows = cur.fetchall()
        for row in rows:
            descriptions.append((row[0], row[1]))

        sent_model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
        rows = []
        for id, desc in descriptions:
            embedding = sent_model.encode(desc, convert_to_tensor=True)
            print(len(embedding.tolist()))
            row_vals = {f'{id_name}': id, 'embeddings': json.dumps(embedding.tolist())}
            rows.append(row_vals)

        logging.debug(len(rows))
        cur.executemany(
            f'''
                UPDATE "{table_name}"
                SET
                    embeddings = %(embeddings)s
                WHERE
                    {id_name} = %({id_name})s
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
