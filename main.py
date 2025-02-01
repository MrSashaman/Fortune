import pygame
import random
import math
import time



# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Колесо Фортуны")
pygame.display.set_icon(pygame.image.load("icon.png"))

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Параметры колеса
WHEEL_RADIUS = 200
WHEEL_CENTER = (WIDTH // 2, HEIGHT // 2)
NUM_SECTORS = 8
SECTOR_COLORS = [RED, GREEN, BLUE, (255, 255, 0), (0, 255, 255), (255, 0, 255), (150, 150, 150), (200, 100, 50)]
SECTOR_NAMES = ["Сектор 1", "Сектор 2", "Сектор 3", "Сектор 4", "Сектор 5", "Сектор 6", "Сектор 7", "Сектор 8"]


# Угол между секторами
ANGLE_PER_SECTOR = 360 / NUM_SECTORS

# Шрифты
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 20)
large_font = pygame.font.Font(None, 72)

# Флаг вращения
spinning = False
rotation_angle = 0
rotation_speed = 0
target_sector = -1
start_time = 0
end_time = 0
deceleration_time = 2
rotation_time = 3

# Функция для рисования колеса
def draw_wheel():
    for i in range(NUM_SECTORS):
        start_angle = math.radians(i * ANGLE_PER_SECTOR - rotation_angle)
        end_angle = math.radians((i + 1) * ANGLE_PER_SECTOR - rotation_angle)
        points = [WHEEL_CENTER]
        points.append((
        WHEEL_CENTER[0] + WHEEL_RADIUS * math.cos(start_angle),
        WHEEL_CENTER[1] + WHEEL_RADIUS * math.sin(start_angle)
        ))
        points.append((
         WHEEL_CENTER[0] + WHEEL_RADIUS * math.cos(end_angle),
        WHEEL_CENTER[1] + WHEEL_RADIUS * math.sin(end_angle)
        ))

        pygame.draw.polygon(screen, SECTOR_COLORS[i % len(SECTOR_COLORS)], points)

        text_angle = math.radians((i + 0.5) * ANGLE_PER_SECTOR - rotation_angle)
        text_x = WHEEL_CENTER[0] + (WHEEL_RADIUS - 30) * math.cos(text_angle)
        text_y = WHEEL_CENTER[1] + (WHEEL_RADIUS - 30) * math.sin(text_angle)
        text = small_font.render(SECTOR_NAMES[i], True, BLACK)
        text_rect = text.get_rect(center=(text_x, text_y))
        screen.blit(text, text_rect)

    pygame.draw.circle(screen, BLACK, WHEEL_CENTER, WHEEL_RADIUS, 2)
    # Draw center indicator
    pygame.draw.polygon(screen,RED , [
        (WHEEL_CENTER[0] + WHEEL_RADIUS , WHEEL_CENTER[1]),
        (WHEEL_CENTER[0] + WHEEL_RADIUS + 20 , WHEEL_CENTER[1] + 10),
        (WHEEL_CENTER[0] + WHEEL_RADIUS + 20 , WHEEL_CENTER[1] - 10)])

# Функция для отображения результатов
def display_result(sector_index):
    text = font.render(f"Выпал сектор: {SECTOR_NAMES[sector_index]}", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(text, text_rect)

    # Функция для отображения загрузочного экрана


def show_loading_screen():
    screen.fill(WHITE)
    text = large_font.render("SteelFoxGames", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(2)  # Задержка на 2 секунды

    # Основной цикл игры


show_loading_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not spinning:
            spinning = True
            rotation_speed = random.randint(5, 15)
            start_time = pygame.time.get_ticks() / 1000
            target_sector = random.randint(0, NUM_SECTORS - 1)
            end_time = start_time + rotation_time + deceleration_time
            target_angle = target_sector * ANGLE_PER_SECTOR

    screen.fill(WHITE)
    draw_wheel()

    if spinning:
        current_time = pygame.time.get_ticks() / 1000
        if current_time < start_time + rotation_time:
            rotation_angle += rotation_speed
        elif current_time < end_time:
            time_progress = (current_time - (start_time + rotation_time)) / deceleration_time
            current_speed = rotation_speed * (1 - time_progress)
            rotation_angle += current_speed
            if current_speed < 0.1:
                spinning = False
                rotation_angle = target_angle
        else:
            spinning = False
            rotation_angle = target_angle

        rotation_angle %= 360
    else:
        if target_sector != -1:
            display_result(target_sector)
    pygame.display.flip()

pygame.quit()
