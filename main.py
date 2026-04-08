# main.py
import pyray as rl
import random
from utils import SCREENW, SCREENH
from statek import Ship
from asteroid import Asteroid

DEBUG = False
ILOSC_ASTEROID = 15

rl.init_window(SCREENW, SCREENH, "Asteroids")
rl.set_target_fps(60)

my_ship = Ship(SCREENW / 2, SCREENH / 2)
# tworzenie astroid o losowych wymiarch i pozycji 
asteroids = []
for _ in range(ILOSC_ASTEROID):
    rand_x = random.uniform(0, SCREENW)
    rand_y = random.uniform(0, SCREENH)
    rand_radius = random.uniform(20.0, 60.0)
    asteroids.append(Asteroid(rand_x, rand_y, rand_radius))
# główna pętla gry
while not rl.window_should_close():
    dt = rl.get_frame_time()
    
    # aktualizcja statku i asteroid 
    my_ship.update(dt, SCREENW, SCREENH)
    
    for ast in asteroids:
        ast.update(dt) 
        ast.wrap(SCREENW, SCREENH) 
    # rysowanie 
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    
    # rysowanie statku i asteroid 
    my_ship.draw(DEBUG)
    
    for ast in asteroids:
        ast.draw()
        
    if DEBUG:
        speed = my_ship.get_speed()
        rl.draw_text(f"Predkosc: {speed:.1f}", 10, 10, 20, rl.LIME)
    
    rl.end_drawing()

rl.close_window()