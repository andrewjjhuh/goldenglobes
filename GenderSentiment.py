import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import numpy as np

def gender_count():
    male_awards = []
    female_awards = []

    with open('clean_actor_and_actress_only.txt') as f:
        for text in f:
            if 'best actor' in text.lower() or 'best performance by an actor' in text.lower():
                male_awards.append(text)
            elif 'best actress' in text.lower() or 'best performance by an actress' in text.lower():
                female_awards.append(text)

    male_count = len(male_awards)
    female_count = len(female_awards)

    print("There were " + str(male_count) + " tweets about male categories this year or " + str(round((male_count*100/(male_count + female_count)), 2)) + "% of the gendered category conversation.")
    print("There were " + str(female_count) + " tweets about female categories this year or " + str(round((female_count*100/(male_count + female_count)), 2)) + "% of the gendered category conversation.")

    nltk.download('vader_lexicon')
    analyzer = SentimentIntensityAnalyzer()

    male_result = {'pos': 0, 'neg': 0, 'neu': 0}
    female_result = {'pos': 0, 'neg': 0, 'neu': 0}
    male_compound = []
    female_compound = []

    for text in male_awards:
        new_text = re.compile(re.escape('best actor'), re.IGNORECASE)
        new_text = new_text.sub('', text)
        score = analyzer.polarity_scores(new_text)
        if score['compound'] > 0.05:
            male_result['pos'] += 1
        elif score['compound'] < -0.05:
            male_result['neg'] += 1
        else:
            male_result['neu'] += 1
        male_compound.append(score['compound'])

    for text in female_awards:
        new_text = re.compile(re.escape('best actress'), re.IGNORECASE)
        new_text = new_text.sub('', text)
        score = analyzer.polarity_scores(new_text)
        if score['compound'] > 0.05:
            female_result['pos'] += 1
        elif score['compound'] < -0.05:
            female_result['neg'] += 1
        else:
            female_result['neu'] += 1
        female_compound.append(score['compound'])

    male_avg = sum(male_compound)/len(male_compound)
    female_avg = sum(female_compound)/len(female_compound)

    male_variance = np.var(male_compound)
    female_variance = np.var(female_compound)

    print("The average sentiment of tweets about male categories is given a score of " + str(round(male_avg*100, 2)) + " on a -100 to 100 negativity to positivity scale")
    print("The average sentiment of tweets about female categories is given a score of " + str(round(female_avg*100, 2)) + " on a -100 to 100 negativity to positivity scale")

    print("The variance in sentiment of tweets about male categories is " + str(male_variance))
    print("The variance in sentiment of tweets about female categories is " + str(female_variance))

    if male_avg > female_avg:
        if male_variance > female_variance:
            print("So in general, tweets about male categories are generally more positive, with more variance in sentiment as well")
        else:
            print("So in general, tweets about male categories are generally more positive, with less variance in sentiment")
    else:
        if female_variance > male_variance:
            print("So in general, tweets about female categories are generally more positive, with more variance in sentiment as well")
        else:
            print("So in general, tweets about female categories are generally more positive, with less variance in sentiment")
            
def clean_json():
    textfile = open("clean_actor_and_actress_only.txt", "w")

    f = open('gg2015.json')
    data = json.load(f)

    for tweet in data:
        text = tweet['text']
        if "RT @" in text or 'best' not in text.lower():
            continue
        if 'actor' not in text.lower() and 'actress' not in text.lower():
            continue
        textfile.write(text + "\n")

    textfile.close()
            
if __name__ == '__main__':
    gender_count()
