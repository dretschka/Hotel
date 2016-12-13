# assignment 7 task 2
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

# import numpy as np
import matplotlib.pyplot as plt
import logging
import random
import operator
import time

logging.basicConfig(filename='charCounter.log', level=logging.DEBUG)
start_time = 0
zipf_probabilities = {' ': 0.17840450037213465, '1': 0.004478392057619917, '0': 0.003671824660673643, '3': 0.0011831834225755678, '2': 0.0026051307175779174, '5': 0.0011916662329062454, '4': 0.0011108979455528355, '7': 0.001079651630435706, '6': 0.0010859164582487295, '9': 0.0026071152282516083, '8': 0.0012921888323905763, '_': 2.3580656240324293e-05, 'a': 0.07264712490903191, 'c': 0.02563767289222365, 'b': 0.013368688579962115, 'e': 0.09688273452496411, 'd': 0.029857183586861923, 'g': 0.015076820473031856, 'f': 0.017232219565845877, 'i': 0.06007894642873102, 'h': 0.03934894249122837, 'k': 0.006067466280926215, 'j': 0.0018537015877810488, 'm': 0.022165129421030945, 'l': 0.03389465109649857, 'o': 0.05792847618595622, 'n': 0.058519445305660105, 'q': 0.0006185966212395744, 'p': 0.016245321110753712, 's': 0.055506530071283755, 'r': 0.05221605572640867, 'u': 0.020582942617121572, 't': 0.06805204881206219, 'w': 0.013964469813783246, 'v': 0.007927199224676324, 'y': 0.013084644140464391, 'x': 0.0014600810295164054, 'z': 0.001048859288348506}
uniform_probabilities = {' ': 0.1875, 'a': 0.03125, 'c': 0.03125, 'b': 0.03125, 'e': 0.03125, 'd': 0.03125, 'g': 0.03125, 'f': 0.03125, 'i': 0.03125, 'h': 0.03125, 'k': 0.03125, 'j': 0.03125, 'm': 0.03125, 'l': 0.03125, 'o': 0.03125, 'n': 0.03125, 'q': 0.03125, 'p': 0.03125, 's': 0.03125, 'r': 0.03125, 'u': 0.03125, 't': 0.03125, 'w': 0.03125, 'v': 0.03125, 'y': 0.03125, 'x': 0.03125, 'z': 0.03125}


# String .join is fastest


# Read the given file into a string
def read_file(file):
    with open(file) as f:
        data = f.read().replace('\n', '')
    return data


def write_file(filename, generated_string):
    with open(filename, 'w') as f:
        f.write(generated_string)

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] " + "Finished writing \"" + filename + "\" file. \n\n")
    return


# Iterate through the string and count the occurrence of each character
def count_chars(data):
    count = 0
    char_dict = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0,
                 'y': 0, 'z': 0, ' ': 0}

    for i in range(0, len(data)):
        try:
            # Increase count by one
            char_dict[data[i].lower()] += 1
            count += 1
        except KeyError:
            # Ignore chars that are not part of the dictionary
            continue

    logging.info(str(count) + ' | ' + str(char_dict) + "\n\n")
    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] " + "Finished counting the chars. Found " + str(count) + " chars.\n\n")
    return count, char_dict


def calculate_percentage(count, char_dict):
    rel_char = {}

    for key, value in char_dict.items():
        rel_char[key] = value / count

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] " + "Finished calculating percentages\n\n")
    return rel_char


def add_percentage(rel_char):
    added_percentage = []
    sum_percentage = 0

    # Sort the rel_char dictionary by value
    sorted_rel_char = sorted(rel_char.items(), key=operator.itemgetter(1), reverse=True)

    for key, value in sorted_rel_char:
        x = sum_percentage + value
        added_percentage.append((key, x))
        sum_percentage = x

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "] " + "Finished adding percentages\n\n")
    return added_percentage


def sample_data(count, added_percentage):
    generated_string = ""
    char_dict = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0,
                 'y': 0, 'z': 0, ' ': 0}

    for i in range(0, count):
        r = random.random()
        for key, value in added_percentage:
            if r <= value:
                generated_string += key
                try:
                    # Increase count by one
                    char_dict[key] += 1
                except KeyError:
                    # Ignore chars that are not part of the dictionary
                    pass
                break

        if i % 10000000 == 0:
            t = str(round((time.time() - start_time), 2))
            logging.info("[" + t + "] " + "Calculated " + str(i) + " chars \n\n")

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " + "Finished generating strings\n\n")

    return generated_string, char_dict


def draw_wrf(char_dict):
    x = [1, 2, 3, 4]
    y = [1, 4, 9, 6]
    labels = ['Frogs', 'Hogs', 'Bogs', 'Slogs']

    plt.plot(x, y, 'ro')
    # You can specify a rotation for the tick labels in degrees or with keywords.
    plt.xticks(x, labels, rotation='vertical')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.2)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.15)
    plt.show()


def main():
    global start_time

    # Delete content of log file
    with open('charCounter.log', 'w'):
        pass

    start_time = time.time()
    file = "simple-20160801-1-article-per-line"
    data = read_file(file)
    count, char_dict = count_chars(data)

    added_percentage_zipf = add_percentage(zipf_probabilities)
    logging.info("ZIPF PROBABILITIES: \n" + str(added_percentage_zipf) + "\n\n")
    generated_string_zipf, char_dict_zipf = sample_data(count, added_percentage_zipf)
    #write_file('generated_zipf.txt', generated_string_zipf)
    print(char_dict_zipf)

    added_percentage_uniform = add_percentage(uniform_probabilities)
    logging.info("UNIFORM PROBABILITIES: \n" + str(added_percentage_uniform) + "\n\n")
    generated_string_uniform, char_dict_uniform = sample_data(count, added_percentage_uniform)
    #write_file('generated_uniform.txt', generated_string_uniform)
    print(char_dict_uniform)


if __name__ == '__main__':
    main()
