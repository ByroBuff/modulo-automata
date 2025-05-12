import pygame
import sys
import colorsys
from tkinter import filedialog
import tkinter as tk

TOTAL_SIZE = 630
GRID_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (0, 0, 0)
NUM_STAGES = 8
FPS = 5
FIXED_HUE = 0.6
BRIGHTNESS_RANGE = (0.1, 1.0)

CELLS_PER_ROW = 10
WIDTH = 21
HEIGHT = 21
CELL_SIZE = TOTAL_SIZE // WIDTH

def get_hsb_color(value):
    if value <= 0:
        return BACKGROUND_COLOR
    brightness = BRIGHTNESS_RANGE[0] + (value / NUM_STAGES) * (BRIGHTNESS_RANGE[1] - BRIGHTNESS_RANGE[0])
    r, g, b = colorsys.hsv_to_rgb(FIXED_HUE, 1.0, brightness)
    return (int(r * 255), int(g * 255), int(b * 255))

def blank_grid():
    return [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

def display_grid(screen, grid, draw_borders):
    global CELL_SIZE
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = get_hsb_color(cell)
            pygame.draw.rect(screen, color, rect)
            if draw_borders:
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

def calculate_next_grid(grid):
    new_grid = [[0] * len(row) for row in grid]
    movements = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            total = 0
            for dx, dy in movements:
                ny = (y + dy) % len(grid)
                nx = (x + dx) % len(row)
                total += grid[ny][nx]
            new_grid[y][x] = total % NUM_STAGES
    return new_grid


def export_grid(grid):
    root = tk.Tk()
    root.withdraw()
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if path:
        with open(path, "w") as f:
            f.write(f"{len(grid)} {len(grid[0])}\n")
            for row in grid:
                f.write(" ".join(map(str, row)) + "\n")

def import_grid():
    global WIDTH, HEIGHT, CELL_SIZE
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if path:
        with open(path, "r") as f:
            header = f.readline()
            HEIGHT, WIDTH = map(int, header.strip().split())
            CELL_SIZE = TOTAL_SIZE // max(WIDTH, HEIGHT)
            return [list(map(int, line.strip().split())) for line in f]
    return [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

def main():
    global WIDTH, HEIGHT, CELL_SIZE, NUM_STAGES, FIXED_HUE, FPS
    pygame.init()
    screen = pygame.display.set_mode((TOTAL_SIZE, TOTAL_SIZE))
    pygame.display.set_caption("Modulo Cells - HSB")
    clock = pygame.time.Clock()

    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    running = False
    draw_borders = True

    while True:
        mx, my = pygame.mouse.get_pos()
        x = mx // CELL_SIZE
        y = my // CELL_SIZE

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE):
                pygame.quit(); sys.exit()

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE: running = not running
                elif e.key == pygame.K_r: grid = blank_grid()
                elif e.key == pygame.K_e: export_grid(grid)
                elif e.key == pygame.K_i: grid = import_grid(screen)
                elif e.key == pygame.K_UP:   FPS = min(FPS+1, 60)
                elif e.key == pygame.K_DOWN: FPS = max(FPS-1, 1)

                elif e.key == pygame.K_RIGHT:
                    NUM_STAGES = min(NUM_STAGES+1, 20)
                elif e.key == pygame.K_LEFT and NUM_STAGES > 2:
                    NUM_STAGES -= 1

                elif e.key == pygame.K_a: FIXED_HUE += 0.05
                elif e.key == pygame.K_d: FIXED_HUE -= 0.05

                elif e.key == pygame.K_w and WIDTH < 120:
                    WIDTH += 2; HEIGHT += 2; grid = blank_grid()
                elif e.key == pygame.K_s and WIDTH > 4:
                    WIDTH -= 2; HEIGHT -= 2; grid = blank_grid()

                elif e.key == pygame.K_g: draw_borders = not draw_borders

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    if e.button == 1:
                        grid[y][x] = (grid[y][x] + 1) % NUM_STAGES
                    elif e.button == 3:
                        grid[y][x] = (grid[y][x] - 1) % NUM_STAGES

                    

        screen.fill(BACKGROUND_COLOR)
        display_grid(screen, grid, draw_borders=draw_borders)
        pygame.display.flip()

        if running:
            grid = calculate_next_grid(grid)
            clock.tick(FPS)
        else:
            clock.tick(60)

if __name__ == "__main__":
    main()
