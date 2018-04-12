import math

def load_data():
	data = [line.split(';') for line in open('vectors.txt').read().split('\n')[:-1]]
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
	x, y = load_data()

	number_of_words = 5000
	pos_dict = { i : 0 for i in range(number_of_words) }
	neg_dict = { i : 0 for i in range(number_of_words) }

	for sent, t in zip(y, x):
		for word in t:
			if sent == 1:
				pos_dict[word] += t[word]
			else:
				neg_dict[word] += t[word]

	positive_words = sum(pos_dict.values())
	negative_words = sum(neg_dict.values())
	tweet_pos_prob = sum(y) / len(y)
	tweet_neg_prob = 1 - tweet_pos_prob

	pos_probs = dict()
	neg_probs = dict()

	for i in range(number_of_words):
		pos_probs[i] = (pos_dict[i] + 1) / (positive_words + number_of_words)
		neg_probs[i] = (neg_dict[i] + 1) / (negative_words + number_of_words)

	def classify(tweet):
		pos = math.log(tweet_pos_prob)
		neg = math.log(tweet_neg_prob)
		for w in tweet:
			pos += math.log(pos_probs[w]) * tweet[w]
			neg += math.log(neg_probs[w]) * tweet[w]

		return 0 if neg > pos else 1

	# Calculate accuracy
	correct = 0
	for sent, tweet in zip(y, x):
		if sent == classify(tweet):
			correct += 1

	print('Accuracy:', correct / len(y) * 100)

main()