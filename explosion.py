import pyray as rl

class Explosion:
    def __init__(self, x, y, max_radius, explosion_sound):
        self.x = float(x)
        self.y = float(y)
        self.max_radius = float(max_radius)
        
        rl.play_sound(explosion_sound)
        
        self.duration = 0.4 
        self.timer = 0.0
        self.alive = True

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.alive = False

    def draw(self):
        if not self.alive:
            return
            
        progress = self.timer / self.duration
        current_radius = self.max_radius * progress
        
        rl.draw_circle_lines(int(self.x), int(self.y), current_radius, rl.ORANGE)