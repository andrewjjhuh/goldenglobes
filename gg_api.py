'''Version 0.35'''
import spacy
import string
import json
from statistics import mode

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
STOPWORDS = ['performance', 'by', 'an', 'in', 'a', 'or', '-', 'made', 'for', 'any']
AWARD_STOPWORDS = {'!', '.', '?', ':', 'wins', 'did', 'didn', 'do', 'does', 'has', 'won', 'about', 'glasses', 'vine',
             'comeback', 'facial', 'speech', 'female', 'the', 'guy', 'male', 'costume', 'dress', 'social', 'biggest',
             '#', 'worst', 'golden', 'globe', 'presenter', 'most', 'joke', '"', 'about', 'giving', 'this', 'not', 'before',
             'which', 'twitter', 'my', 'his', 'her', 'at', 'and', 'journey', 'stacked', 'maybe', 'oscar'}

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    f = open('gg2015.json')
    data = json.load(f)

    final_award_names = set()
    goes_to = []

    for tweet in data:
        text = tweet['text']
        text = text.lower()
        if "wins the golden globe for" in text:
            result = re.search('wins the golden globe for (.*) for', text)
            if result is None:
                continue
            if any(word in AWARD_STOPWORDS for word in result.group(1).split()) or len(result.group(1).split()) < 3:
                continue
            final_award_names.add(result.group(1))

        elif "goes to" in text:
            result = re.search('the golden globe for (.*) goes to', text)
            if result is None:
                continue
            if any(word in AWARD_STOPWORDS for word in result.group(1).split()) or len(result.group(1).split()) < 3:
                continue
            goes_to.append(result.group(1))

    award_list = list(final_award_names)
    award_list_temp = list(final_award_names)

    for award in award_list:
        award_list_temp.remove(award)
        if any(award in s for s in award_list_temp):
            final_award_names.remove(award)

    award_list = list(final_award_names)

    goes_to.sort()
    c = Counter(goes_to)
    for common in c.most_common():
        if common[1] > 1:
            if any(common[0] in s for s in award_list):
                continue
            final_award_names.add(str(common[0]))
        if len(final_award_names) >= 26:
            break

    awards = list(final_award_names)

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    if year == 2013 or year == 2015:
        award_names = OFFICIAL_AWARDS_1315
    else:
        award_names = OFFICIAL_AWARDS_1819

    winners = dict.fromkeys(award_names, None)

    cleaned_awards = []

    positivity = []
    controversy = []

    for award in award_names:  # Splits and cleans the award names for processing
        split = award.split()
        new_word = []
        for word in split:
            if word not in STOPWORDS:  # Many words are irrelevant, removed with list of stopwords
                new_word.append(word)
                if word == 'television':  # Usually television is shortened to tv, want to account for both
                    new_word.append('tv')
        cleaned_awards.append(new_word)

    winner_list = []

    for award in cleaned_awards:
        measure = len(award)  # Measure will initially give little allowance, ease up over time if we don't find result
        if 'television' in award:  # Can give additional allowance for television, since we included tv as well
            measure = measure - 1
        if 'cecil' in award or 'actress' in award or 'actor' in award or 'screenplay' in award or 'director' in award:
            flag = find_winner_people(measure, award, winner_list, positivity, controversy)  # These words indicate the award is to a person
            while flag is False:
                measure = measure-1
                flag = find_winner_people(measure, award, winner_list, positivity, controversy)  # Search until we find a result
        else:
            flag = find_winner_general(measure, award, winner_list, positivity, controversy)  # Non-person awards are under a separate function
            while flag is False:
                measure = measure - 1
                flag = find_winner_general(measure, award, winner_list, positivity, controversy)

    for award, winner in zip(award_names, winner_list):
        winners[award] = winner

    max_positivity = max(positivity)
    min_positivity = min(positivity)
    max_controversy = max(controversy)

    index_positivity = positivity.index(max_positivity)
    index_negativity = positivity.index(min_positivity)
    index_controversy = controversy.index(max_controversy)

    print("The most positive reaction to a win was to the award " + award_names[index_positivity] + ", winner: " + winner_list[index_positivity])
    print("The most negative reaction to a win was to the award " + award_names[index_negativity] + ", winner: " + winner_list[index_negativity])
    print("The award that genereated the most controversy was " + award_names[index_controversy] + ", winner: " + winner_list[index_controversy])

    return winners

def find_winner_people(measure, award_name, winners_people, positivity, controversy):
    potential_winners = []

    compound_scores = []
    analyzer = SentimentIntensityAnalyzer()

    nlp = spacy.load("en_core_web_sm")
    with open('clean_person_entities.txt') as f:
        for text in f:
            count = 0
            for word in award_name:
                if word in text.lower():
                    count += 1  # Count helps us to see whether award is mentioned or not
            if count == measure:
                doc = nlp(text)
                for entity in doc.ents:  # Searching for person-entities, usually winner is mentioned most with award
                    if entity.label_ == 'PERSON' and 'Best' not in entity.text and '#' not in entity.text:
                        potential_winners.append(entity.text)
                        score = analyzer.polarity_scores(text)
                        compound_scores.append(score['compound'])
        if potential_winners:
            person_check = []
            for people in potential_winners:
                if len(people.split()) > 1:
                    person_check.append(people)
            winners_people.append(mode(person_check))  # Append the most common person associated with award
            positivity.append(sum(compound_scores)/len(compound_scores))
            controversy.append(np.var(compound_scores))
            return True
        else:
            return False

def find_winner_general(measure, award_name, winners, positivity, controversy):
    potential_winners = []

    compound_scores = []
    analyzer = SentimentIntensityAnalyzer()

    with open('clean_non_person_entities.txt') as f:
        for text in f:
            count = 0
            for word in award_name:
                if word in text.lower():
                    count += 1  # Count helps us to see whether award is mentioned or not
            if count == measure:
                if "wins" in text.lower():
                    split = text.split('wins')
                    candidate = split[0]  # Accounts for common formatting "____ wins the award for ___"
                    if candidate is not None:
                        if len(candidate.split()) < 7:  # Don't want long strings making their way into winners
                            clean = candidate.translate(str.maketrans('', '', string.punctuation))
                            potential_winners.append(clean.title().strip())  # Format it back into a title
                            score = analyzer.polarity_scores(text)
                            compound_scores.append(score['compound'])
        if potential_winners:
            winners.append(mode(potential_winners))  # Append the most common thing associated with award
            positivity.append(sum(compound_scores) / len(compound_scores))
            controversy.append(np.var(compound_scores))
            return True
        else:
            return False

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here

    f = open('gg2015.json')
    data = json.load(f)

    textfile = open("clean_person_entities.txt", "w")

    for tweet in data:
        text = tweet['text']
        if "RT @" in text:
            continue
        if 'best' not in text.lower():
            continue
        textfile.write(text + "\n")

    textfile.close()

    textfile = open("clean_non_person_entities.txt", "w")

    for tweet in data:
        text = tweet['text']
        if "RT @" in text or 'actor' in text.lower() or 'actress' in text.lower() or 'wins' not in text.lower():
            continue
        textfile.write(text + "\n")
        
    textfile.close()
    
    textfile = open("clean_actor_and_actress_only.txt", "w")

    for tweet in data:
        text = tweet['text']
        if "RT @" in text or 'best' not in text.lower():
            continue
        if 'actor' not in text.lower() and 'actress' not in text.lower():
            continue
        textfile.write(text + "\n")

    textfile.close()

    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    return

if __name__ == '__main__':
    # main()
    get_winner(2019)
