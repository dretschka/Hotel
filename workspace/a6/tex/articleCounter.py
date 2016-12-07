# assignment 6 task 3
# Andrea Mildes - mildes@uni-koblenz.de
# Sebastian Blei - sblei@uni-koblenz.de
# Johannes Kirchner - jkirchner@uni-koblenz.de
# Abdul Afghan - abdul.afghan@outlook.de

import numpy as np
import matplotlib.pyplot as plt


# Draw a graph showing the amount of articles starting with a definite
# or indefinite article.
def draw_graph(a, an, the, count, total):
    objects = ('An', 'A', 'The', 'Combined')
    y_pos = np.arange(len(objects))
    occurrences = (an, a, the, total)

    plt.bar(y_pos, occurrences, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Occurrences')
    plt.title('Article texts of the Simple English Wikipedia starting '
              'with articles')
    textstr = 'Occurrences of \'an\' = %.0f\n' \
              'Occurrences of \'a\' = %.0f\n' \
              'Occurrences of \'the\' = %.0f\n' \
              'Combined occurrences = %.0f\n' \
              'scanned article texts = %.0f\n' \
              'Percentage of texts starting \n' \
              'with an acrticle = %.4f' % \
              (an, a, the, total, count, ((total/count)*100))
    props = dict(facecolor='white', alpha=0.5)
    plt.text(-0.4, 24000, textstr, fontsize=14, verticalalignment='top', bbox=props)

    plt.show()


# Read the given file and store each line (article text) in a list
def readLines(file):
    with open(file) as f:
        wiki_articles = f.readlines()
    return wiki_articles


# Iterate through each article text and check if the first word is an article
def countArticles(wiki_articles):
    a = 0
    an = 0
    the = 0
    count = 0

    for article in wiki_articles:
        first_word = article.split(' ', 1)[0]
        first_word = first_word.strip()
        first_word = first_word.lower()

        count += 1
        if first_word == "a":
            a += 1
        elif first_word == "an":
            an += 1
        elif first_word == "the":
            the += 1

    total = a + an + the
    return a, an, the, count, total


def main():
    file = "simple-20160801-1-article-per-line"
    wiki_articles = readLines(file)
    a, an, the, count, total = countArticles(wiki_articles)
    print("Occurrences of \'A\': " + str(a))
    print("Occurrences of \'An\': " + str(an))
    print("Occurrences of \'The\': " + str(the))
    print("Combined occurrences: " + str(total))
    print("Total amount of article texts: " + str(count))
    print("Percentage of texts starting with an article: " + str(total / count))
    draw_graph(a, an, the, count, total)


if __name__ == '__main__':
    main()
