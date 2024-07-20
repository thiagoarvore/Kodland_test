import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Alien Invasion')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

player_image = pygame.image.load('sprites/player.png')
enemy_image = pygame.image.load('sprites/red.png')

player_size = 50
enemy_size = 50
player_image = pygame.transform.scale(player_image, (player_size, player_size))
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))

player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
enemy_list = []
bullet_list = []

speed = 10
enemy_speed = 2
bullet_speed = 20
bullet_width = 5
bullet_height = 20

MAIN_MENU = "main_menu"
GAME = "game"
GAME_OVER = "game_over"
state = MAIN_MENU

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def detect_collision(obj1_pos, obj2_pos, obj1_size, obj2_size):
    o1_x, o1_y = obj1_pos
    o2_x, o2_y = obj2_pos

    if (o2_x >= o1_x and o2_x < (o1_x + obj1_size)) or (o1_x >= o2_x and o1_x < (o2_x + obj2_size)):
        if (o2_y >= o1_y and o2_y < (o1_y + obj1_size)) or (o1_y >= o2_y and o1_y < (o2_y + obj2_size)):
            return True
    return False

def create_enemy():
    enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
    enemy_list.append(enemy_pos)

def game_loop():
    global state, enemy_list, player_pos, speed, enemy_speed

    clock = pygame.time.Clock()
    running = True
    death_count = 0

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_pos[0] -= player_size
                if event.key == pygame.K_RIGHT:
                    player_pos[0] += player_size
                if event.key == pygame.K_SPACE and state == GAME:
                    bullet_pos = [player_pos[0] + player_size // 2 - bullet_width // 2, player_pos[1]]
                    bullet_list.append(bullet_pos)

        if state == MAIN_MENU:
            draw_text('Alien Invasion', font, WHITE, screen, WIDTH // 2, HEIGHT // 4)
            draw_text('Aperte espaço para começar', small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
            draw_text('Aperte Q(quit) para sair', small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 40)
            pygame.display.update()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                state = GAME
                enemy_list.clear()
                bullet_list.clear()
                player_pos[0] = WIDTH // 2
            elif keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

        elif state == GAME:
            if random.randint(0, 30) < 1:
                create_enemy()

            for enemy_pos in enemy_list:
                enemy_pos[1] += enemy_speed
                if enemy_pos[1] > HEIGHT:
                    enemy_list.remove(enemy_pos)

            for bullet_pos in bullet_list:
                bullet_pos[1] -= bullet_speed
                if bullet_pos[1] < 0:
                    bullet_list.remove(bullet_pos)

            for bullet_pos in bullet_list:
                for enemy_pos in enemy_list:
                    if detect_collision(bullet_pos, enemy_pos, bullet_width, enemy_size):
                        bullet_list.remove(bullet_pos)
                        enemy_list.remove(enemy_pos)
                        death_count += 1
                        if death_count % 10 == 0:
                            enemy_speed += 1
                        break

            for enemy_pos in enemy_list:
                if detect_collision(player_pos, enemy_pos, player_size, enemy_size):
                    state = GAME_OVER

            for enemy_pos in enemy_list:
                screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))

            for bullet_pos in bullet_list:
                pygame.draw.rect(screen, BLUE, (bullet_pos[0], bullet_pos[1], bullet_width, bullet_height))

            screen.blit(player_image, (player_pos[0], player_pos[1]))

            draw_text(f'Aliens derrotados: {death_count}', small_font, WHITE, screen, WIDTH - WIDTH // 5, HEIGHT // 10)

            pygame.display.update()

        elif state == GAME_OVER:
            draw_text('Game Over', font, RED, screen, WIDTH // 2, HEIGHT // 4)
            draw_text('Press R to Restart', small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
            draw_text('Press Q to Quit', small_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 40)
            pygame.display.update()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                state = MAIN_MENU
                death_count = 0
                enemy_speed = 2
            elif keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

        clock.tick(30)

if __name__ == "__main__":
    game_loop()
