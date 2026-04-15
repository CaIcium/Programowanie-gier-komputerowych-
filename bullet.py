import math
import pyray as rl
from utils import ghost_positions

class Bullet:
    def __init__(self, x, y, angle, shoot_sound):
        self.x = float(x)
        self.y = float(y)
        self.radius = 2.0  
        
       
        rl.play_sound(shoot_sound)
        
        # Flagi i cykl życia
        self.ttl = 1.5     # Czas życia w sekundach
        self.alive = True
        
        # Prędkość pocisku
        speed = 800.0 
        
        # Obliczamy wektor prędkości
        self.velocity_x = math.cos(angle) * speed
        self.velocity_y = math.sin(angle) * speed

    def update(self, dt):
        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False
            return 
            
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def wrap(self, screen_width, screen_height):
        self.x %= screen_width
        self.y %= screen_height

    def draw(self):
        if not self.alive:
            return
            
        positions = ghost_positions(self.x, self.y, self.radius)
        orig_x, orig_y = self.x, self.y
        
        for px, py in positions:
            rl.draw_circle(int(px), int(py), self.radius, rl.YELLOW)
            
        self.x, self.y = orig_x, orig_y