import random as rand
import constants as cons

n = cons.GRID_LEN


def start_game(num_of_sides):
    grid = [[0] * num_of_sides for i in range(num_of_sides)]
    grid = place_two(grid, num_of_sides)
    grid = place_two(grid, num_of_sides)
    return grid


def gen(num_of_sides):
    return rand.randint(0, num_of_sides - 1), rand.randint(0, num_of_sides - 1)


def place_two(grid, num_of_sides=n):
    x, y = gen(num_of_sides)
    while (grid[x][y] != 0):
        x, y = gen(num_of_sides)
    grid[x][y] += 2
    return grid


def curr(grid, num_of_sides=n):
    for i in range(num_of_sides):
        for j in range(num_of_sides):
            if grid[i][j] == 2048:
                return 1
    for i in range(num_of_sides):
        for j in range(num_of_sides):
            if grid[i][j] == 0:
                return -1
    for i in range(num_of_sides - 1):
        for j in range(num_of_sides - 1):
            if grid[i][j] == grid[i + 1][j] or grid[i][j + 1] == grid[i][j]:
                return -1
    for k in range(num_of_sides - 1):
        if grid[num_of_sides - 1][k] == grid[num_of_sides - 1][k + 1]:
            return -1
    for j in range(num_of_sides - 1):
        if grid[j][num_of_sides - 1] == grid[j + 1][num_of_sides - 1]:
            return -1
    return 0


def merge(grid, flag, num_of_sides):
    for i in range(num_of_sides):
        for j in range(num_of_sides - 1):
            if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                grid[i][j] *= 2
                grid[i][j + 1] = 0
                flag = True
    return grid, flag


def rev(grid, num_of_sides):
    for i in range(num_of_sides):
        grid[i].reverse()
    return grid


def trans(grid, num_of_sides):
    return [[grid[j][i] for j in range(num_of_sides)] for i in range(num_of_sides)]


def up(grid, num_of_sides=n):
    print('up')
    grid = trans(grid, num_of_sides)
    grid, done = cover_up(grid, num_of_sides)
    grid, done = merge(grid, done, num_of_sides)
    grid = cover_up(grid, num_of_sides)[0]
    grid = trans(grid, num_of_sides)
    return grid, done


def down(grid, num_of_sides=n):
    print('down')
    grid = rev(trans(grid, num_of_sides), num_of_sides)
    grid, done = cover_up(grid, num_of_sides)
    grid, done = merge(grid, done, num_of_sides)
    grid = cover_up(grid, num_of_sides)[0]
    grid = trans(rev(grid, num_of_sides), num_of_sides)
    return grid, done


def left(grid, num_of_sides=n):
    print('left')
    grid, done = cover_up(grid, num_of_sides)
    grid, done = merge(grid, done, num_of_sides)
    grid = cover_up(grid, num_of_sides)[0]
    return grid, done


def right(grid, num_of_sides=n):
    print('right')
    grid = rev(grid, num_of_sides)
    grid, done = cover_up(grid, num_of_sides)
    grid, done = merge(grid, done, num_of_sides)
    grid = cover_up(grid, num_of_sides)[0]
    grid = rev(grid, num_of_sides)
    return grid, done


def cover_up(grid, num_of_sides=n):
    grid_new = [[0] * num_of_sides for i in range(num_of_sides)]
    flag = False
    for i in range(num_of_sides):
        cnt = 0
        for j in range(num_of_sides):
            if grid[i][j] != 0:
                grid_new[i][cnt] = grid[i][j]
                if j != cnt:
                    flag = True
                cnt += 1
    return grid_new, flag