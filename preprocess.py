import html
import csv
import re

def load_dateset():
    X, y = [], []
    with open('train.csv', 'r', encoding='latin1') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None) # Skip header
        for row in reader:
            y.append(int(row[1]))
            X.append(row[2])
    return X, y

def print_dataset(X, Y):
    print("\n".join(["{};{}".format(y, x) for x, y in zip(X, Y)]))

def html_unescape(x):
    return html.unescape(x)

def remove_mentions(x):
    return re.sub(r"@[^\s]+", "", x)

def remove_hashtags(x):
    return re.sub(r"#[^\s]+", "", x)

def fix_whitespace(x):
    return re.sub(r"\s+", " ", x).strip()

def handle_links(x):
    return re.sub(r"(https?://)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", "", x)

def normalize_case(x):
    return x.lower()

def handle_punctuation(x):
    return fix_whitespace(re.sub(r"[^a-zA-Z0-9\s]", "", x))

fns = [ html_unescape, remove_mentions, remove_hashtags, fix_whitespace,
        handle_links, handle_punctuation, normalize_case ]

def main():
    X, y = load_dateset()
    length = len(X)
    j = 0
    for i in range(length):
        s = X[i]
        for fn in fns:
            s = fn(s)

        if s:
            X[j] = s
            y[j] = y[i]
            j += 1

    X = X[:j]
    y = y[:j]
    print_dataset(X, y)

main()


