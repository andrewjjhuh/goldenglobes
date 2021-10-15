import json
import spacy
import re

def find_award_names():
    f = open('gg2013.json')
    data = json.load(f)

    texts = []
    textfile = open("test.txt", "w")

    for tweet in data:
        text = tweet['text']
        text = text.lower()
        if "wins the golden globe for" in text:
        # if "wins for" in text:
            result = re.search('wins the golden globe for (.*) for', text)
            # if result is None:
            #     result = re.search('wins the golden globe for (.*) in', text)
            if result is None:
                continue
            texts.append(result.group(1))
            textfile.write(result.group(1) + "\n")

    print(texts)

    textfile.close()

def clean_json():
    f = open('gg2013.json')
    data = json.load(f)

    texts = []
    textfile = open("clean_json.txt", "w")

    for tweet in data:
        text = tweet['text']
        text = text.lower()
        if "rt @" in text:
            continue
        textfile.write(text + "\n")

if __name__ == '__main__':
    find_award_names()
    # clean_json()

