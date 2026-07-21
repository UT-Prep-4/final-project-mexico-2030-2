import pygame as pg 

tilemap = [
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0,],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0,],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 0,],
        [0, 1, 0, 1, 0, 0, 0, 0, 1, 0,],
        [0, 1, 0, 1, 0, 0, 0, 1, 1, 0,],
        [0, 1, 1, 1, 0, 0, 0, 1, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0,]
]

def generate_waypoints(tilemap, tile_size):
    # Find the starting path tile (first 1 found)
    start = None
    for y in range(len(tilemap)):
        for x in range(len(tilemap[y])):
            if tilemap[y][x] == 1:
                start = (x, y)
                break
        if start:
            break

    if start is None:
        return []

    waypoints = []
    visited = set()

    current = start

    while current:
        x, y = current
        visited.add(current)

        # Center of the tile
        waypoints.append((
            x * tile_size + tile_size // 2,
            y * tile_size + tile_size // 2
        ))

        next_tile = None

        # Right, Down, Left, Up
        for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
            nx = x + dx
            ny = y + dy

            if (
                0 <= nx < len(tilemap[0]) and
                0 <= ny < len(tilemap) and
                tilemap[ny][nx] == 1 and
                (nx, ny) not in visited
            ):
                next_tile = (nx, ny)
                break

        current = next_tile

    return waypoints