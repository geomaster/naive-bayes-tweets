def load_data():
	data = [line.split(';') for line in open('vectors.txt').read().split('\n')]
	y = [d[0] for d in data]
	x = [[int(k) for k in d[1].split(',')] for d in  data]
	return x, y

def main():
	x, y = load_data()
	print(x)

main()