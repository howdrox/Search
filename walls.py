import numpy as np

wall_types = []

grid = np.zeros((10, 10))

test = np.zeros((3, 3))

test[0][0] = 1
test[1][0] = 1
test[2][0] = 1
test[1][1] = 1
test[2][1] = 1

wall_types.append(test)

test = np.zeros((3, 3))

test[0][0] = 1
test[1][0] = 1
test[2][0] = 1
test[1][1] = 1
test[2][1] = 1
test[2][2] = 1

wall_types.append(test)

test = np.zeros((3, 3))

test[0][0] = 1
test[1][0] = 1
test[2][0] = 1
test[0][1] = 1
test[1][1] = 1
test[2][1] = 1
test[0][2] = 1
test[1][2] = 1
test[2][2] = 1

wall_types.append(test)

test = np.zeros((3, 3))

test[0][0] = 1
test[1][0] = 1
test[2][0] = 1
test[0][1] = 1
test[1][1] = 1
test[2][1] = 1
test[2][2] = 1

wall_types.append(test)

test = np.zeros((3, 3))

test[0][1] = 1
test[1][1] = 1
test[2][1] = 1

wall_types.append(test)

test = np.zeros((3, 3))

test[0][0] = 1
test[1][1] = 1
test[2][2] = 1

wall_types.append(test)

np.save("./gamedata/wall_types", wall_types)

for i in wall_types:
    print(i)

r, c = 3, 4
grid[r : r + test.shape[0], c : c + test.shape[1]] = test
print(grid)
