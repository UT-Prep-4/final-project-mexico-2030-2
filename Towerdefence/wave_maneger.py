import pygame as pg
from enemys import Goblin


class WaveManager:
    def __init__(self, enemy_group, enemy_images, waypoints, spawn_data):
        self.enemy_group = enemy_group
        self.enemy_images = enemy_images
        self.waypoints = waypoints
        self.spawn_data = spawn_data

        self.wave = 0
        self.wave_running = False

        self.enemy_queue = []

        self.spawn_delay = 500  # milliseconds
        self.last_spawn = pg.time.get_ticks()

    def start_wave(self):
        if self.wave_running:
            return

        if self.wave >= len(self.spawn_data):
            return

        self.enemy_queue.clear()

        current_wave = self.spawn_data[self.wave]

        # Build queue of enemies to spawn
        for enemy_type, amount in current_wave.items():
            for _ in range(amount):
                self.enemy_queue.append(enemy_type)

        self.wave_running = True
        self.last_spawn = pg.time.get_ticks()

    def update(self):
        if not self.wave_running:
            return

        current_time = pg.time.get_ticks()

        # Spawn one enemy every spawn_delay milliseconds
        if self.enemy_queue:
            if current_time - self.last_spawn >= self.spawn_delay:
                enemy_type = self.enemy_queue.pop(0)

                enemy = Goblin(
                    enemy_type,
                    self.waypoints,
                    self.enemy_images
                )

                self.enemy_group.add(enemy)
                self.last_spawn = current_time

        # Wave finished
        if len(self.enemy_queue) == 0 and len(self.enemy_group) == 0:
            self.wave_running = False
            self.wave += 1

    def get_wave(self):
        return self.wave + 1

    def finished(self):
        return self.wave >= len(self.spawn_data)