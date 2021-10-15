import json
import spacy

def find_award_names():
    f = open('gg2013.json')
    data = json.load(f)

    # texts = []
    # textfile = open("spacy.txt", "w")

    nlp = spacy.load("en_core_web_sm")

    text = "Ben Affleck won $20 for his work in Argo"
    doc = nlp(text)

    for entity in doc.ents:
        print(entity.text, entity.label_)

if __name__ == '__main__':
    find_award_names()