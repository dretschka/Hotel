# assignment 10 task 1
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import logging
import time
import numpy as np
import matplotlib.pyplot as plt

# Configure logging and set start time
logging.basicConfig(filename='system_entropy.log', level=logging.DEBUG)
start_time = 0


# Read the given file into a list
def read_file(file):
    l = []
    with open(file) as f:
        for line in f:
            l.append(tuple(line.strip().split('\t')))
    return l


# Creates a dictionary with the date as key and another dictionary
# containing the memes and count of memes as value
def get_dict_of_memes_by_date(l):
    dic = {}
    # Sep by date
    for line in l:
        date = line[1].strip()
        hashtag = line[2].lower().strip()
        # Check if Date is in dic yet
        # If not, add the date and the current hashtag
        # If it is, check if the hashtag is already in its set
        # If it is, increase count by one
        # If its not, add it
        if date not in dic:
            dic[date] = {}
            dic[date][hashtag] = 1
        else:
            if hashtag in dic[date]:
                dic[date][hashtag] += 1
            else:
                dic[date][hashtag] = 1
    return dic


# Creates a nested dictionary with the following structure:
# dic[date][user][hashtag] -> count of the hashtag
def get_dict_of_memes_by_date_and_user(l):
    dic = {}
    # Sep by date
    for line in l:
        date = line[1].strip()
        hashtag = line[2].lower().strip()
        user = line[0].lower().strip()
        if date not in dic:
            dic[date] = {}
            dic[date][user] = {}
            dic[date][user][hashtag] = 1
        else:
            if user in dic[date]:
                if hashtag in dic[date][user]:
                    dic[date][user][hashtag] += 1
                else:
                    dic[date][user][hashtag] = 1
            else:
                dic[date][user] = {}
                dic[date][user][hashtag] = 1
    return dic


# Calculates the system entropy
def calc_system_entropy_per_day(l):
    dic = get_dict_of_memes_by_date(l)
    entropy_per_day = []

    for k, v in dic.items():
        dic_len = len(v)
        system_entropy = 0
        for i, j in v.items():
            system_entropy += (j / dic_len) * np.log((j / dic_len))
        system_entropy *= -1
        entropy_per_day.append((k, system_entropy))

    return entropy_per_day


def calc_average_user_entropy_per_day(l):
    dic = get_dict_of_memes_by_date_and_user(l)
    avg_user_entropy_per_day = []
    user_entropy = 0
    user_entropy_list = []
    avg_user_entropy = 0

    for k, v in dic.items():
        date = k
        user_dic = v
        for i, j in user_dic.items():
            user = i
            hashtag_dic = j

            # Calculate user entropy
            user_entropy = 0
            len_hash_dic = len(hashtag_dic)
            for x, y in hashtag_dic.items():
                user_entropy += (y / len_hash_dic) * np.log((y / len_hash_dic))
            user_entropy_list.append(user_entropy)

        # calculate average user entropy:
        for ue in user_entropy_list:
            avg_user_entropy += ue
        avg_user_entropy /= len(user_entropy_list)

        avg_user_entropy_per_day.append((date, avg_user_entropy))

    return avg_user_entropy_per_day


# draw the plot
def draw_plot(system_entropy, user_entropy):
    temp_system_entropy = []
    temp_user_entropy = []

    # Sort both lists by date
    system_entropy.sort(key=lambda tup: tup[0])
    user_entropy.sort(key=lambda tup: tup[0])

    for i in system_entropy:
        temp_system_entropy.append(i[1])
    for i in user_entropy:
        temp_user_entropy.append(i[1])

    plt.plot(temp_system_entropy, 'r',
               label='System Entropy')
    plt.plot(temp_user_entropy, 'b',
               label='Average User Entropy')
    plt.title("Entropy")
    plt.xlabel("Rank")
    plt.ylabel("Entropy")
    plt.legend(loc=0)
    plt.margins(0.2)
    plt.show()

    return


def main():
    global start_time

    # Delete content of log file
    with open('system_entropy.log', 'w'):
        pass

    start_time = time.time()

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  Starting :) \n\n")

    l = read_file('onlyhash.data')

    # Calculate the system entropy per day
    system_entropy = calc_system_entropy_per_day(l)

    # Calculate the average user entropy per day
    user_entropy = calc_average_user_entropy_per_day(l)

    # Draw the plot
    draw_plot(system_entropy, user_entropy)

    t = str(round((time.time() - start_time), 2))
    logging.info("[" + t + "]  " + "FINISHED \n\n")


if __name__ == '__main__':
    main()
