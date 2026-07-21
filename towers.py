import pygame as pg
import math
import constans as c
from tower_data import TOWER_DATA


class Tower(pg.sprite.Sprite):
    def __init__(self, pos, sprite_sheets):
        super().__init__()

        # -----------------------------
        # Upgrade Stats
        # -----------------------------
        self.upgrade_level = 1
        self.damage = 2
        self.range = TOWER_DATA[0]["range"]
        self.cooldown = TOWER_DATA[0]["cooldown"]

        # -----------------------------
        # Position
        # -----------------------------
        self.tile_x = pos[0] // c.TILE_SIZE
        self.tile_y = pos[1] // c.TILE_SIZE

        self.x = self.tile_x * c.TILE_SIZE + c.TILE_SIZE // 2
        self.y = self.tile_y * c.TILE_SIZE + c.TILE_SIZE // 2

        # -----------------------------
        # Tower State
        # -----------------------------
        self.selected = False
        self.target = None
        self.last_shot = pg.time.get_ticks()

        # -----------------------------
        # Animation
        # -----------------------------
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(
            self.sprite_sheets[self.upgrade_level - 1]
        )

        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        self.angle = 0

        self.original_image = self.animation_list[0]
        self.image = pg.transform.rotate(
            self.original_image,
            self.angle
        )

        self.rect = self.image.get_rect(
            center=(self.x, self.y)
        )

        self.create_range_image()

    # ---------------------------------
    # Load Animation Frames
    # ---------------------------------

    def load_images(self, sprite_sheet):

        animation_list = []

        frame_size = sprite_sheet.get_height()

        for i in range(c.ANIMATION_STEPS):

            frame = sprite_sheet.subsurface(
                i * frame_size,
                0,
                frame_size,
                frame_size,
            )

            animation_list.append(frame)

        return animation_list

    # ---------------------------------
    # Range Circle
    # ---------------------------------

    def create_range_image(self):

        self.range_image = pg.Surface(
            (self.range * 2, self.range * 2),
            pg.SRCALPHA
        )

        pg.draw.circle(
            self.range_image,
            (255, 255, 255, 70),
            (self.range, self.range),
            self.range
        )

        self.range_rect = self.range_image.get_rect(
            center=self.rect.center
        )
    # ---------------------------------
    # Update
    # ---------------------------------

    def update(self, enemy_group):

        # Remove target if it has been killed
        if self.target and not self.target.alive():
            self.target = None

        # Continue attack animation
        if self.target:
            self.play_animation()

        # Find a new target if cooldown is over
        elif pg.time.get_ticks() - self.last_shot >= self.cooldown:
            self.pick_target(enemy_group)

    # ---------------------------------
    # Find Target
    # ---------------------------------

    def pick_target(self, enemy_group):

        closest_enemy = None
        closest_distance = self.range

        for enemy in enemy_group:

            dx = enemy.pos.x - self.x
            dy = enemy.pos.y - self.y

            distance = math.hypot(dx, dy)

            if distance <= closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        if closest_enemy:

            self.target = closest_enemy

            dx = self.target.pos.x - self.x
            dy = self.target.pos.y - self.y

            self.angle = math.degrees(math.atan2(-dy, dx))

            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    # ---------------------------------
    # Attack Animation
    # ---------------------------------

    def play_animation(self):

        if pg.time.get_ticks() - self.update_time >= c.ANIMATION_DELAY:

            self.update_time = pg.time.get_ticks()

            self.frame_index += 1

            if self.frame_index >= len(self.animation_list):

                self.frame_index = 0

                # Damage enemy after animation finishes
                if self.target and self.target.alive():

                    self.target.health -= self.damage

                    if self.target.health <= 0:
                        self.target.kill()

                self.target = None
                self.last_shot = pg.time.get_ticks()

        self.original_image = self.animation_list[self.frame_index]

    # ---------------------------------
    # Upgrade Tower
    # ---------------------------------

    def upgrade(self):

        if self.upgrade_level >= c.TOWER_LEVELS:
            return

        self.upgrade_level += 1

        stats = TOWER_DATA[self.upgrade_level - 1]

        self.range = stats["range"]
        self.cooldown = stats["cooldown"]

        # Increase damage every level
        self.damage * 2

        # Load upgraded animation
        self.animation_list = self.load_images(
            self.sprite_sheets[self.upgrade_level - 1]
        )

        self.frame_index = 0
        self.original_image = self.animation_list[0]

        # Rebuild range circle
        self.create_range_image()

    # ---------------------------------
    # Draw Tower
    # ---------------------------------

    def draw(self, surface):

        self.image = pg.transform.rotate(
            self.original_image,
            self.angle + 90
        )

        self.rect = self.image.get_rect(
            center=(self.x, self.y)
        )

        surface.blit(self.image, self.rect)

        if self.selected:

            self.range_rect.center = self.rect.center

            surface.blit(
                self.range_image,
                self.range_rect
            )