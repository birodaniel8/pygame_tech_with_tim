# py -3.8 -m pip install pygame
import pygame
import os
pygame.font.init()
pygame.init()


# base appearance settings:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
FPS = 60
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship game")  # app title

# base game settings:
VELOCITY = 5  # spaceship spead
BULLET_VELOCITY = 7  # bullet spead
MAX_BULLETS = 10  # max number of bullets fired by each player
wasd_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
arrow_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)  # separating border

# user generated events (for hitting the other spaceship)
YELLOW_HIT = pygame.USEREVENT + 1  # these numbers are just identifiers
RED_HIT = pygame.USEREVENT + 2

# load and transform images:
SPACE = pygame.image.load(os.path.join("Assets", "space.png"))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# load sounds:
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE)  # backgroud color
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # health text:
    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))

    # add spaceships:
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    # fire bullets:
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def spaceship_movement(spaceship, velocity, keys_pressed, direction_keys, border_side):
    # movement for the left from border spaceship:
    if border_side == "left":
        if keys_pressed[direction_keys[0]] and spaceship.x - velocity > 0:  # left
            spaceship.x -= velocity
        if keys_pressed[direction_keys[1]] and spaceship.x + velocity + spaceship.width < BORDER.x:  # right
            spaceship.x += velocity
    # movement for the right from border spaceship:
    else:
        if keys_pressed[direction_keys[0]] and spaceship.x - velocity > BORDER.x + BORDER.width:  # left
            spaceship.x -= velocity
        if keys_pressed[direction_keys[1]] and spaceship.x + velocity + spaceship.width < WIDTH:  # right
            spaceship.x += velocity
    # up and down movement for both type:
    if keys_pressed[direction_keys[2]] and spaceship.y - velocity > 0:  # up
        spaceship.y -= velocity
    if keys_pressed[direction_keys[3]] and spaceship.y + velocity + spaceship.height < HEIGHT - 15:  # down
        spaceship.y += velocity


def bullet_movement(red_bullets, yellow_bullets, red, yellow):
    # red bullets:
    for bullet in red_bullets:
        bullet.x += BULLET_VELOCITY  # fire red bullet
        # if yellow has been hit, call the YELLOW_HIT event and remove bullet:
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        # also if it is outside the window:
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
    # yellow bullets:
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VELOCITY  # fire yellow bullet
        # if red has been hit, call the RED_HIT event and remove bullet:
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        # also if it is outside the window:
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)  # wait 5 sec


def main():
    # initialize spaceships:
    red = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 3
    yellow_health = 3

    clock = pygame.time.Clock()
    run = True
    while run:
        # controlling FPS:
        clock.tick(FPS)

        for event in pygame.event.get():
            # quit event:
            if event.type == pygame.QUIT:
                pygame.quit()

            # add bullets:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(red_bullets) <= MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width - 3, red.y + red.height // 2 - 2, 10, 4)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()  # play bullet sound
                if event.key == pygame.K_RCTRL and len(yellow_bullets) <= MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height // 2 - 2, 10, 4)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # hit event:
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # move spaceships:
        spaceship_movement(red, VELOCITY, pygame.key.get_pressed(), wasd_keys, "left")
        spaceship_movement(yellow, VELOCITY, pygame.key.get_pressed(), arrow_keys, "right")

        # bullet movement:
        bullet_movement(red_bullets, yellow_bullets, red, yellow)

        # draw window:
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        # check the winner:
        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS!"
        if yellow_health <= 0:
            winner_text = "RED WINS!"
        if winner_text != "":
            draw_winner(winner_text)  # someone won
            break

    # restart the game:
    main()


if __name__ == '__main__':
    main()
