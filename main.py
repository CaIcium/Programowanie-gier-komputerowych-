import pyray as rl
import random
import math
from utils import SCREENW, SCREENH, check_collision
from statek import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion

DEBUG = False
ILOSC_ASTEROID = 15

rl.init_window(SCREENW, SCREENH, "Asteroids")
rl.set_target_fps(60)

rl.init_audio_device() 

# pliki dźwiekowe 
shoot_sound = rl.load_sound("assets/laserShoot.wav") 
explosion_sound = rl.load_sound("assets/cracking.wav") 

#tekstury
stars_tex = rl.load_texture("assets/horse.jpg")

# statek na srodku 
my_ship = Ship(SCREENW / 2, SCREENH / 2)

# generowanie asteroid
asteroids = []
for _ in range(ILOSC_ASTEROID):
    rand_x = random.uniform(0, SCREENW)
    rand_y = random.uniform(0, SCREENH)
    rand_radius = random.uniform(20.0, 60.0)
    ast = Asteroid(rand_x, rand_y, rand_radius)
    ast.alive = True
    asteroids.append(ast)
    

bullets = []
explosions = []

# pętla gry 
while not rl.window_should_close():
    dt = rl.get_frame_time()
    
    my_ship.update(dt, SCREENW, SCREENH)
    
    # Obsługa strzelania 
    if rl.is_key_pressed(32):
        nose_x = my_ship.x + math.cos(my_ship.angle) * my_ship.size
        nose_y = my_ship.y + math.sin(my_ship.angle) * my_ship.size
        
        new_bullet = Bullet(nose_x, nose_y, my_ship.angle, shoot_sound)
        bullets.append(new_bullet)
    
    # aktualizacja pozycji i przenikania przez krawędzie dla asteroid
    for ast in asteroids:
        ast.update(dt) 
        ast.wrap(SCREENW, SCREENH) 
        
    # aktualizacja pozycji i przenikania dla pocisków
    for b in bullets:
        b.update(dt)
        b.wrap(SCREENW, SCREENH)
        
    # aktualizacja czasu trwania animacji eksplozji
    for exp in explosions:
        exp.update(dt)
        
    # Sprawdzanie kolizji między aktywnymi pociskami a aktywnymi asteroidami
    for b in bullets:
        if not b.alive:
            continue
        for ast in asteroids:
            if not ast.alive:
                continue
            
            # W przypadku trafienia: oznaczamy obiekty jako zniszczone i tworzymy eksplozję
            if check_collision(b.x, b.y, b.radius, ast.x, ast.y, ast.radius):
                b.alive = False
                ast.alive = False
                explosions.append(Explosion(ast.x, ast.y, ast.radius * 1.5, explosion_sound))
                
    # czyszczenie list ze zniszczonych obiektów 
    bullets = [b for b in bullets if b.alive]
    asteroids = [ast for ast in asteroids if ast.alive]
    explosions = [exp for exp in explosions if exp.alive]

    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    
    # Rysowanie tła 
    source_rec = rl.Rectangle(0, 0, stars_tex.width, stars_tex.height)
    dest_rec = rl.Rectangle(0, 0, SCREENW, SCREENH)
    origin = rl.Vector2(0, 0)
    rl.draw_texture_pro(stars_tex, source_rec, dest_rec, origin, 0.0, rl.WHITE)
    
    # Rysowanie statku
    my_ship.draw(DEBUG)
    
    # Rysowanie reszty
    for ast in asteroids:
        ast.draw()
        
    for b in bullets:
        b.draw()
        
    for exp in explosions:
        exp.draw()
        
    # debug
    if DEBUG:
        speed = my_ship.get_speed()
        rl.draw_text(f"Predkosc: {speed:.1f}", 10, 10, 20, rl.LIME)
        rl.draw_text(f"Pociski: {len(bullets)}", 10, 40, 20, rl.LIME)
        rl.draw_text(f"Asteroidy: {len(asteroids)}", 10, 70, 20, rl.LIME)
    
  
    rl.end_drawing()

# zwalnianie zasobów
rl.unload_texture(stars_tex)
rl.unload_sound(shoot_sound)
rl.unload_sound(explosion_sound)
rl.close_audio_device()


rl.close_window()