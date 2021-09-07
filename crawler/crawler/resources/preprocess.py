import re
from bs4 import BeautifulSoup
import string
from symspellpy import helpers
import contractions
import emoji
import unidecode
from itertools import groupby

def collapse_duplicated_punctuations(text):
    """
    collapse duplicated punctations
    because we added space to separate punc and word in step 3, no need to append " " after punc
    """
    newtext = []
    for k, g in groupby(text):
        if k in string.punctuation:
            newtext.append(k)
        else:
            newtext.extend(g)

    return ''.join(newtext) 

def expand_contractions(text):
    """
    expand shortened words, e.g. don't to do not
    contractions library does not keep character case => need to transfer casing from origin text to fixed text
    """
    expanded_text = helpers.transfer_casing_for_similar_text(text, contractions.fix(text))
    # uppercase I
    return re.sub(r"\bi\b", "I", expanded_text)

def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    stripped_text = soup.get_text()
    return stripped_text

# Remove and replace by empty space
def remove_redundant_elements(text):
    # remove urls
    text = re.sub(r"http\S+", " ", text)
    # remove phone
    text = re.sub(r"[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}", " ", text)
    # remove email
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", " ", text)
    # remove newline
    table = str.maketrans("\n\t\r", "   ")
    text = text.translate(table)
    # remove redundant whitespaces
    text = " ".join(text.split())
    return text

def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(r" ", text)

def remove_accented_chars(text):
    text = unidecode.unidecode(text)
    return text

def preprocess(text):
    text = remove_html_tags(text)
    text = expand_contractions(text)
    text = remove_redundant_elements(text)
    text = remove_emoji(text)
    text = remove_accented_chars(text)
    text = collapse_duplicated_punctuations(text)
    text = text.replace("\s+", " ")
    text = text.lower()
    return text