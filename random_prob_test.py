import random

probs = 0
for q in range(500):
    numcell = 256 # Number of potential cells to hold values
    cells = {}
    for i in range(1,numcell+1):
        cells[i] = 0

    N = 3634 # test population value

    for i in range(N):
        c = random.randint(1, numcell)
        cells[c] += 1

    has = 0
    for item in cells:
        #print(str(item) + " : " + str(cells[item]))
        if (cells[item] > 9):
            has += 1
    probs+= has / numcell

print(probs/500)
