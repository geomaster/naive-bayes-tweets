from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import FreqDist
from random import shuffle

def read_data():
    data = [x.split(';') for x in open('data/processed.txt', 'r').read().split('\n')[:-1]]
    x = [d[1] for d in data]
    y = [d[0] for d in data]
    return x, y

def tokenize(x):
    return list(map(word_tokenize, x))

def remove_stopwords(x):
    sw = set(stopwords.words('english'))
    return [[word for word in tweet if word not in sw] for tweet in x]

def stem(x):
    porter = PorterStemmer()
    return [[porter.stem(word) for word in tweet] for tweet in x]

LIMIT = 5000

def freqdist_top_n(fd, n):
    words = list(fd.keys())
    words.sort(key=lambda x: fd[x], reverse=True)
    words = words[:n]
    return words

def create_wordvec(words, tweet):
    freq = {}
    for word in tweet:
        try:
            j = words.index(word)
            if j not in freq:
                freq[j] = 1
            else:
                freq[j] += 1
        except ValueError:
            continue

    return {i: f for i, f in freq.items()}

def serialize_wordvec(vec):
    return ','.join(['{}={}'.format(k, v) for k, v in vec.items()])

def output_dataset(filename, topwords, x, y):
    with open(filename, 'w') as f:
        length = len(x)
        for i in range(length):
            print('{};{}'.format(y[i], serialize_wordvec(create_wordvec(topwords,
                x[i]))), file=f)

functions = [tokenize, remove_stopwords, stem]

TRAIN_SET_SIZE = 0.7

def main():
    print('Converting data to vectors...')
    x, y = read_data()
    for fun in functions:
        x = fun(x)

    # Split train from validation set
    train_set_count = int(TRAIN_SET_SIZE * len(x))
    #validation_set_count = len(x) - train_set_count
    dataset = [(X, Y) for X, Y in zip(x, y)]
    shuffle(dataset)

    train_set = dataset[:train_set_count]
    validation_set = dataset[train_set_count:]

    x_train = [x for x, _ in train_set]
    y_train = [y for _, y in train_set]
    x_validation = [x for x, _ in validation_set]
    y_validation = [y for _, y in validation_set]

    fd = FreqDist([word for tweet in x_train for word in tweet])
    topwords = freqdist_top_n(fd, LIMIT)

    output_dataset('data/train.txt', topwords, x_train, y_train)
    output_dataset('data/validation.txt', topwords, x_validation, y_validation)

main()
