# core/prey.py

import math
import random
from core.agent_base import BaseAgent

class Prey(BaseAgent):
    """
    Prey: menurunkan BaseAgent. Logika dasar:
     - Jika predator terlihat: lari menjauh predator terdekat.
     - Jika tidak ada predator di vision radius: diam (bisa random walk juga).
     - Fitness dihitung sebagai lama bertahan hidup (atau jumlah predator yang dihindari).
    """

    def __init__(self, x: float, y: float, config: dict, environment):
        super().__init__(x, y, config, environment, entity_class="prey", color_key="blue")
        # Inisialisasi fitness
        self.fitness = 0.0
        # Bisa tambahkan random walk speed di saat tidak ada predator

    def update(self):
        """
        1) Tambah fitness (misal: +1 setiap time step jika masih alive)
        2) Panggil super().update() untuk pergerakan
        """
        if self.alive:
            self.fitness += 1.0  # contoh: +1 per time step
        super().update()

    def handle_movement(self):
        """
        Rule-based escape: jika predator ada dalam vision, lari menjauh.
        Jika tidak, diam (atau gerakan random).
        """
        visible = [agent for agent in self.visionDetector() if agent.entity_class == "predator" and agent.alive]
        if not visible:
            # Tidak ada predator → misal: diam
            self.vel_x = 0
            self.vel_y = 0
            return

        # Pilih predator terdekat
        target = visible[0]
        min_dist = math.hypot(self.x - target.x, self.y - target.y)
        for p in visible[1:]:
            d = math.hypot(self.x - p.x, self.y - p.y)
            if d < min_dist:
                min_dist = d
                target = p

        # Lari menjauh: vektor = posisi-prey minus posisi-predator
        dx = self.x - target.x
        dy = self.y - target.y
        if min_dist > 0:
            dx /= min_dist
            dy /= min_dist
        self.move_towards_point(dx, dy)

    def reproduce(self):
        """
        Dipanggil person 2 di GA: 
        Jika self.fitness tinggi, silakan pilih sebagai parent. 
        Metode ini kembalikan salinan (deep copy) dari trait dan set fitness=0.
        """
        child = Prey(self.x, self.y, self.config, self.environment)
        child.traits = self.traits.copy()  # nanti diisi trait di Person 2
        return child
