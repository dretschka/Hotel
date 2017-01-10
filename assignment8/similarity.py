# assignment 8
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import logging
import time
import pandas as pd
import re
import numpy as np
from numpy import zeros
import operator
np.set_printoptions(threshold=np.nan)


document_freq = {}
word_vector = {}
article_dic = {}
df1 = pd.DataFrame()
df2 = pd.DataFrame()

# Configure logging and set start time
logging.basicConfig(filename='similarity.log', level=logging.DEBUG)
start_time = 0


# Read the given file into a string
def read_file(file):
    with open(file) as f:
        data = f.read().replace('\n', '')
    return data


# Write a file
def write_file(filename, generated_string):
    with open(filename, 'w') as f:
        f.write(generated_string)

    t = str(round((time.time() - start_time), 2)).zfill(5)
    logging.info("[" + t + "] " +
                 "Finished writing \"" + filename + "\" file. \n\n")
    return


def create_set(s):
    regex = re.compile("\w+")
    s_list = regex.findall(s)
    word_set = set()

    for s in s_list:
        word_set.add(s.lower())

    return word_set


def calc_term_freq(s):
    regex = re.compile("\w+")
    s_list = regex.findall(s)
    word_rank = {}

    for s in s_list:
        s = s.lower()
        try:
            # Increase count by one
            word_rank[s] += 1
        except KeyError:
            # Create new dictionary entry for terms that
            # are not part of the dict yet
            word_rank[s] = 1

    return word_rank


def calc_document_freq(s):
    # create set of the given string in order to get only one
    # occurrence of each word

    s_set = create_set(s)

    for s in s_set:
        try:
            # Increase count by one
            document_freq[s] += 1
        except KeyError:
            # Create new dictionary entry for chars that
            # are not part of the dict. yet
            document_freq[s] = 1
    return


def calcJaccardSimilarity(wordset1, wordset2):
    intersection = wordset1.intersection(wordset2)
    union = wordset1.union(wordset2)

    jac = len(intersection) / len(union)
    return jac


# Compute the document frequency and store it in global
# dictionary document_freq
def log_doc_freq():
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Compute document frequency ...")

    df1.text.apply(calc_document_freq)

    # sorted_x = sorted(document_freq.items(), key=operator.itemgetter(1))
    # for k, v in sorted_x:
    #     print(str(v) + " | " + k)

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Done! \n\n")

    return


# tfidf(word, document) = tf(word, document) * log(|D| / df(word))
def calc_tfidf(term, term_freq):
    # 1: term frequency of the word in document
    # 2: Amount of Documents
    amount_of_documents = len(df1)

    if len(document_freq) == 0:
        logging.error("document_freq dictionary is empty!")
        exit()

    # 3: document frequency of the term
    document_freq_word = document_freq[term]

    tfidf = term_freq * np.log(amount_of_documents / document_freq_word)

    return tfidf


def create_dic_of_all_article_with_terms():
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Compute tfidf dictionary ...")

    dic = {}

    # Iterate over df1
    for i in range(0, len(df1)):
        articles_dic = {}
        word_rank_dic = calc_term_freq(df1.loc[i].text)

        # Iterate over the word rank dictionary of the article df1.loc[i]
        for k, v in word_rank_dic.items():
            # Store each word as key in the article_dic and the
            # tfidf of the word as value
            articles_dic[k] = calc_tfidf(k, v)

        # Store the resulting article_dic as a value and the
        # article id as a key in the dic dictionary
        dic[i] = articles_dic

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Done! \n\n")

    return dic


# Generate a dictionary with a unique vector for each word
def create_word_vectors():
    global word_vector

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Compute word vectors ...")

    # Get the amount of all words in all documents
    l = len(document_freq)
    i = 0

    for k, v in document_freq.items():
        v = zeros(l)
        v[i] = 1
        word_vector[k] = v
        i += 1

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Done! \n\n")

    return


def calculateCosineSimilarity(tfIdfDict1, tfIdfDict2):
    # Calculate the vector for tfIdfDict1
    article_vector1 = np.zeros(len(document_freq))
    for term, tfidf in tfIdfDict1.items():
        # Get the vector corresponding to the current word
        vec = word_vector[term]
        # Multiply vector with tfidf
        article_vector1 += vec * tfidf

    # Calculate the vector for tfIdfDict2
    article_vector2 = np.zeros(len(document_freq))
    for term, tfidf in tfIdfDict2.items():
        # Get the vector corresponding to the current word
        vec = word_vector[term]
        # Multiply vector with tfidf
        article_vector2 += vec * tfidf

    # Get the dot product of the vectors
    dot = article_vector1.dot(article_vector2)

    # Get the length of both vectors
    length_vector1 = np.linalg.norm(article_vector1)
    length_vector2 = np.linalg.norm(article_vector2)

    # Inverse cosine of the dot product divided by the product of
    # the length of both vectors
    cosine_sim = dot / (length_vector1*length_vector2)

    return cosine_sim


# Calculate the length of all articles and choose the longest ones
def get_longest_articles():
    l = []

    # Iterate over df1 and append a tuple to the list l
    # The tuple contains the index of the text combined with its length
    for i in range(0, len(df1)):
        l.append((i, len(df1.loc[i].text)))

    # Sort the list by text-length descending in place
    l.sort(key=lambda tup: tup[1], reverse=True)

    # Generate list with 100 entries containing only the article ids
    l2 = []
    for i in range(0, 100):
        l2.append(l[i][0])

    return l2


# Select 100 random articles
def get_random_articles():
    l = []

    for i in range(0, 100):
        l.append(np.random.choice(df1.index, replace=False))

    return l


def compute_jaccard_similarity_of_all_articles(articles):
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Compute jaccard similarities "
                           "of all articles ...")

    matrix = np.zeros(shape=(100, 100))

    # Compute every possible combination of articles. We only need to
    # calculate the similarity once per pair and we do
    # not need to calculate the similarity of the article with itself.
    for i in range(0, len(articles)):
        i_article = create_set(df1.loc[articles[i]].text)

        for j in range(0, i):
            j_article = create_set(df1.loc[articles[j]].text)

            jaccard = calcJaccardSimilarity(i_article, j_article)
            matrix[i, j] = jaccard

        if i % 10 == 0:
            logging.info("i: " + str(i))

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Done! \n\n")

    return matrix


def compute_cosine_similarity_of_all_articles(articles):
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Compute cosine similarities "
                           "of all articles ...")

    matrix = np.zeros(shape=(100, 100))

    # Compute every possible combination of articles. We only need to
    # calculate the similarity once per pair and we do
    # not need to calculate the similarity of the article with itself.
    for i in range(0, len(articles)):
        i_article = article_dic[articles[i]]

        for j in range(0, i):
            j_article = article_dic[articles[j]]

            cos_sim = calculateCosineSimilarity(i_article, j_article)
            matrix[i, j] = cos_sim

        if i % 10 == 0:
            logging.info("i: " + str(i))

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Done! \n\n")

    return matrix


def pretty_print_matrix(matrix):
    for i in range(0, 100):
        for j in range(0, 100):
            print("%1.3f|" % (matrix[i, j]), end='')
        print()


def main():
    # Set start time
    global start_time, df1, df2, article_dic
    start_time = time.time()

    # Reset log file
    with open('similarity.log', 'w'):
        pass

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started --- \n\n")

    store = pd.HDFStore('store2.h5')
    df1 = store['df1']
    df2 = store['df2']

    # ------------------------------------------------#
    # 1.1.1 Calculate the Jaccard coefficient for the #
    # articles "Germany" and "Europe"                 #
    # ------------------------------------------------#
    word_set_germany = create_set(
        str(df1[df1.name == 'Germany'].text.values[0]))
    word_set_europe = create_set(
        str(df1[df1.name == 'Europe'].text.values[0]))
    print(calcJaccardSimilarity(word_set_germany, word_set_europe))

    # ----------------------------------------------#
    # 1.1.2 Calculate the cosine similarity for the #
    # article "Germany" and "Europe"                #
    # ----------------------------------------------#
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started calculations for 1.1.2 --- \n\n")

    # Compute the document frequency and store it in
    # global dictionary document_freq
    log_doc_freq()

    # Compute a dictionary with the article id as key and
    # a dictionary for each article containing the article terms
    # and the corresponding tfidf values as value
    article_dic = create_dic_of_all_article_with_terms()

    # Compute a dictionary to match a unique vector to a specific word.
    # This is done before calculating the cosine similarity
    # so this only has to be executed once
    create_word_vectors()

    # Get ID of the article "Germany" and "Europe"
    ger_id = df1[df1.name == "Germany"].index[0]
    eur_id = df1[df1.name == "Europe"].index[0]

    # Calculate the cosine similarity of both articles
    cos_sim = calculateCosineSimilarity(article_dic[ger_id],
                                        article_dic[eur_id])
    print(cos_sim)

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Finished calculations for 1.1.2 --- \n\n")

    # --------------------------#
    # 1.2 Similarity of graphs  #
    # --------------------------#
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started calculations for 1.2 --- \n\n")

    germany_outlinks = set(df2[df2.name == "Germany"].out_links.values[0])
    europe_outlinks = set(df2[df2.name == "Europe"].out_links.values[0])
    outlinks_jaccard_sim =  calcJaccardSimilarity(germany_outlinks,
                                                  europe_outlinks)
    print(outlinks_jaccard_sim)

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Finished calculations for 1.2 --- \n\n")

    # --------------------------#
    # 1.4 Implement the measure #
    # --------------------------#
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started calculations for 1.4 --- \n\n")

    # Find the 100 longest articles
    l_articles = get_longest_articles()

    jaccard_matrix = compute_jaccard_similarity_of_all_articles(l_articles)
    pretty_print_matrix(jaccard_matrix)

    cosine_matrix = compute_cosine_similarity_of_all_articles(l_articles)
    pretty_print_matrix(cosine_matrix)

    # Find 100 random articles
    #r_articles = get_random_articles()
    #compute_similarity()

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Finished calculations for 1.4 --- \n\n")

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Finished --- \n\n")


if __name__ == '__main__':
    main()
