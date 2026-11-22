import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def add_word(word_type: str, en_word: str, ni_word: str) -> None:
    if word_type == "pron.":
        word_type = "pronoun"
    elif word_type == "adj.":
        word_type = "adjective"
    elif word_type == "conj":
        word_type = "conjunction"

    if en_word not in en_ni:
        en_ni[en_word] = {
            "type": word_type,
            "nikaongo": []
        }
    en_ni[en_word]["nikaongo"].append(ni_word)

file_name: str = "en_ni.txt"
file = open(file_name, 'r')

text = file.read()
file.close()

en_ni = {}

pronouns = {
    "my": "vatawi des",
    "mine": "vatawi des",
    "your": "ju des",
    "yours": "ju des",
    "his": "xi des",
    "her": "wi des",
    "its": "kivi des",
    "our": "moy des",
    "ours": "moy des",
    "their": "grup des",
    "i'm": "vatawi is"
}
for key in pronouns.keys():
    add_word("pronoun", key, pronouns[key])

for line in text.splitlines():
    # skip comments and empty lines
    if line.startswith('#') or not len(line) or line.isspace():
        continue

    type, en_words, ni_word, *_ = line.split('\t')
    en_words = en_words.lower()
    ni_word = ni_word.lower()
    for en_word in en_words.split('/'):
        add_word(type, en_word, ni_word)

en_ni_file = open("en_ni.json", 'w')
en_ni_file.write(json.dumps(en_ni, indent=4))
en_ni_file.close()