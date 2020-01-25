# imports
import urllib.request  # get websites
from bs4 import BeautifulSoup  # parse HTML
from nltk.corpus import stopwords, wordnet  # nlp
from nltk.tokenize import sent_tokenize, word_tokenize


def analyse(url, testWord):
    # vars
    goodCount, badCount = 0, 0  # reset counts
    testWord.lower()  # word to test


    # defs
    def synFind(w, type):  # find synonyms/antonyms of a given word w
        nyms = []  # reset nyms

        if type == "s":  # for synonyms
            for synset in wordnet.synsets(w):
                for lemma in synset.lemmas():
                    nyms.append(lemma.name())  # add synonyms to nyms

        elif type == "a":  # for antonyms
            for synset in wordnet.synsets(w):
                for lemma in synset.lemmas():
                    nyms.append(lemma.antonyms().name())  # add antonyms to nyms

        return nyms


    def synList(w, type):
        l = []  # reset l
        l.append(w)  # append original word to l

        for synonym in synFind(w, type):  # for each synonym of w
            if synonym not in l:  # if new
                l.append(synonym)  # append to l

            if w in synFind(synonym, type):  # if the original word is a synonym of the synonym
                for synSyn in synFind(synonym, type):  # for each synonym of the synonym
                    if synSyn not in l:  # if new
                        l.append(synSyn)  # append to l

        return l


    response = urllib.request.urlopen(url)  # get html
    soup = BeautifulSoup(response.read(), "html5lib")  # remove html tags
    text = soup.get_text(strip=True)  # i can't remember what this line does but it doesn't work without it

    words = word_tokenize(text)
    for word in words:  # for each word
        word.lower()  # make lowercase

    wordCount = words.count(testWord)


    sentences = sent_tokenize(text)  # separate into sentences
    for sentence in sentences:  # for each sentence
        words = word_tokenize(sentence)  # separate into words

        for i in range(len(sentence)):
            sentence[i].lower()

        for word in synList("good", "s"):  # for every word in goodSyns
            if testWord in words and word in words:  # if testWord and synSyn are both in the sentence
                goodCount += 1  # increase goodCount

        for word in synList("bad", "s"):  # same for "bad"
            if testWord in words and word in words:
                badCount += 1  # increase badCount


    total = goodCount + badCount  # find percentages
    if total > 0:
        goodPerc = round((goodCount / total) * 100, 2)
        badPerc = round((badCount / total) * 100, 2)
    else:
        goodPerc, badPerc = -1, -1

    return {
    "good": goodPerc,
    "bad": badPerc
    }
