class NaiveBayesClassifier:
    def __init__(self, num_words):
        self.num_words_ = num_words

    def train(self, x, y):
        num_words = self.num_words
        pos_dict = { i : 0 for i in range(num_words) }
        neg_dict = { i : 0 for i in range(num_words) }

        for tweet, sentiment in zip(x, y):
            for word in tweet:
                if sentiment == 1:
                    pos_dict[word] += tweet[word]
                else:
                    neg_dict[word] += tweet[word]

        positive_words = sum(pos_dict.values())
        negative_words = sum(neg_dict.values())
        self.tweet_pos_prob = sum(y) / len(y)
        self.tweet_neg_prob = 1 - self.tweet_pos_prob

        self.pos_probs = dict()
        self.neg_probs = dict()

        for i in range(num_words):
            self.pos_probs[i] = (pos_dict[i] + 1) / (positive_words + num_words)
            self.neg_probs[i] = (neg_dict[i] + 1) / (negative_words + num_words)

    def predict(self, tweet):
        pos = math.log(self.tweet_pos_prob)
        neg = math.log(self.tweet_neg_prob)
        for w in tweet:
            pos += math.log(self.pos_probs[w]) * tweet[w]
            neg += math.log(self.neg_probs[w]) * tweet[w]

        return 0 if neg > pos else 1

    def get_accuracy(self, x, y):
        correct = 0
        for tweet, sentiment in zip(x, y):
            if sentiment == self.predict(tweet):
                correct += 1

        return correct / len(y)


