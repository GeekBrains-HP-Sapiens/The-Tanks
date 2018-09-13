# from functools import wraps

# def memorize(func):
    
#     @wraps(func)
#     def g(n, memory={0: 0, 1: 1}):

#         r = memory.get(n)

#         if r is None:

#             r = func(n)

#             memory[n] = r

#         return r

#     return g

# @memorize
def AStar(start, end, walls, size):
    cells = {(x, y): {'pos': (x, y), 'parent': None, 'g': 0, 'h': max(abs(
        x - end[0]), abs(y - end[1])), 'wall': (x, y) in walls} for y in range(size[1]) for x in range(size[0])}

    opened = [cells[start]]

    closed = []

    path = []

    while opened:

        current = min(opened, key=lambda i: i['g'] + i['h'])

        closed.append(current)

        opened.remove(current)

        if current['pos'] == end:

            while current['parent']:
                path.append(current['pos'])

                current = current['parent']

            return path[::-1]

        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):

            x, y = current['pos'][0] + dx, current['pos'][1] + dy

            if x < 0 or y < 0 or x >= size[0] or y >= size[1]:
                continue

            adj = cells[(x, y)]

            if adj['wall'] or adj in closed:
                continue

            new_g = current['g'] + 1

            new_cell = adj not in opened

            if new_cell or new_g < adj['g']:
                adj['parent'] = current

                adj['g'] = new_g

            if new_cell:
                opened.append(adj)

    return path
