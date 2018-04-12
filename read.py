import csv

def load_dateset():
    X, y = [], []
    with open('train.csv', 'rb', encoing='latin1') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader, None) # Skip header
        for row in reader:
            y.append(int(row[1]))
            X.append(row[2])
    return X, y


if __name__ == '__main__':
    X, y = load_dateset()

    for i in range(4):
        print(X[i], y[i], type(X[i]), type(y[i]))
