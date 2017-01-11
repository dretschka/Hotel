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
sparse_tfidf_vectors = {}
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
                 "Finished writing \"" + filename + "\" file. \n")
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
    logging.info("[" + t + "]  Done! \n")

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
    logging.info("[" + t + "]  Done! \n")

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
    logging.info("[" + t + "]  Done! \n")

    return


# Computes the sparse tfidf vector for an article and stores
# it in a global dictionary together with its euclidean
# length as a tuple
# We don't do this in the calculateCosineSimilarity method
# because we only want to compute the vector for every article once
# since this improves performance dramatically.
def compute_sparse_tfidf_vector(article_id):
    global sparse_tfidf_vectors
    a = article_dic[article_id]

    # Calculate the vector for the given article
    article_vector = np.zeros(len(document_freq))
    for term, tfidf in a.items():
        # Get the vector corresponding to the current word
        vec = word_vector[term]
        # Multiply vector with tfidf
        article_vector += vec * tfidf

    sparse_tfidf_vectors[article_id] = (article_vector, np.linalg.norm(article_vector))

    return


# Iterates of a list of article ids and computes its sparse vectors
def compute_sparse_tfidf_vector_from_list(article_list):
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Computing sparse vectors ...")

    for i in range(0, len(article_list)):
        compute_sparse_tfidf_vector(article_list[i])

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Done!")

    return


def calculateCosineSimilarity(tfIdfDict1, tfIdfDict2):
    vector1 = tfIdfDict1[0]
    vector2 = tfIdfDict2[0]

    # Get the dot product of the vectors
    dot = vector1.dot(vector2)

    # Get the length of both vectors
    length_vector1 = tfIdfDict1[1]
    length_vector2 = tfIdfDict2[1]

    # Some articles are emtpy. If this is the case, mark it
    if length_vector1 == 0 or length_vector2 == 0:
        return -1

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

        # Some articles are emtpy. If this is the case, skip it.
        if len(i_article) == 0: continue

        for j in range(0, i):
            j_article = create_set(df1.loc[articles[j]].text)

            # Some articles are emtpy. If this is the case, skip it.
            if len(j_article) == 0: continue

            jaccard = calcJaccardSimilarity(i_article, j_article)
            matrix[i, j] = jaccard

        # Logging
        if i % 10 == 0:
            t = str(round((time.time() - start_time), 2))
            logging.info("[" + t + "] Finished " + str(i) + "% of all articles")

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Done! \n")

    return matrix


def compute_cosine_similarity_of_all_articles(articles):
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Compute cosine similarities "
                           "of all articles ...")

    matrix = np.zeros(shape=(100, 100))

    # First compute the sparse vectors for each article in the list
    compute_sparse_tfidf_vector_from_list(articles)

    # Compute every possible combination of articles. We only need to
    # calculate the similarity once per pair and we do
    # not need to calculate the similarity of the article with itself.
    for i in range(0, len(articles)):
        i_vec = sparse_tfidf_vectors[articles[i]]

        for j in range(0, i):
            j_vec = sparse_tfidf_vectors[articles[j]]

            cos_sim = calculateCosineSimilarity(i_vec, j_vec)
            # Store the cosine similarity in a matrix
            matrix[i, j] = cos_sim

        # Logging
        if i % 10 == 0:
            t = str(round((time.time() - start_time), 2))
            logging.info("[" + t + "] Finished " + str(i) + "% of all articles")

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Done! \n")

    return matrix


def compute_jaccard_similarity_for_outlinks_of_all_articles(articles):
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Compute jaccard similarities for outlinks "
                           "of all articles ...")

    matrix = np.zeros(shape=(100, 100))

    # Compute every possible combination of articles. We only need to
    # calculate the similarity once per pair and we do
    # not need to calculate the similarity of the article with itself.
    for i in range(0, len(articles)):
        i_article = set(df2.loc[articles[i]].out_links)

        # Some articles are emtpy. If this is the case, skip it.
        if len(i_article) == 0: continue

        for j in range(0, i):
            j_article = set(df2.loc[articles[j]].out_links)

            # Some articles are emtpy. If this is the case, skip it.
            if len(j_article) == 0: continue

            jaccard = calcJaccardSimilarity(i_article, j_article)
            matrix[i, j] = jaccard

        # Logging
        if i % 10 == 0:
            t = str(round((time.time() - start_time), 2))
            logging.info("[" + t + "] Finished " + str(i) + "% of all articles")

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Done! \n")

    return matrix


def pretty_print_matrix(matrix):
    for i in range(0, 100):
        for j in range(0, 100):
            print("%1.3f|" % (matrix[i, j]), end='')
        print()


def main():
    global start_time, df1, df2, article_dic
    # Set start time
    start_time = time.time()

    # Reset log file
    with open('similarity.log', 'w'):
        pass

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started --- \n")

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

    print("Jaccard Similarity of Germany and Europe: " +
          str(calcJaccardSimilarity(word_set_germany, word_set_europe)))

    # ----------------------------------------------#
    # 1.1.2 Calculate the cosine similarity for the #
    # article "Germany" and "Europe"                #
    # ----------------------------------------------#
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started calculations for 1.1.2 ---")

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

    # Create sparse vectors for each article
    compute_sparse_tfidf_vector_from_list([ger_id, eur_id])

    # Calculate the cosine similarity of both articles
    cos_sim = calculateCosineSimilarity(sparse_tfidf_vectors[ger_id],
                                        sparse_tfidf_vectors[eur_id])

    print("Cosine Similarity for Germany and Europe: " + str(cos_sim))

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Finished calculations for 1.1.2 --- \n")

    # --------------------------#
    # 1.2 Similarity of graphs  #
    # --------------------------#
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started calculations for 1.2 ---")

    germany_outlinks = set(df2[df2.name == "Germany"].out_links.values[0])
    europe_outlinks = set(df2[df2.name == "Europe"].out_links.values[0])
    outlinks_jaccard_sim = calcJaccardSimilarity(germany_outlinks,
                                                  europe_outlinks)

    print("Jaccard Similarity of outlinks of Germany and Europe: "
          + str(outlinks_jaccard_sim))

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Finished calculations for 1.2 --- \n")

    # --------------------------#
    # 1.4 Implement the measure #
    # --------------------------#
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started calculations for 1.4 ---")

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started calculations "
                           "for the 100 longest articles --- \n")
    # Find the 100 longest articles
    l_articles = get_longest_articles()

    jaccard_matrix = compute_jaccard_similarity_of_all_articles(l_articles)
    print("\n\n ---------- JACCARD MATRIX ---------- \n\n")
    pretty_print_matrix(jaccard_matrix)

    cosine_matrix = compute_cosine_similarity_of_all_articles(l_articles)
    print("\n\n ---------- COSINE MATRIX ---------- \n\n")
    pretty_print_matrix(cosine_matrix)

    jaccard_outlinks_matrix = compute_jaccard_similarity_for_outlinks_of_all_articles(l_articles)
    print("\n\n ---------- JACCARD MATRIX FOR OUTLINKS ---------- \n\n")
    pretty_print_matrix(jaccard_outlinks_matrix)

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Started calculations "
                           "for 100 random articles --- \n")

    # Find 100 random articles
    r_articles = get_random_articles()
    jaccard_matrix = compute_jaccard_similarity_of_all_articles(r_articles)
    print("\n\n ---------- JACCARD MATRIX ---------- \n\n")
    pretty_print_matrix(jaccard_matrix)

    cosine_matrix = compute_cosine_similarity_of_all_articles(r_articles)
    print("\n\n ---------- COSINE MATRIX ---------- \n\n")
    pretty_print_matrix(cosine_matrix)

    jaccard_outlinks_matrix = compute_jaccard_similarity_for_outlinks_of_all_articles(r_articles)
    print("\n\n ---------- JACCARD MATRIX FOR OUTLINKS ---------- \n\n")
    pretty_print_matrix(jaccard_outlinks_matrix)

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Finished calculations for 1.4 --- \n")

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] --- Finished ---")

    exit(1)

if __name__ == '__main__':
    main()
