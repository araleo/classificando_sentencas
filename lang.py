from operator import itemgetter
import math
import nltk
import os
import string
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file)) as f:
            files[file] = f.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = list()
    tokens = nltk.word_tokenize(document)
    for token in tokens:
        if (token not in string.punctuation
                and token not in nltk.corpus.stopwords.words("portuguese")):
            words.append(token.lower())
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    words_lists = documents.values()

    # for each list of words in the dictionary
    for words in words_lists:

        # for each word in that list
        for word in words:

            # if that word is not already in the output
            if word not in idfs:

                # count in how many other documents it appears
                doc_count = 0
                for x in words_lists:
                    if word in x:
                        doc_count += 1

                idfs[word] = math.log(len(words_lists) / doc_count)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict()

    # for each file
    for name, content in files.items():

        # sets the initial tf-idf of that file as 0
        idf = 0

        # for each word in query:
        for word in query:

            # counts how many instances of word in each file
            # and calculates the tf-idf value
            c = content.count(word)
            idf += c * idfs[word]

        # updates the tf-idf dictionary
        tf_idfs[name] = idf

    filenames = sorted(tf_idfs, key=tf_idfs.get, reverse=True)
    return filenames[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_idfs_qtds = list()

    for sentence, words in sentences.items():
        idf = 0
        count = 0
        for word in query:
            if word in words:
                idf += idfs[word]
                count += 1
        qtd = count / len(words)
        sentences_idfs_qtds.append((sentence, idf, qtd))

    top = sorted(sentences_idfs_qtds, key=itemgetter(1, 2), reverse=True)
    top = [x[0] for x in top]
    return top[:n]


if __name__ == "__main__":
    main()
