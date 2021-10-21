import json
import spacy
import re
import statistics
from statistics import mode
import string

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
INDICATORS = ['wins', 'won', 'goes to', 'gets the', 'congrats', 'win']
PEOPLE_AWARDS = ['cecil b. demille award', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television', 'best screenplay - motion picture']
COLLOQUIAL_PEOPLE_AWARDS = ['cecil b. demille award', 'best actress in a motion picture - drama', 'best actor in a motion picture - drama', 'best actress in a motion picture - comedy or musical', 'best actor in a motion picture - comedy or musical', 'best supporting actress in a motion picture', 'best supporting actor in a motion picture', 'best director', 'best actress in a tv series, drama', 'best actor in a tv series, drama', 'best actress in a tv comedy or musical', 'best actor in a tv comedy or musical', 'best actress in a mini-series or tv movie', 'best actor in a mini-series or tv movie', 'best supporting actress (tv)', 'best supporting actor (tv)', 'best screenplay']
MOVIE_AWARDS = ['best motion picture - drama', 'best motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best original score - motion picture']
TV_AWARDS = ['best television series - drama', 'best television series - comedy or musical', 'best mini-series or motion picture made for television']
SONG_AWARDS = ['best original song - motion picture']

def movie_awards():
    potential_drama = []
    potential_comedy = []
    potential_animated = []
    potential_foreign = []
    potential_score = []

    search_drama = []
    search_comedy = []
    search_animated = []
    search_foreign = []
    search_score = []

    winners = []

    with open('clean_json_with_caps.txt') as f:
        for text in f:
            if "best motion picture" in text.lower():
                if "actor" in text.lower() or "actress" in text.lower():
                    continue
                if "drama" in text.lower():
                    potential_drama.append(text)
                elif "comedy" in text.lower() or "musical" in text.lower():
                    potential_comedy.append(text)
            elif "animated feature film" in text.lower():
                potential_animated.append(text)
            elif "foreign language film" in text.lower() or "foreign film" in text.lower():
                potential_foreign.append(text)
            elif "score" in text.lower():
                potential_score.append(text)


    for line in potential_drama:
        if "wins" in line.lower():
            split = line.split('wins')
            candidate = split[0]
            if candidate is not None:
                if len(candidate.split()) < 7:
                    clean = candidate.translate(str.maketrans('', '', string.punctuation))
                    search_drama.append(clean.title().strip())

    for line in potential_comedy:
        if "wins" in line.lower():
            split = line.split('wins')
            candidate = split[0]
            if candidate is not None:
                if len(candidate.split()) < 7:
                    clean = candidate.translate(str.maketrans('', '', string.punctuation))
                    search_comedy.append(clean.title().strip())

    for line in potential_animated:
        if "wins" in line.lower():
            split = line.split('wins')
            candidate = split[0]
            if candidate is not None:
                if len(candidate.split()) < 7:
                    clean = candidate.translate(str.maketrans('', '', string.punctuation))
                    search_animated.append(clean.title().strip())

    for line in potential_foreign:
        if "wins" in line.lower():
            split = line.split('wins')
            candidate = split[0]
            if candidate is not None:
                if len(candidate.split()) < 7:
                    clean = candidate.translate(str.maketrans('', '', string.punctuation))
                    search_foreign.append(clean.title().strip())

    for line in potential_score:
        if "wins" in line.lower():
            split = line.split('wins')
            candidate = split[0]
            if candidate is not None:
                if len(candidate.split()) < 7:
                    clean = candidate.translate(str.maketrans('', '', string.punctuation))
                    search_score.append(clean.title().strip())

    winners.append(max(set(search_drama), key=search_drama.count))
    winners.append(max(set(search_comedy), key=search_comedy.count))
    winners.append(max(set(search_animated), key=search_animated.count, default=0))
    winners.append(max(set(search_foreign), key=search_foreign.count, default=0))
    winners.append(max(set(search_score), key=search_score.count, default=0))

    print(winners)

def people_awards():
    nlp = spacy.load("en_core_web_sm")

    winners = []

    final_winners = []

    for category in COLLOQUIAL_PEOPLE_AWARDS:
        potential_winners = []
        with open('clean_json_with_caps.txt') as f:
            for text in f:
                if category in text.lower():
                    doc = nlp(text)
                    for entity in doc.ents:
                        if entity.label_ == 'PERSON' and 'Best' not in entity.text and '#' not in entity.text:
                            potential_winners.append(entity.text)
            if potential_winners:
                most_likely = mode(potential_winners)
            else:
                winners.append("None Found")
                continue
        winners.append(most_likely)

    for name in winners: # Final Error Check
        doc = nlp(name)
        for entity in doc.ents:
            if entity.label_ == 'PERSON':
                final_winners.append(entity.text)

    print(final_winners)

def tv_awards():
    potential_drama = []
    potential_comedy = []
    potential_mini = []

    search_drama = []
    search_comedy = []
    search_mini = []

    winners = []

    with open('clean_json_with_caps.txt') as f:
        for text in f:
            if "best tv series" in text.lower() or "best television series" in text.lower() or "best mini-series" in text.lower():
                if "actor" in text.lower() or "actress" in text.lower():
                    continue
                if "drama" in text.lower():
                    potential_drama.append(text)
                elif "comedy" in text.lower() or "musical" in text.lower():
                    potential_comedy.append(text)
                elif "mini-series" in text.lower():
                    potential_mini.append(text)

    for line in potential_drama:
        if "wins" in line.lower():
            split = line.split('wins')
            candidate = split[0]
            if candidate is not None:
                if len(candidate.split()) < 7:
                    clean = candidate.translate(str.maketrans('', '', string.punctuation))
                    search_drama.append(clean.title().strip())

    for line in potential_comedy:
        if "wins" in line.lower():
            split = line.split('wins')
            candidate = split[0]
            if candidate is not None:
                if len(candidate.split()) < 7:
                    clean = candidate.translate(str.maketrans('', '', string.punctuation))
                    search_comedy.append(clean.title().strip())

    for line in potential_mini:
        if "wins" in line.lower():
            split = line.split('wins')
            candidate = split[0]
            if candidate is not None:
                if len(candidate.split()) < 7:
                    clean = candidate.translate(str.maketrans('', '', string.punctuation))
                    search_mini.append(clean.title().strip())

    winners.append(max(set(search_drama), key=search_drama.count))
    winners.append(max(set(search_comedy), key=search_comedy.count))
    winners.append(max(set(search_mini), key=search_mini.count))

    print(winners)

def song_awards():
    potential_song = []
    search_song = []
    winners = []
    with open('clean_json_with_caps.txt') as f:
        for text in f:
            if "song" in text.lower():
                potential_song.append(text)

        for line in potential_song:
            if "wins" in line.lower():
                split = line.split('wins')
                candidate = split[0]
                if candidate is not None:
                    if len(candidate.split()) < 7:
                        clean = candidate.translate(str.maketrans('', '', string.punctuation))
                        search_song.append(clean.title().strip())

    winners.append(max(set(search_song), key=search_song.count))

    print(winners)

if __name__ == '__main__':
    movie_awards()
    people_awards()
    tv_awards()
    song_awards()
