import math
import pyray as rl

def rotate_point(x, y, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return x * cos_a - y * sin_a, x * sin_a + y * cos_a

class Ship:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.angle = 0.0 
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.rotation_speed = 3.0
        self.thrust_power = 200.0
        self.is_thrusting = False

    def update(self, dt, screen_width, screen_height):
        if rl.is_key_down(rl.KEY_LEFT):
            self.angle -= self.rotation_speed * dt
        if rl.is_key_down(rl.KEY_RIGHT):
            self.angle += self.rotation_speed * dt

        self.is_thrusting = rl.is_key_down(rl.KEY_UP)
        if self.is_thrusting:
            self.velocity_x += math.sin(self.angle) * self.thrust_power * dt
            self.velocity_y -= math.cos(self.angle) * self.thrust_power * dt

        self.velocity_x *= 0.99
        self.velocity_y *= 0.99

        speed = self.get_speed()
        max_speed = 300.0
        if speed > max_speed:
            self.velocity_x = (self.velocity_x / speed) * max_speed
            self.velocity_y = (self.velocity_y / speed) * max_speed

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        self.x %= screen_width
        self.y %= screen_height

    def get_speed(self):
        return math.sqrt(self.velocity_x**2 + self.velocity_y**2)

    def draw(self, debug=False):
        if self.is_thrusting:
            f1_x, f1_y = 0.0, 30.0
            f2_x, f2_y = -8.0, 15.0
            f3_x, f3_y = 8.0, 15.0

            rf1_x, rf1_y = rotate_point(f1_x, f1_y, self.angle)
            rf2_x, rf2_y = rotate_point(f2_x, f2_y, self.angle)
            rf3_x, rf3_y = rotate_point(f3_x, f3_y, self.angle)

            vf1 = rl.Vector2(self.x + rf1_x, self.y + rf1_y)
            vf2 = rl.Vector2(self.x + rf2_x, self.y + rf2_y)
            vf3 = rl.Vector2(self.x + rf3_x, self.y + rf3_y)

            rl.draw_triangle_lines(vf1, vf2, vf3, rl.ORANGE)

        p1_x, p1_y = 0.0, -20.0
        p2_x, p2_y = -15.0, 15.0
        p3_x, p3_y = 15.0, 15.0

        r1_x, r1_y = rotate_point(p1_x, p1_y, self.angle)
        r2_x, r2_y = rotate_point(p2_x, p2_y, self.angle)
        r3_x, r3_y = rotate_point(p3_x, p3_y, self.angle)

        v1 = rl.Vector2(self.x + r1_x, self.y + r1_y)
        v2 = rl.Vector2(self.x + r2_x, self.y + r2_y)
        v3 = rl.Vector2(self.x + r3_x, self.y + r3_y)

        rl.draw_triangle_lines(v1, v2, v3, rl.RAYWHITE)

        if debug:
            start_pos = rl.Vector2(self.x, self.y)
            end_pos = rl.Vector2(self.x + self.velocity_x, self.y + self.velocity_y)
            rl.draw_line_v(start_pos, end_pos, rl.GREEN)
