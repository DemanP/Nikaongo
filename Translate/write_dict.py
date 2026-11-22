import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

additionals = {
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

file_name: str = "en_ni.txt"
file = open(file_name, 'r')

text = file.read()
file.close()

en_ni = {}
for key in additionals.keys():
    en_ni[key] = [additionals[key]]

def add_word(en_word: str, ni_word: str):
    if en_word.startswith('#'):
        return
    if en_word not in en_ni:
        en_ni[en_word] = []
    en_ni[en_word].append(ni_word)

for line in text.splitlines():
    en_words, ni_word, *_ = line.split('\t')
    en_words = en_words.lower()
    ni_word = ni_word.lower()
    for en_word in en_words.split('/'):
        add_word(en_word, ni_word)

en_ni_file = open("en_ni.json", 'w')
en_ni_file.write(json.dumps(en_ni, indent=4))
en_ni_file.close()