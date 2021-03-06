import argparse
import json
import logging
from collections import defaultdict

import psycopg2
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

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
        if args.job:
            id_name = 'job_id'
            table_name = 'Jobs'
        else:
            id_name = 'course_id'
            table_name = 'Courses'

        cur.execute(f'SELECT {id_name}, description FROM "{table_name}"')

        rows = cur.fetchall()
        for row in rows:
            descriptions.append((row[0], row[1]))

        checkpoint = "mrm8488/codebert-base-finetuned-stackoverflow-ner"
        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModelForTokenClassification.from_pretrained(checkpoint)
        classifier = pipeline("token-classification", model=model, tokenizer=tokenizer)

        rows = []
        for id, desc in descriptions:
            skills = extract_skills(classifier, desc)
            row_vals = {f'{id_name}': id, 'skills': json.dumps(skills)}
            logging.debug(row_vals)
            rows.append(row_vals)

        logging.debug(len(rows))
        cur.executemany(
            f'''
                UPDATE "{table_name}" 
                SET
                    skills = %(skills)s
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
