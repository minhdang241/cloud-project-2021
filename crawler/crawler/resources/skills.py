from collections import defaultdict


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
