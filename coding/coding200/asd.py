from collections import defaultdict
import itertools
import numpy as np
import string
import copy


inputFile = open("map.txt", "r")

L = inputFile.read().split("\n")
L = [[letter for letter in line] for line in L][:-1]
L = np.array(L)
copyL = copy.deepcopy(L)

size = np.shape(L)
start_pos = tuple(np.argwhere(L == "A").flatten())
end_pos = tuple(np.argwhere(L == "B").flatten())

portals = defaultdict(lambda: list())
for letter in string.ascii_lowercase:
    for coords in np.argwhere(L == letter):
        portals[letter].append(tuple(coords))


def neighbours(cell):
    for c in itertools.product(*(range(n-1, n+2) for n in cell)):
        if c != cell and all(0 <= i < bound for i, bound in zip(c, size)):
            yield c


def check_activation(cell):
    return sum([1 for i, j in neighbours(cell) if L[i][j] == "&"])


def get_next_gen(current_gen_L):
    next_gen_L = copy.deepcopy(current_gen_L)
    portals_to_pop = []
    for i in range(size[0]):
        for j in range(size[1]):
            if (i, j) not in [start_pos, end_pos]:
                letter = current_gen_L[i][j]
                if letter == "&":
                    if not (2 <= check_activation((i, j)) <= 3):
                        next_gen_L[i][j] = "."
                else:
                    if check_activation((i, j)) >= 3:
                        if letter != ".":
                            cur_portal = portals[letter]
                            next_gen_L[cur_portal[0][0]][cur_portal[0][1]] = "&"
                            next_gen_L[cur_portal[1][0]][cur_portal[1][1]] = "&"
                            portals_to_pop.append(letter)
                        else:
                            next_gen_L[i][j] = "&"

    for portal in portals_to_pop:
        if portal in portals:
            portals.pop(portal)

    return next_gen_L


# every pos 2d
# paths 1d  [(1,2), (2,2)]
# pos   (1,2)
# paths = np.zeros(size+(1, 2), dtype=int)
# base_paths = copy.deepcopy(paths)
# paths[start_pos] += list(start_pos)
current_map = L
paths = [[[] for _ in range(size[0])] for _ in range(size[0])]
print(start_pos)
paths[start_pos[0]][start_pos[1]].append([start_pos, ])


index = 0
while True:
    next_map = get_next_gen(current_map)
    next_paths = [[[] for _ in range(size[0])] for _ in range(size[0])]

    for x, y in itertools.product(range(size[0]), range(size[1])):
        if not paths[x][y]:
            continue

        for dx, dy, D in [(1, 0, "S"), (0, 1, "E"), (-1, 0, "N"), (0, -1, "W")]:
            nx = x+dx
            ny = y+dy
            if not 0 <= nx < size[0] or not 0 <= ny < size[1]:
                continue
            if current_map[nx][ny] == "&" or next_map[nx][ny] == "&":
                continue

            # print(paths[x][y])
            temp_paths = [[pos[:2] for pos in path] for path in paths[x][y]]
            # print(temp_paths)
            new_paths = [path+[(nx, ny, D)] for path in paths[x][y] if all([(nx, ny) not in temp_path for temp_path in temp_paths])]
            letter = current_map[nx][ny]
            if letter not in "AB.":
                for portal in portals[letter]:
                    if nx != portal[0] or ny != portal[1]:
                        nx, ny = portal
                        break
                new_paths = [new_path+[(nx, ny), ] for new_path in new_paths]

            if next_paths[nx][ny]:
                next_paths[nx][ny] += new_paths
            else:
                next_paths[nx][ny] = new_paths

    paths = next_paths
    current_map = next_map
    # print()
    # print(paths)
    # print()
    index += 1
    # print(index)
    # if index == 2:
    #     break
    if paths[end_pos[0]][end_pos[1]]:
        break


print()
print(current_map)
print()

# print(paths[end_pos[0]][end_pos[1]])


def proceess_path(path):
    steps = "".join([(pos+("",))[2] for pos in path])
    portals = sum([1 for pos in path if len(pos) == 2])
    return (steps, portals-1)


paths = paths[end_pos[0]][end_pos[1]]

portals_used = list(map(len, paths))
portals_used = list(map(len, paths))

print(len(paths))
paths = [path for path in paths if len(path) == max(portals_used)]
print(len(paths))
paths = list(map(proceess_path, paths))
print((paths))
paths.sort()
print((paths))
portals_used = paths[0][1]
paths = [path[0] for path in paths]
passwd = f"{len(paths)}-{''.join(paths)}-{portals_used}"
print(passwd)
