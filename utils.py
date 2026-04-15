import math

# Wymiary ekranu
SCREENW = 800
SCREENH = 500

def ghost_positions(x, y, size):
    # Listy przechowujące główne i dodatkowe współrzędne do rysowania
    draw_x_list = [x]
    draw_y_list = [y]

    # Sprawdzanie, czy obiekt wychodzi za lewą lub prawą krawędź
    if x < size:
        draw_x_list.append(x + SCREENW)
    elif x > SCREENW - size:
        draw_x_list.append(x - SCREENW)

    # Sprawdzanie, czy obiekt wychodzi za górną lub dolną krawędź
    if y < size:
        draw_y_list.append(y + SCREENH)
    elif y > SCREENH - size:
        draw_y_list.append(y - SCREENH)

    # Generowanie wszystkich kombinacji punktów (x, y) do narysowania
    positions = []
    for dx in draw_x_list:
        for dy in draw_y_list:
            positions.append((dx, dy))

    return positions

def check_collision(x1, y1, r1, x2, y2, r2):
    # Obliczanie odległości między środkami dwóch okręgów (wzór Pitagorasa)
    distance = math.hypot(x2 - x1, y2 - y1)
    
    # Zwraca True, jeśli odległość jest mniejsza lub równa sumie ich promieni
    return distance <= (r1 + r2)