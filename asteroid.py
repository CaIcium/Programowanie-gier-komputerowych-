import math
import random
import pyray as rl
from utils import ghost_positions

class Asteroid:
    def __init__(self, x, y, radius):
        self.x = float(x)
        self.y = float(y)
        self.radius = float(radius)
        
        # informacje o rotacji
        self.angle = 0.0
        self.rot_speed = random.uniform(-3.0, 3.0)

        #ruch asteroidy, im wieksza to wolniejsza asteroidy i vice versa 
        move_angle = random.uniform(0, 2 * math.pi)
        base_speed = random.uniform(1000.0, 2500.0)
        speed = base_speed / self.radius
        self.velocity_x = math.cos(move_angle) * speed
        self.velocity_y = math.sin(move_angle) * speed
        
        #tutaj kształt asteroidy 
        self.vertices = []
        num_vertices = random.randint(7, 12) # Losujemy od 7 do 12 kątów
        angle_step = (2 * math.pi) / num_vertices
        
        for i in range(num_vertices):
            vertex_angle = i * angle_step
            
            offset = random.uniform(-self.radius * 0.4, self.radius * 0.2)
            r = self.radius + offset

            local_x = r * math.cos(vertex_angle)
            local_y = r * math.sin(vertex_angle)
            self.vertices.append((local_x, local_y))

    def update(self, dt):
        # ruch
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        # rotacja
        self.angle += self.rot_speed * dt
   # jak obiekt wyleci za ekran to pojawia sie na drugiej stronie 
    def wrap(self, screen_width, screen_height):
        self.x %= screen_width
        self.y %= screen_height

    def draw(self, debug=False):
        positions = ghost_positions(self.x, self.y, self.radius)
        orig_x, orig_y = self.x, self.y
        
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        
        for px, py in positions:
            self.x = px
            self.y = py
            # animacja rotacji asteroidy
            transformed_points = []
            for vx, vy in self.vertices:
                rot_x = vx * cos_a - vy * sin_a
                rot_y = vx * sin_a + vy * cos_a
                
                world_x = rot_x + self.x
                world_y = rot_y + self.y
                transformed_points.append((world_x, world_y))
                #rysowanie linii miedzy wierzchołaki asteroidy 
            num_points = len(transformed_points)
            for i in range(num_points):
                p1 = transformed_points[i]
                p2 = transformed_points[(i + 1) % num_points] # Łączy ostatni wierzchołek z pierwszym
                rl.draw_line(int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1]), rl.WHITE)
            
        self.x, self.y = orig_x, orig_y
        
        if debug:
            rl.draw_circle_lines(int(self.x), int(self.y), int(self.radius), rl.RED)
            start_pos = rl.Vector2(self.x, self.y)
            end_pos = rl.Vector2(self.x + (self.velocity_x * 0.5), self.y + (self.velocity_y * 0.5))
            rl.draw_line_v(start_pos, end_pos, rl.GREEN)