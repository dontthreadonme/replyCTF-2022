from collections import defaultdict
import copy
import itertools
inputFile = open("challenge.txt", "r")

L = inputFile.read().split("\n\n")

# map = "".join(L[0][6:].replace(" ","").replace("\n", ""))
grid = L[0][6:].replace(" ", "").split("\n")
words = L[1].split("\n")[2:]
removed_words = []

copy = copy.deepcopy(grid)


def clean_map(remove_coords):
    word = "".join([grid[i][j] for i, j in remove_coords])
    removed_words.append(word)
    for i, j in remove_coords:
        grid[i][j] = "_"


def search_horizontal(word, i, j, temp=[], turn=False):
    if (not 0 <= i < width) or (not 0 <= j < width) or word[len(temp)] != grid[i][j]:
        return

    initial_i, initial_j = i, j
    for step in [-1, 1]:
        new_temp = temp.copy()
        i, j = initial_i, initial_j

        for index, letter in enumerate(word[len(temp):]):
            if 0 <= j < width and letter == grid[i][j]:
                new_temp.append((i, j))

                if not turn:
                    # if j == 30 and i == 3:
                    #     print("turn", word, word, index, new_temp[:-1], "".join([copy[i][j] for i, j in new_temp]))
                    if search_vertical(word, i, j, new_temp[:-1], turn=True):
                        return True

                j += step
            else:
                break
        j -= step
        index -= 1

        if len(new_temp) == len(word):
            clean_map(new_temp)
            return True


def search_vertical(word, i, j, temp=[], turn=False):
    if len(word) == len(temp):
        return

    if (not 0 <= i < width) or (not 0 <= j < width) or word[len(temp)] != grid[i][j]:
        return

    initial_i, initial_j = i, j
    for step in [-1, 1]:
        new_temp = temp.copy()
        i, j = initial_i, initial_j

        for index, letter in enumerate(word[len(temp):]):
            if 0 <= i < width and letter == grid[i][j]:
                new_temp.append((i, j))

                if not turn:
                    # print("turn", word, word, index, new_temp[:-1], "".join([copy[i][j] for i, j in new_temp]))
                    if search_horizontal(word, i, j, new_temp[:-1], turn=True):
                        return True

                i += step
            else:
                break
        i -= step
        index -= 1
        if len(new_temp) == len(word):
            clean_map(new_temp)
            return True


def search_diagonal(word, i, j):
    if (not 0 <= i < width) or (not 0 <= j < width) or word[0] != grid[i][j]:
        return

    initial_i, initial_j = i, j
    for step in itertools.product([-1, 1], [-1, 1]):
        new_temp = []
        i, j = initial_i, initial_j

        for index, letter in enumerate(word[len(new_temp):]):
            if 0 <= i < width and 0 <= j < width and letter == grid[i][j]:
                new_temp.append((i, j))
                j += step[0]
                i += step[1]
            else:
                break
        j -= step[0]
        i -= step[1]
        index -= 1

        if len(new_temp) == len(word):
            clean_map(new_temp)
            return True


def search_grid(word, i, j):
    return search_horizontal(word, i, j, turn=False) or \
        search_vertical(word, i, j, turn=False) or \
        search_diagonal(word, i, j)


width, height = len(grid), len(grid[0])
for i, word in enumerate(grid):
    grid[i] = [letter for letter in word]

start_dic = defaultdict(lambda: [])
for i in range(width):
    for j in range(height):
        start_dic[grid[i][j]] += [(i, j)]

for word in words:
    for start_letter in start_dic[word[0]]:
        i, j = start_letter
        search_grid(word, i, j)


# grid = ["".join(row) for row in grid]
# for l in grid:
#     print(l)

# print(removed_words)
# print(all([removed_word in words for removed_word in removed_words]))

grid = "".join(["".join(row) for row in grid]).replace("_", "").replace("\n", "").replace(" ", "")
print(f"Flag is: {grid}")
