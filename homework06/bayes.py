from collections import Counter
from copy import deepcopy
from stop_words import get_stop_words
from db import News, session
import math
import csv
import string


stop_words = get_stop_words('english')
stop_words.extend('–')


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator).lower()

def del_stops(s):
    s = s.split()
    k = []
    for i in range(len(s)):
        if s[i] not in stop_words:
            k.append(s[i])
    s=''
    for i in range(len(k)):
        if i!=len(k)-1:
            s+=(k[i]+' ')
        else:
            s+=(k[i])
    return s


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.label_probability = {} # словарь с P(C) для каждого класса
        self.word_prediction = {}

    def fit(self, x, y):
        """ Fit Naive Bayes classifier according to X, y. """

        number_of_labels = len(set(y)) # кол-во классов
        number_of_news = len(x) # кол-во новостей

        usage_of_label = dict(Counter(y)) # словарь с количеством использований каждого класса
        print(usage_of_label)

        for elem in usage_of_label:
            self.label_probability[elem] = usage_of_label[elem]/number_of_news

        title_label =[] # список заголовков и их меток
        for i in range(len(x)):
            title_label.append([x[i],y[i]])

        t = deepcopy(x)
        for i in range(len(x)):
            t[i] = x[i].split()
        all_words = []
        for i in t:
            all_words.extend(i) # список всех слов

        table = []
        for title, label in title_label:
            for word in title.split():
                table.append((word, label)) # список слов, их меток

        word_count = dict(Counter(table)) # словарь ("слово":"метка") - кол-во
        #print(word_count)

        all_words_count = dict(Counter(all_words)) # кол-во использований каждого слова

        all_words_usage = dict.fromkeys(all_words_count) # кол-во использований слова для каждой метки
        for word in all_words_count:
            current = dict.fromkeys(usage_of_label, 0)

            for i in usage_of_label:
                for j in word_count:
                    if j == (word, i):
                        current[i] = word_count[j]
                    else:
                        pass

            all_words_usage[word] = current
        #print(all_words_usage)

        d = len(all_words_count)
        #d=36
        print(d)


        number_of_words_per_label = [] # кол-во слов в каждой метке (метка, кол-во)
        for label in usage_of_label:
            k=0
            for i in table:
                if i[1] == label:
                    k+=1
            number_of_words_per_label.append((label, k))


        self.word_prediction.fromkeys(all_words_count)

        for word in all_words_count:
            current = dict.fromkeys(usage_of_label, 0)
            #print(current)

            for i in usage_of_label:
                try:
                    nic = word_count[(word, i)]
                except:
                    nic = 0
                print(word, i, nic)
                for j in number_of_words_per_label:
                    if j[0] == i:
                        nc = j[1]
                    else:
                        pass
                alpha = self.alpha

                current[i] = (nic + alpha)/(nc + d*alpha)

            self.word_prediction[word] = current
        return self.word_prediction


    def predict(self, x):
        """ Perform classification on an array of test vectors X. """
        response = []

        for sentence in x:
            words = sentence.split()
            label_probability = []

            for label in self.label_probability:
                amount = math.log(self.label_probability[label], math.e)

                for word in words:
                    word_probability = self.word_prediction.get(word)

                    if word_probability:
                        amount += math.log(word_probability[label], math.e)

                label_probability.append((amount, label))
            
            _, answer = max(label_probability)
            response.append(answer)

        return response


    def score(self, x_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        correct = 0
        for i, answer in enumerate(self.predict(x_test)):
            if answer == y_test[i]:
                correct += 1

        print(correct/len(y_test))
        return correct/len(y_test)


"""with open("SMSSpamCollection.txt",  encoding='utf-8') as f:
    data = list(csv.reader(f, delimiter="\t"))

X, Y = [], []
for target, msg in data:
    X.append(msg)
    Y.append(target)

x = [clean(x).lower() for x in X]
x = [del_stops(news) for news in x]
y = [news for news in Y]

x, y, x_test, y_test = x[:4900], y[:4900], x[4900:], y[4900:]"""


s = session()
labeled_news = s.query(News).filter(News.label != None).filter(News.id < 951).all()
x = [clean(news.title) for news in labeled_news]
x = [del_stops(news) for news in x]
y = [news.label for news in labeled_news]
unlabeled_news = s.query(News).filter(News.label != None).filter(News.id > 950).all()
#unlabeled_news = s.query(News).filter(News.label == None).all()
x_test = [clean(news.title) for news in unlabeled_news]
x_test = [del_stops(news) for news in x_test]
y_test = [news.label for news in unlabeled_news]


"""x = ['I love this sandwich', 'This is an amazing place', 'I feel very good about these beers', 'This is my best work', 'What an awesome view', 'I do not like this restaurant', 'I am tired of this stuff', "I can't deal with this", 'He is my sworn enemy', 'My boss is horrible']
y = ['pos', 'pos', 'pos', 'pos', 'pos', 'neg', 'neg', 'neg', 'neg', 'neg']"""


if __name__ == '__main__':
    """prediction = NaiveBayesClassifier(1)
    print(prediction.fit(x, y))
    print('===')
    print(prediction.predict(x_test))
    print(prediction.score(x_test, y_test))"""
    prediction = NaiveBayesClassifier(1)
    print(prediction.fit(x, y))
    print('======')
    print(prediction.predict(x_test))
    print(prediction.score(x_test, y_test))
    