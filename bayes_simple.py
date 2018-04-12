import math
from NaiveBayesClassifier import NaiveBayesClassifier

def load_data(filename):
    data = [line.split(';') for line in open(filename).read().split('\n')[:-1]]
    y = [int(d[0]) for d in data]
    x_data = [d[1] for d in data]
    x = []
    for line in x_data:
        ddict = {}
        if not line:
            x.append({})
            continue
        for elem in line.split(','):
            a = elem.split('=')
            ddict[int(a[0])] = int(a[1])
        x.append(ddict)

    return x, y

def main():
    x_train, y_train = load_data('data/train.txt')
    x_validation, y_validation = load_data('data/validation.txt')

    number_of_words = 5000
    classifier = NaiveBayesClassifier(number_of_words)

    classifier.train(x_train, y_train)
    print('Accuracy:', classifier.get_accuracy(x_validation, y_validation) * 100)

main()
