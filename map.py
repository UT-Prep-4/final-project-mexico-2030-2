from final_project import screen

TILE = 32
game_map = [
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0],
]

for y in range(len(game_map)):
    for x in range(len(game_map[y])):
        if game_map[y][x] == 1:
            screen.blit('map_images/dirt.png', (x * TILE, y * TILE))
        else:
            screen.blit('map_images/grass.png', (x * TILE, y * TILE))