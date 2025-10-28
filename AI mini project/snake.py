import pygame
import sys
import random
from collections import deque
import heapq

# --- Configuration ---
CELL_SIZE = 24
GRID_W = 28  # number of columns
GRID_H = 20  # number of rows
WINDOW_W = CELL_SIZE * GRID_W
WINDOW_H = CELL_SIZE * GRID_H
FPS = 12

# Colors
BG = (10, 10, 10)
GRID_COLOR = (30, 30, 30)
SNAKE_COLOR = (50, 200, 50)
SNAKE_HEAD = (20, 230, 80)
FOOD_COLOR = (200, 50, 50)
PATH_COLOR = (80, 160, 250)
TEXT_COLOR = (220, 220, 220)

# Directions
DIRS = {'UP': (0, -1), 'DOWN': (0, 1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}
DIR_VECTORS = list(DIRS.values())
OPPOSITE = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}


# --- Utility / A* ---
def in_bounds(pos):
    x, y = pos
    return 0 <= x < GRID_W and 0 <= y < GRID_H


def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(pos):
    x, y = pos
    for dx, dy in DIR_VECTORS:
        yield (x + dx, y + dy)


def a_star(start, goal, obstacles, allow_tail=None):
    """A* pathfinding"""
    if start == goal:
        return [start]

    closed = set()
    open_heap = []
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    heapq.heappush(open_heap, (fscore[start], start))

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        if current in closed:
            continue
        closed.add(current)

        for nb in neighbors(current):
            if not in_bounds(nb):
                continue
            if nb in obstacles and nb != allow_tail:
                continue
            if nb in closed:
                continue

            tentative_g = gscore[current] + 1
            if nb not in gscore or tentative_g < gscore[nb]:
                came_from[nb] = current
                gscore[nb] = tentative_g
                fscore[nb] = tentative_g + heuristic(nb, goal)
                heapq.heappush(open_heap, (fscore[nb], nb))

    return []


# --- Game Objects ---
class Snake:
    def __init__(self, start_pos):
        self.body = deque([
            start_pos,
            (start_pos[0] - 1, start_pos[1]),
            (start_pos[0] - 2, start_pos[1])
        ])
        self.dir = 'RIGHT'
        self.grow = 0

    def head(self):
        return self.body[0]

    def tail(self):
        return self.body[-1]

    def positions_set(self):
        return set(self.body)

    def step(self, direction=None):
        if direction is None:
            direction = self.dir
        else:
            if OPPOSITE.get(direction) == self.dir and len(self.body) > 1:
                direction = self.dir
            else:
                self.dir = direction

        dx, dy = DIRS[self.dir]
        hx, hy = self.head()
        new_head = (hx + dx, hy + dy)
        self.body.appendleft(new_head)
        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()

    def eat(self):
        self.grow += 1

    def collides(self, pos=None):
        if pos is None:
            pos = self.head()
        if not in_bounds(pos):
            return True
        return pos in list(self.body)[1:]


class Food:
    def __init__(self):
        self.pos = (0, 0)

    def place(self, snake_positions):
        free = [(x, y) for x in range(GRID_W) for y in range(GRID_H)
                if (x, y) not in snake_positions]
        if not free:
            self.pos = None
            return
        self.pos = random.choice(free)


# --- Rendering ---
def draw_grid(screen):
    for x in range(0, WINDOW_W, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_H))
    for y in range(0, WINDOW_H, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_W, y))


def draw_cell(screen, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                       CELL_SIZE - 2, CELL_SIZE - 2)
    pygame.draw.rect(screen, color, rect, border_radius=6)


def vec_to_dir(vec):
    for k, v in DIRS.items():
        if v == vec:
            return k
    return None


def safe_random_move(snake):
    hx, hy = snake.head()
    candidates = []
    body_set = snake.positions_set()
    tail = snake.tail()
    for dname, (dx, dy) in DIRS.items():
        nx, ny = hx + dx, hy + dy
        if not in_bounds((nx, ny)):
            continue
        if (nx, ny) in body_set and (nx, ny) != tail:
            continue
        candidates.append(dname)
    if not candidates:
        return None
    return random.choice(candidates)


# --- Main ---
def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption('Snake with A* Pathfinding')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    def reset():
        snake = Snake((GRID_W // 2, GRID_H // 2))
        food = Food()
        food.place(snake.positions_set())
        auto = True
        score = 0
        return snake, food, auto, score

    snake, food, auto, score = reset()
    running = True
    manual_direction = None

    while running:
        # --- Input ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    auto = not auto
                elif event.key == pygame.K_r:
                    snake, food, auto, score = reset()
                elif event.key in (pygame.K_UP, pygame.K_w):
                    manual_direction = 'UP'
                    auto = False
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    manual_direction = 'DOWN'
                    auto = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    manual_direction = 'LEFT'
                    auto = False
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    manual_direction = 'RIGHT'
                    auto = False

        # --- Logic ---
        next_move = None
        if auto and food.pos is not None:
            start = snake.head()
            goal = food.pos
            obstacles = set(snake.body)
            tail = snake.tail()
            path = a_star(start, goal, obstacles, allow_tail=tail)
            if path and len(path) >= 2:
                nx, ny = path[1]
                dx = nx - start[0]
                dy = ny - start[1]
                next_dir = vec_to_dir((dx, dy))
                next_move = next_dir
            else:
                next_move = safe_random_move(snake)
        else:
            if manual_direction:
                next_move = manual_direction
                manual_direction = None

        if next_move is None:
            snake.step()
        else:
            snake.step(next_move)

        if not in_bounds(snake.head()) or snake.collides():
            snake, food, auto, score = reset()
            continue

        if snake.head() == food.pos:
            snake.eat()
            score += 1
            food.place(snake.positions_set())

        # --- Draw ---
        screen.fill(BG)
        draw_grid(screen)

        if auto and food.pos is not None:
            start = snake.head()
            goal = food.pos
            obstacles = set(snake.body)
            tail = snake.tail()
            path = a_star(start, goal, obstacles, allow_tail=tail)
            if path and len(path) > 1:
                for p in path[1:]:
                    draw_cell(screen, p, PATH_COLOR)

        if food.pos:
            draw_cell(screen, food.pos, FOOD_COLOR)

        for i, p in enumerate(snake.body):
            color = SNAKE_HEAD if i == 0 else SNAKE_COLOR
            draw_cell(screen, p, color)

        mode_text = 'AUTO' if auto else 'MANUAL'
        txt = font.render(
            f'Mode: {mode_text}    Score: {score}    SPACE: toggle auto/manual    R: restart',
            True, TEXT_COLOR)
        screen.blit(txt, (8, 8))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

