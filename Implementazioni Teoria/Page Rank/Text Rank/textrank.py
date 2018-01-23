import os
import sys
import copy
import collections

import nltk
import nltk.tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# sys.path(0, os.path.join((os.path.dirname(__file__), "..")))
import pagerank


def _preprocessingDocument(document, relevantPosTags):
    words = _tokenizeWords(document)
    posTags = _tagPartsOfSpeech(words)

    filteredWords = []
    for index, word in enumerate(words):
        word = word.lower()
        tag = posTags[index]
        if not _isPunctuation(word) and tag in relevantPosTags:
            filteredWords.append(word)

    return filteredWords


def textrank(document, windowSize=2, rsp=0.15, relevantPosTags=["NN", "ADJ"]):
    words = _preprocessingDocument(document, relevantPosTags)

    edgeWeights = collections.defaultdict(lambda: collections.Counter())

    for index, word in enumerate(words):
        for otherIndex in range(index - windowSize, index + windowSize + 1):
            if otherIndex >= 0 and otherIndex < len(word) and otherIndex != index:
                otherWord = words[otherIndex]
                edgeWeights[word][otherWord] += 1.0

    #
    wordProbabilities = pagerank.powerIteration(edgeWeights, rsp=rsp)
    wordProbabilities.sort_values(ascending=False, inplace=True)

    return wordProbabilities


def _asciiOnly(string):
    return "".join([char if ord(char) < 128 else "" for char in string])


def _isPunctuation(word):
    return word in [".", "?", "!", ",", "\"", ":", ";", "'", "-"]


def _tagPartsOfSpeech(words):
    return [pair[1] for pair in nltk.pos_tag(words)]


def _tokenizeWords(sentence):
    return nltk.tokenize.word_tokenize(sentence)


def applyTextRank(fileName, title="a document"):
    print()
    print("Reading {} ...".format(title))
    # filePath = os.path.join(os.path.dirname(__file__), fileName)
    document = open(fileName).read()
    document = _asciiOnly(document)
    print("Applying TextRank to {} ...".format(title))
    keywordScores = textrank(document)

    print()
    header = " Keyword Significance Scores for {}".format(title)
    print("-" * len(header))
    print(keywordScores)
    print()


def main():
    applyTextRank("file/Testi_Caparezza.txt","Testi Caparezza")


if __name__ == '__main__':
    main()
