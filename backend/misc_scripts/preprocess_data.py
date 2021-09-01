import re
import string
from itertools import groupby

import contractions
import emoji
import unidecode
from bs4 import BeautifulSoup
from symspellpy import helpers


def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    stripped_text = soup.get_text()
    return stripped_text


def add_spaces(text):
    # Space after punc. Only apply to !.,;:?
    # Eg: Dislike.However => Dislike. However
    text = re.compile(r"([!.,;:?])([A-Z])").sub(r"\1 \2", text)
    # Space before open bracket
    # Eg: Dislike(sth) => Dislike (sth)
    text = re.sub(r"([A-za-z])([\(\{\[])", r'\1 \2', text)
    # Space after close bracket
    # Eg: (such as)I like => (such as) I like
    text = re.sub(r"([\)\}\]])([A-Za-z])", r'\1 \2', text)
    # Space between word and - or +
    # Eg: I like it because-fast -pretty => I like it because - fast - pretty
    # Eg: I like mac-book => keep the same
    text = re.sub(r"([A-Za-z])([-+])(\s)", r'\1 \2 ', text)
    return text


def handle_listing_number(text):
    """
    Only remove if it is listing numbers such as 1. 2. 3.
    """
    listing = []

    def remove_listing_number(match_obj):
        listing_number = match_obj.group(0).strip()
        result = ""
        if match_obj.start() == 0 and listing_number[0] == "1":
            return ""
        for c in listing_number:
            if c.isdigit():
                # save to listing if it is digit
                listing.append(int(c))
                break
            result += c
        if not any(c in string.punctuation for c in result):
            result += "."
        return result + " "

    new_text = re.sub(r"\b([\.\;\:\!\?\D]*)([1-9])\.\s", remove_listing_number, text.strip())
    if len(listing) > 1:
        listing_copy = listing[:]
        listing_copy.sort()
        # if listing is sorted
        if listing_copy == listing:
            return new_text
    return text


def expand_contractions(text):
    """
    expand shortened words, e.g. don't to do not
    contractions library does not keep character case => need to transfer casing from origin text to fixed text
    """
    expanded_text = helpers.transfer_casing_for_similar_text(text, contractions.fix(text))
    # uppercase I
    return re.sub(r"\bi\b", "I", expanded_text)


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
