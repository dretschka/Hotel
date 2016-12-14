# assignment 7 task 2
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

# matplotlib to plot the required data
import matplotlib.pyplot as plt
# logging for debug purposes
import logging
# random to generate random numbers for the sampling process
import random
# operator for creating sorted lists from dictionaries
import operator
# time for debug purposes
import time
# regex to reliably separate a string into words
import re

# Configure logging and set start time
logging.basicConfig(filename='charCounter.log', level=logging.DEBUG)
start_time = 0

# Provided probabilities
zipf_probabilities = {' ': 0.17840450037213465, '1': 0.004478392057619917, '0': 0.003671824660673643,
                      '3': 0.0011831834225755678, '2': 0.0026051307175779174, '5': 0.0011916662329062454,
                      '4': 0.0011108979455528355, '7': 0.001079651630435706, '6': 0.0010859164582487295,
                      '9': 0.0026071152282516083, '8': 0.0012921888323905763, '_': 2.3580656240324293e-05,
                      'a': 0.07264712490903191, 'c': 0.02563767289222365, 'b': 0.013368688579962115,
                      'e': 0.09688273452496411, 'd': 0.029857183586861923, 'g': 0.015076820473031856,
                      'f': 0.017232219565845877, 'i': 0.06007894642873102, 'h': 0.03934894249122837,
                      'k': 0.006067466280926215, 'j': 0.0018537015877810488, 'm': 0.022165129421030945,
                      'l': 0.03389465109649857, 'o': 0.05792847618595622, 'n': 0.058519445305660105,
                      'q': 0.0006185966212395744, 'p': 0.016245321110753712, 's': 0.055506530071283755,
                      'r': 0.05221605572640867, 'u': 0.020582942617121572, 't': 0.06805204881206219,
                      'w': 0.013964469813783246, 'v': 0.007927199224676324, 'y': 0.013084644140464391,
                      'x': 0.0014600810295164054, 'z': 0.001048859288348506}
uniform_probabilities = {' ': 0.1875, 'a': 0.03125, 'c': 0.03125, 'b': 0.03125, 'e': 0.03125, 'd': 0.03125,
                         'g': 0.03125, 'f': 0.03125, 'i': 0.03125, 'h': 0.03125, 'k': 0.03125, 'j': 0.03125,
                         'm': 0.03125, 'l': 0.03125, 'o': 0.03125, 'n': 0.03125, 'q': 0.03125, 'p': 0.03125,
                         's': 0.03125, 'r': 0.03125, 'u': 0.03125, 't': 0.03125, 'w': 0.03125, 'v': 0.03125,
                         'y': 0.03125, 'x': 0.03125, 'z': 0.03125}


# Read the given file into a string
def read_file(file):
    with open(file) as f:
        data = f.read().replace('\n', '')
    return data


# Write a file
def write_file(filename, generated_string):
    with open(filename, 'w') as f:
        f.write(generated_string)

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] " +
                 "Finished writing \"" + filename + "\" file. \n\n")
    return


# Iterate through the string and count the characters as well
# as the occurrence of each character
def count_chars(data):
    count = 0
    char_dict = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0,
                 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0,
                 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0,
                 'y': 0, 'z': 0, ' ': 0, '0': 0, '1': 0, '2': 0,
                 '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}

    for i in range(0, len(data)):
        try:
            # Increase count by one
            char_dict[data[i].lower()] += 1
            count += 1
        except KeyError:
            # Ignore chars that are not part of the dictionary
            continue

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] " + "Finished counting the chars. Found "
                 + str(count) + " chars.\n\n")
    return count, char_dict


# Calculate the relative values of a given total
# and a dictionaries of absolute counts
def calculate_percentage(count, char_dict):
    rel_char = {}

    for key, value in char_dict.items():
        rel_char[key] = value / count

    return rel_char


# Cumulative sum up relative values
def cumulative_distribution(rel_char):
    c_distri = []
    sum_percentage = 0

    # Sort the rel_char dictionary by value
    sorted_rel_char = sorted(rel_char.items(),
                             key=operator.itemgetter(1), reverse=True)

    for key, value in sorted_rel_char:
        x = sum_percentage + value
        c_distri.append((key, x))
        sum_percentage = x

    return c_distri


# Sample the data
def sample_data(count, rel_char):
    generated_string = ""
    c_distri = cumulative_distribution(rel_char)

    for i in range(0, count):
        r = random.random()
        for key, value in c_distri:
            # Find lowest value bigger than r
            if r <= value:
                generated_string += key
                break

        # Occasionally log progress
        if i % 10000000 == 0:
            t = str(round((time.time() - start_time), 2))
            logging.info("[" + t + "] " + "Calculated " + str(i) + " chars")

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " + "Finished sampling process\n\n")

    return generated_string


# Calculate the word rank by counting the occurrence of each word
def count_word_rank(s):
    regex = re.compile("\w+")
    s_list = regex.findall(s)
    word_rank = {}

    for s in s_list:
        try:
            # Increase count by one
            word_rank[s] += 1
        except KeyError:
            # Create new dictionary entry for chars that
            # are not part of the dict. yet
            word_rank[s] = 1

    sorted_word_rank = sorted(word_rank.items(),
                              key=operator.itemgetter(1), reverse=True)

    return sorted_word_rank


# Calculate word rank probability as well as the cumulative probability
def wr_probability(word_rank):
    s = 0
    word_rank_probability = []
    c = 0
    cumulative_word_rank_probability = []

    for word in word_rank:
        s += word[1]

    # Calculate probability
    for word in word_rank:
        word_rank_probability.append((word[0], (word[1]/s)))

    # Cumulative probability
    for word in word_rank_probability:
        c += word[1]
        cumulative_word_rank_probability.append((word[0], c))

    return word_rank_probability, cumulative_word_rank_probability


# Determine the maximum pointwise distance
def maximum_pwd(wr_x_probability, wr_data_probability):
    max_pwd = 0

    for i in range(0, min(len(wr_x_probability), len(wr_data_probability))):
        pwd = abs(wr_data_probability[i][1] - wr_x_probability[i][1])
        if pwd > max_pwd:
            max_pwd = pwd
    return max_pwd


# Draw the plots
def draw_wrf(word_rank_data, word_rank_zipf, word_rank_uniform, slogx):

    temp_word_rank_data = []
    temp_word_rank_zipf = []
    temp_word_rank_uniform = []

    for word in word_rank_data:
        temp_word_rank_data.append(word[1])

    for word in word_rank_zipf:
        temp_word_rank_zipf.append(word[1])

    for word in word_rank_uniform:
        temp_word_rank_uniform.append(word[1])

    if not slogx:
        plt.loglog(temp_word_rank_data, 'r',
                   label='Simple English Wikipedia WR')
        plt.loglog(temp_word_rank_zipf, 'b',
                   label='ZIPF WR')
        plt.loglog(temp_word_rank_uniform, 'g',
                   label='Uniform WR')
        plt.title("word rank frequency diagram")
        plt.xlabel("word rank")
        plt.ylabel("frequency")
    else:
        plt.semilogx(temp_word_rank_data, 'r',
                     label='Simple English Wikipedia WR')
        plt.semilogx(temp_word_rank_zipf, 'b',
                     label='ZIPF WR')
        plt.semilogx(temp_word_rank_uniform, 'g',
                     label='Uniform WR')
        plt.title("CDF Plot")
        plt.xlabel("word rank")
        plt.ylabel("cumulative relative frequency")

    plt.legend(loc=0)
    plt.margins(0.2)
    plt.show()


def main():
    global start_time

    # Delete content of log file
    with open('charCounter.log', 'w'):
        pass

    start_time = time.time()

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Starting :) \n\n")

    # Count characters and spaces in the simple english wikipedia
    file = "simple-20160801-1-article-per-line"
    data = read_file(file)
    count, char_dict = count_chars(data)

    # Sample the ZIPF distribution and store the result in an file
    generated_string_zipf = sample_data(count, zipf_probabilities)
    write_file('generated_zipf.txt', generated_string_zipf)

    # Sample the Uniform distribution and store the result in an file
    generated_string_uniform = sample_data(count, uniform_probabilities)
    write_file('generated_uniform.txt', generated_string_uniform)

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  START WORD RANK CALCULATING \n\n")

    # Count the resulting words from the provided data set and
    # from the generated text
    word_rank_data = count_word_rank(data)
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " +
                 str(word_rank_data[:30]) + "\n\n")

    word_rank_zipf = count_word_rank(generated_string_zipf)
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " +
                 str(word_rank_zipf[:30]) + "\n\n")

    word_rank_uniform = count_word_rank(generated_string_uniform)
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " +
                 str(word_rank_uniform[:30]) + "\n\n")

    # Draw the Word Rank Frequency Diagram
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " +
                 "Drawing the Word Rank Frequency Diagram ... \n\n")
    draw_wrf(word_rank_data, word_rank_zipf, word_rank_uniform, False)

    # Calculate the word rank and the word probability for each data set
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " + "Calculating the WR ... \n\n")
    word_rank_data = count_word_rank(data)
    wr_data_probability, cwr_data_probability = \
        wr_probability(word_rank_data)

    word_rank_zipf = count_word_rank(generated_string_zipf)
    wr_zipf_probability, cwr_zipf_probability = \
        wr_probability(word_rank_zipf)

    word_rank_uniform = count_word_rank(generated_string_uniform)
    wr_uniform_probability, cwr_uniform_probability = \
        wr_probability(word_rank_uniform)

    # Draw the CDF Plot
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " + "Drawing the CDF Plot ... \n\n")
    draw_wrf(cwr_data_probability, cwr_zipf_probability,
             cwr_uniform_probability, True)

    # Calculate the maximum pointwise distance
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " +
                 "Calculating the maximum pointwise distance ... \n\n")
    max_pwd_zipf = maximum_pwd(wr_zipf_probability, wr_data_probability)
    max_pwd_uniform = maximum_pwd(wr_uniform_probability, wr_data_probability)

    print("Maximum pointwise distance of ZIPF: " + str(max_pwd_zipf))
    print("Maximum pointwise distance of Uniform: " + str(max_pwd_uniform))

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " + "FINISHED \n\n")


if __name__ == '__main__':
    main()
