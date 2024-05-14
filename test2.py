
pairs = ((i, j) for i in range(9) for j in range(9) if i != j)
tile = pairs.pop(randint(len(pairs) - 1))
