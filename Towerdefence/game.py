import pygame as pg
from player import Player
import constans as c
from enemys import Goblin
from towers import Tower
from button import Button
from levels import tilemap, generate_waypoints
from enemy_data import ENEMY_SPAW_DATA
from wave_maneger import WaveManager

pg.init()

clock = pg.time.Clock()

# ------------------------
# Screen
# ------------------------
screen = pg.display.set_mode(
    (c.SCREEN_WIDTH + c.SIDE_BAR, c.SCREEN_HEIGHT)
)
pg.display.set_caption("Mystical Defence")

# ------------------------
# Images
# ------------------------

tower_spritesheet = []
for i in range(1, c.TOWER_LEVELS + 1):
    sheet = pg.image.load(
        f"Towers/Archer_spritesheet_{i}.png"
    ).convert_alpha()
    tower_spritesheet.append(sheet)

grass_tile = pg.image.load(
    "map_images/Grass_tile.png"
).convert_alpha()

path_tile = pg.image.load(
    "map_images/Path_tile.png"
).convert_alpha()

Archer_image = pg.image.load(
    "towers/Archer_tower.png"
).convert_alpha()

Archerbuy_image = pg.image.load(
    "Buttons/Archer_buy.png"
).convert_alpha()

Cancel_image = pg.image.load(
    "Buttons/Cancel_button.png"
).convert_alpha()

Upgrade_image = pg.image.load(
    "Buttons/Upgrade_button.png"
).convert_alpha()

Go_image = pg.image.load(
    "Buttons/GO_button.png"
).convert_alpha()

enemy_images = {
    "Normal": pg.image.load("enemy/Enemy_sprite_1.png").convert_alpha(),
    "Fast": pg.image.load("enemy/Enemy_sprite_3.png").convert_alpha(),
    "Strong": pg.image.load("enemy/Enemy_sprite_2.png").convert_alpha(),
}

# ------------------------
# Groups
# ------------------------

enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()

# ------------------------
# Waypoints
# ------------------------

waypoints = generate_waypoints(tilemap, c.TILE_SIZE)

# ------------------------
# Wave Manager
# ------------------------

wave_manager = WaveManager(
    enemy_group,
    enemy_images,
    waypoints,
    ENEMY_SPAW_DATA
)

# ------------------------
# Buttons
# ------------------------

tower_button = Button(
    c.SCREEN_WIDTH + 10,
    10,
    Archerbuy_image
)

cancel_button = Button(
    c.SCREEN_WIDTH + 10,
    70,
    Cancel_image
)

upgrade_button = Button(
    c.SCREEN_WIDTH + 10,
    110,
    Upgrade_image
)

go_button = Button(
    c.SCREEN_WIDTH + 20,
    170,
    Go_image
)

# ------------------------
# Font
# ------------------------

font = pg.font.SysFont("arial", 20)

# ------------------------
# Game Variables
# ------------------------

placing_tower = False
selected_tower = None
TOWER_COST = 150
coins = Player.coins

# ------------------------
# Helper Functions
# ------------------------

def create_tower(mouse_pos):
    if not Player.spend_coins(TOWER_COST):
        return

    tower = Tower(mouse_pos, tower_spritesheet)
    tower_group.add(tower)

    coins -= TOWER_COST
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

    if tilemap[mouse_tile_y][mouse_tile_x] != 0:
        return

    for tower in tower_group:
        if (
            tower.tile_x == mouse_tile_x
            and tower.tile_y == mouse_tile_y
        ):
            return

    tower = Tower(mouse_pos, tower_spritesheet)
    tower_group.add(tower)


def select_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

    for tower in tower_group:
        if (
            tower.tile_x == mouse_tile_x
            and tower.tile_y == mouse_tile_y
        ):
            return tower

    return None

# ------------------------
# Main Game Loop
# ------------------------

run = True

while run:

    clock.tick(c.FPS)

    mouse_pos = pg.mouse.get_pos()

    screen.fill((0, 0, 0))

    # ------------------------
    # Draw Map
    # ------------------------

    for row_index, row in enumerate(tilemap):
        for col_index, tile in enumerate(row):

            x = col_index * c.TILE_SIZE
            y = row_index * c.TILE_SIZE

            if tile == 0:
                screen.blit(grass_tile, (x, y))
            else:
                screen.blit(path_tile, (x, y))

    # ------------------------
    # Update Game
    # ------------------------

    wave_manager.update()

    enemy_group.update()
    tower_group.update(enemy_group)

    # ------------------------
    # Draw Sprites
    # ------------------------

    enemy_group.draw(screen)

    for tower in tower_group:
        tower.draw(screen)

    # ------------------------
    # Sidebar
    # ------------------------

    pg.draw.rect(
        screen,
        (45, 45, 45),
        (
            c.SCREEN_WIDTH,
            0,
            c.SIDE_BAR,
            c.SCREEN_HEIGHT,
        ),
    )

    # ------------------------
    # Text
    # ------------------------

    wave_text = font.render(
        f"Wave: {wave_manager.get_wave()}",
        True,
        "white",
    )

    coin_text = font.render(
    f"Coins: {Player.coins}",
    True,
    (255, 255, 0)
    )

    life_text = font.render(
    f"Lives: {Player.lives}",
    True,
    (255, 0, 0)
    )

    screen.blit(coin_text, (c.SCREEN_WIDTH + 10, 10))
    screen.blit(life_text, (c.SCREEN_WIDTH + 10, 35))

    screen.blit(
        wave_text,
        (c.SCREEN_WIDTH + 15, 220),
    )

    # ------------------------
    # Buttons
    # ------------------------

    if tower_button.draw(screen):
        placing_tower = True

    if placing_tower:
        if cancel_button.draw(screen):
            placing_tower = False

    if selected_tower:

        if selected_tower.upgrade_level < c.TOWER_LEVELS:

            if upgrade_button.draw(screen):
                selected_tower.upgrade()

    # ------------------------
    # GO Button
    # ------------------------

    if not wave_manager.wave_running:

        if go_button.draw(screen):
            wave_manager.start_wave()

    # ------------------------
    # Ghost Tower
    # ------------------------

    if placing_tower:

        if mouse_pos[0] < c.SCREEN_WIDTH:

            tile_x = mouse_pos[0] // c.TILE_SIZE
            tile_y = mouse_pos[1] // c.TILE_SIZE

            if tilemap[tile_y][tile_x] == 0:

                screen.blit(
                    Archer_image,
                    (
                        tile_x * c.TILE_SIZE,
                        tile_y * c.TILE_SIZE,
                    ),
                )

    # ------------------------
    # Events
    # ------------------------

    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False

        if (
            event.type == pg.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            mouse_pos = pg.mouse.get_pos()

            if (
                mouse_pos[0] < c.SCREEN_WIDTH
                and mouse_pos[1] < c.SCREEN_HEIGHT
            ):

                if placing_tower:

                    create_tower(mouse_pos)

                else:

                    if selected_tower:
                        selected_tower.selected = False

                    selected_tower = select_tower(mouse_pos)

                    if selected_tower:
                        selected_tower.selected = True

    pg.display.update()


pg.quit()