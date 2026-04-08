#wymiary ekranu 
SCREENW = 800
SCREENH = 600
#płynne przejście przez krawędzie ekranu 
def ghost_positions(x, y, size):
    draw_x_list = [x]
    draw_y_list = [y]

    # Sprawdzanie osi x
    if x < size:
        draw_x_list.append(x + SCREENW)
    elif x > SCREENW - size:
        draw_x_list.append(x - SCREENW)

    # Sprawdzanie osi y
    if y < size:
        draw_y_list.append(y + SCREENH)
    elif y > SCREENH - size:
        draw_y_list.append(y - SCREENH)

    # Generowanie wszystkich kombinacji 
    positions = []
    for dx in draw_x_list:
        for dy in draw_y_list:
            positions.append((dx, dy))

    return positions