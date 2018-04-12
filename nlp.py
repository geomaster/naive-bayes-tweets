from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import FreqDist

def read_data():
    data = [x.split(';') for x in open('data.txt', 'r').read().split('\n')[:-1]]
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
    for i, word in enumerate(tweet):
        try:
            j = words.index(word)
            if i not in freq:
                freq[i] = 1
            else:
                freq[i] += 1
        except ValueError:
            continue

    return {i: f for i, f in freq.items()}

def serialize_wordvec(vec):
    return ','.join(['{}={}'.format(k, v) for k, v in vec.items()])

functions = [tokenize, remove_stopwords, stem]

def main():
    x, y = read_data()
    for fun in functions:
        x = fun(x)

    fd = FreqDist([word for tweet in x for word in tweet])
    topwords = freqdist_top_n(fd, LIMIT)

    length = len(x)
    for i in range(length):
        print('{};{}'.format(y[i], serialize_wordvec(create_wordvec(topwords, x[i]))))

main()
