import json
import bz2
import csv
import string
from collections import Counter
from nltk import ngrams
from tqdm import tqdm

with bz2.open('10K.github.jsonl.bz2', 'rt') as f:
    data = [json.loads(line) for line in f]

push_events = [d for d in data if d['type'] == 'PushEvent']

author_3grams = {}

for event in tqdm(push_events):
    author = event['actor']['login']

    commits = event['payload']['commits']
    if len(commits) > 0:
        message = commits[0]['message']
        message = message.lower().translate(str.maketrans('', '', string.punctuation))

        three_grams = ngrams(message.split(), 3)
        print(three_grams)
        if author in author_3grams:
            author_3grams[author].update(three_grams)
        else:
            author_3grams[author] = Counter(three_grams)

top_five_3grams = {}
for author, ngram_counts in author_3grams.items():
    top_five_3grams[author] = [' '.join(ngram) for ngram, count in ngram_counts.most_common(5)]

with open('top_5_3grams.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['author', 'first 3-gram', 'second 3-gram', 'third 3-gram', 'fourth 3-gram', 'fifth 3-gram'])
    for author, ngrams in top_five_3grams.items():
        if ngrams:
            writer.writerow(["[" + author + "]:"] + ngrams)
