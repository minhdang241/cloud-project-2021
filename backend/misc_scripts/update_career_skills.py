import argparse
import json
import logging
from collections import defaultdict

import psycopg2

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
        hash_map = defaultdict(set)
        for row in rows:
            career_id = row[0]
            cur.execute(f'SELECT skills FROM "Jobs" WHERE career_id={career_id}')
            results = cur.fetchall()
            for res in results:
                hash_map[career_id].update(res[0])
        data = []
        for k, v in hash_map.items():
            data.append({'career_id': k, 'skills': json.dumps(list(v))})

        cur.executemany(
            '''
                UPDATE "Careers"
                SET
                    skills = %(skills)s
                WHERE
                    career_id = %(career_id)s
            ''', tuple(data)
        )

        conn.commit()
        cur.close()
        logging.info("UPDATE successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
