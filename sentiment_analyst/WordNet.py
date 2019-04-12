import nltk
from nltk.corpus import wordnet

# nltk.download('wordnet')

positive = []
negative = []

for w in ["good", "great", "fantastic", "nice", "cool"]:
    for syn in wordnet.synsets(w):
        for l in syn.lemmas():
            positive.append(l.name())
            if l.antonyms():
                negative.append(l.antonyms()[0].name())

for w in ["bad", "dull", "ugly", "disappoint"]:
    for syn in wordnet.synsets(w):
        for l in syn.lemmas():
            negative.append(l.name())
            if l.antonyms():
                positive.append(l.antonyms()[0].name())

print(set(positive))
print("\n")
print(set(negative))

print(len(set(positive)))
print(len(set(negative)))
