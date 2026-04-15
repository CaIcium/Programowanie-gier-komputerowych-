import pyray as rl
import math
from utils import ghost_positions
class Ship:
    def __init__(self, x, y):
        #parmetry statku
        self.x = x
        self.y = y
        self.size = 15.0  
        self.angle = -math.pi / 2  
        
        self.speed_x = 0.0
        self.speed_y = 0.0
        
        self.acceleration = 300.0  
        self.rotation_speed = 4.0  
        self.friction = 0.99       

    def update(self, dt, screen_w, screen_h):
        # Obrót statku prawo lewo 
        if rl.is_key_down(rl.KEY_LEFT) or rl.is_key_down(rl.KEY_A):
            self.angle -= self.rotation_speed * dt
        if rl.is_key_down(rl.KEY_RIGHT) or rl.is_key_down(rl.KEY_D):
            self.angle += self.rotation_speed * dt

        # gaz 
        if rl.is_key_down(rl.KEY_UP) or rl.is_key_down(rl.KEY_W):
            self.speed_x += math.cos(self.angle) * self.acceleration * dt
            self.speed_y += math.sin(self.angle) * self.acceleration * dt

        # tarcie 
        self.speed_x *= self.friction
        self.speed_y *= self.friction

        # Aplikowanie prędkości do pozycji statku
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt

        self.x = self.x % screen_w
        self.y = self.y % screen_h

    def get_speed(self):
        # Obliczenie całkowitej prędkości statku z twierdzenia pitagorasa 
        return math.sqrt(self.speed_x**2 + self.speed_y**2)

    def draw(self, debug=False):
        # 1. Pobieramy wszystkie pozycje do narysowania (główny obiekt + duchy)
        positions = ghost_positions(self.x, self.y, self.size)
        
        # 2. Zapisujemy oryginalne współrzędne
        orig_x, orig_y = self.x, self.y
        
        # 3. Pętla rysująca statek w każdym wyznaczonym miejscu
        for px, py in positions:
            self.x = px
            self.y = py
            
           #rysowanie statku 
            nose_x = self.x + math.cos(self.angle) * self.size
            nose_y = self.y + math.sin(self.angle) * self.size
            
            left_x = self.x + math.cos(self.angle - 2.5) * self.size
            left_y = self.y + math.sin(self.angle - 2.5) * self.size
            
            right_x = self.x + math.cos(self.angle + 2.5) * self.size
            right_y = self.y + math.sin(self.angle + 2.5) * self.size
            
            # łączenie wierzchołków liniami 
            rl.draw_line(int(nose_x), int(nose_y), int(left_x), int(left_y), rl.WHITE)
            rl.draw_line(int(left_x), int(left_y), int(right_x), int(right_y), rl.WHITE)
            rl.draw_line(int(right_x), int(right_y), int(nose_x), int(nose_y), rl.WHITE)
            
            
            if debug:
                rl.draw_circle_lines(int(self.x), int(self.y), int(self.size), rl.RED)
                
                end_x = self.x + (self.speed_x * 0.5)
                end_y = self.y + (self.speed_y * 0.5)
                rl.draw_line(int(self.x), int(self.y), int(end_x), int(end_y), rl.GREEN)
        # przywrócenie wspołrzednych statku do oryginalnych wartości po rysowaniu wszystkich duchów
        self.x, self.y = orig_x, orig_y
