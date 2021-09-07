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

description = """
Full Job Description
What We'll Bring:

A work environment that encourages collaboration and innovation. We consistently explore new technologies and tools to be agile.
Flexible time off, workplace flexibility, an environment that welcomes continued professional growth through support of tuition reimbursement, conferences and seminars.
Our culture encourages our people to hone current skills and build new capabilities, while discovering their genius.
The chance to work within a challenge and engaging team, supporting some of TransUnion's most critical infrastructure.
What You'll Bring:

Experience with Visio, Asset Management and BMS tools
Practical knowledge and work experience with structured cabling and the layer 1 infrastructure
Proficiency with basic operations of a PC, proficiency in MS Office and Outlook preferred
Able to understand installation specifications
A disciplined approach to managing task assignments and strong people skills; good judgement and flexibility are critical to this position
A team-player attitude with the ability to work autonomously and responsibly in a mission- critical Data Center environment
Must be flexible with work schedule as needed including nights, weekends, holidays and on-call schedule.
Rack and Stack customer equipment
The ability to easily lift up to 50 lbs. throughout the day
What We'd Prefer to See:

A willingness to travel up to 5 – 10%
Impact You'll Make:

Work with members of the data center team to schedule and preform all project and daily operations task within the data center sites.
Provide support for remote site refresh work within the US states and Canada.
Travel between data center sites within the Chicagoland area for hands-on support and data center consolidations.
Cabling: Daily installation and oversight of all network and storage patching for new systems including maintenance of appropriate documentation for all pathways and labeling of all connections.
Installation: Daily installation of all IT servers, network hardware and related components to manufacturer specification.
Space assignment: Provision exact space assignments and maintain documentation for each IT device and all related components ensuring proper operation and appropriate expansion space.
Power assignment: Provision exact power assignments and maintain documentation for all rack mounted and floor mounted devices maintaining appropriate power distribution and utilization.
Cabinet Layout: Assign space, power, tile cuts and cable raceways for all new rows of server cabinets, floor mounted devices, storage frames, tape drives etc.
Cable plant design: Work with hardware owners to understand project requirements and select, document and order appropriate solutions to meet connectivity and density needs.
Daily operation and oversight: Manage relationships with facility support and IT manufacturer service providers to ensure appropriate daily operation and accurate installations.
Onsite Support: Respond to incidents and work with other teams in the verification and recovery process of IT systems. Must have flexible schedule for afterhours support and on call.
"""

print(preprocess(description))