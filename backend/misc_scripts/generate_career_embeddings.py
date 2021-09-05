import argparse
import json
import logging
from collections import defaultdict

import psycopg2
import torch
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_space(ent):
    ent['word'] = ent['word'].replace('Ġ', ' ')
    return ent


def merge_B_I_entities(ents):
    results = []
    i = 0
    N = len(ents)
    while i < N:
        ent = ents[i]
        ent = add_space(ent)
        if i < N - 1 and ent['entity'][:2] == 'B-':
            i += 1
            next_ent = ents[i]
            while i < N and next_ent['entity'][:2] == 'I-':
                ent['word'] += add_space(next_ent)['word']
                i += 1
                if i < N:
                    next_ent = ents[i]
                else:
                    break
            i -= 1
            ent['end'] = ents[i]['end']
            ent['word'] = ent['word'].strip().lower()
        results.append(ent)
        i += 1
    return results


def merge_entity(ent1, ent2):
    if ent1['end'] == ent2['start']:
        ent = {'start': ent1['start'], 'end': ent2['end'], 'entity': ent1['entity'],
               'word': (ent1['word'] + ent2['word']).strip().lower()}
        return ent


def merge_similar_entities(ents):
    results = []
    hash_map = defaultdict(list)
    for ent in ents:
        hash_map[ent['entity']].append(ent)
    for k, v in hash_map.items():
        new_ents = []
        merge_ent = v[0]
        i = 0
        while i < len(v) - 1:
            temp = merge_entity(merge_ent, v[i + 1])
            if temp:
                merge_ent = temp
            else:
                new_ents.append(merge_ent)
                merge_ent = v[i + 1]
            i += 1
        merge_ent['word'] = merge_ent['word'].strip().lower()
        new_ents.append(merge_ent)
        results += new_ents
    return results


def extract_skills(classifier, desc):
    ents = classifier(desc)
    results = merge_B_I_entities(ents)
    results = merge_similar_entities(results)
    skills = set()
    for ent in results:
        skills.add(ent['word'])
    return list(skills)


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
