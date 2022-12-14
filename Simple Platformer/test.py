import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

pygame.display.set_caption('Platformer Game')

WINDOW_SIZE = (900, 600)

screen = pygame.display.set_mode(WINDOW_SIZE)

game_font = pygame.font.Font('Pixeltype.ttf', 175)

player = pygame.Rect(100, 100, 40, 40)

# load map from .txt file
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('map')

# append tile rects to list and draw them
def draw_map(game_map):
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile != '.':
                tile_rects.append(pygame.Rect(x*16, y*16, 16, 16))
                pygame.draw.rect(screen, 'firebrick1', pygame.Rect( x*16, y*16, 16, 16))
            x += 1
        y += 1
    return tile_rects

# find collisions between given character and tiles   
def get_collisions(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions

# get player input and make array with x and y direction with player direction
def get_input():
    left = False
    right = False
    up = False
    direction = [0, 0]
    if pygame.key.get_pressed()[K_LEFT]:
        left = True
    if pygame.key.get_pressed()[K_RIGHT]:
        right = True
    if pygame.key.get_pressed()[K_UP]:
        up = True
    if left:
        direction[0] = -1
    if right:
        direction[0] = 1
    if left and right:
        direction[0] = 0
    if up:
        direction[1] = -1
    return direction


def solve_movement(rect, tiles, direction, x_accel, x_decel, y_accel, velocity, max_velocity):
    # create an array that determines the player's velocity in each direction
    velocity[1] += y_accel
    if direction[0] == 1:
        velocity[0] += x_accel
        if velocity[0] > max_velocity:
            velocity[0] = max_velocity
    if direction[0] == -1:
        velocity[0] -= x_accel
        if velocity[0] < -max_velocity:
            velocity[0] = -max_velocity
    if direction[0] == 0:
        if velocity[0] > 0:
            velocity[0] -= x_decel
            if velocity[0] < x_decel:
                velocity[0] = 0
        elif velocity[0] < 0:
            velocity[0] += x_decel
            if velocity[0] > -x_decel:
                velocity[0] = 0

    # apply movement to character, test for collisions, and adjust player position
    collide_left = False
    collide_right = False
    collide_top = False
    collide_bottom = False
    rect.x += velocity[0]
    collisions = get_collisions(rect, tiles)
    for tile in collisions:
        if velocity[0] > 0:
            rect.right = tile.left
            collide_right = True
            velocity[0] = 0
        if velocity[0] < 0:
            rect.left = tile.right
            collide_left = True
            velocity[0] = 0
    rect.y += velocity[1]
    collisions = get_collisions(rect, tiles)
    for tile in collisions:
        if velocity[1] > 0:
            rect.bottom = tile.top
            collide_bottom = True
            velocity[1] = 0
        if velocity[1] < 0:
            rect.top = tile.bottom
            collide_top = True
            velocity[1] = 0

    # jump and wall Jump (can be moved to a new Function)
    if direction[1] == -1:
        if collide_bottom == True:
            velocity[1] = -15
        elif collide_right == True:
            velocity[0] = -10.6066
            velocity[1] = -10.6066
        elif collide_left == True:
            velocity[0] = 10.6066
            velocity[1] = -10.6066
    # slow player down when sliding on a wall
    if collide_right or collide_left and not collide_bottom:
        if velocity[1] > 1:
            velocity[1] = 1
    return rect


velocity = [0, 0]

coin_rects = [pygame.Rect(180, 240, 20, 20), pygame.Rect(220, 240, 20, 20),
              pygame.Rect(260, 240, 20, 20), pygame.Rect(350, 240, 20, 20),
              pygame.Rect(180, 50, 20, 20), pygame.Rect(180, 510, 20, 20),
              pygame.Rect(220, 510, 20, 20), pygame.Rect(260, 510, 20, 20),
              pygame.Rect(180, 470, 20, 20), pygame.Rect(220, 470, 20, 20),
              pygame.Rect(260, 470, 20, 20)]

num_coins = len(coin_rects)
coins_collected = 0

win_surf = game_font.render('You Win!', False, 'white')
win_rect = win_surf.get_rect(center = (450, 300))

win = False

while True: # game loop (runs every frame)
    # clear screen
    screen.fill('black')
    # append tiles in map to a list and draw them
    tile_rects = draw_map(game_map)
    # get player input and return direction of player movement
    direction = get_input()
    # use the direction of player to move the player and handle collisions
    player = solve_movement(player, tile_rects, direction, 0.5, 0.8, 1, velocity, 10)
    # character loops back when exiting the screen
    if player.top > WINDOW_SIZE[1]:
        player.bottom = 0
    if player.bottom < 0:
        player.top = WINDOW_SIZE[1]
    if player.left > WINDOW_SIZE[0]:
        player.right = 0
    if player.right < 0:
        player.left = WINDOW_SIZE[0]
    # draw the player
    pygame.draw.rect(screen, 'aquamarine', player)

    if win == True:
        screen.blit(win_surf, win_rect)

    # tracks coin collection and win condition
    coin_collisions = get_collisions(player, coin_rects)
    for coin in coin_collisions:
        coin_rects.remove(coin)
        coins_collected += 1
        if coins_collected == num_coins:
            win = True
        
    for coin in coin_rects:
        pygame.draw.rect(screen, 'khaki1', coin)

    # allows player to exit the game
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
