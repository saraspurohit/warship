import pygame
import random
import os

# Colors
black = (0, 0, 0)
pink = (233, 220, 229)
white = (255, 255, 255)

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Saras Ka spaceship!")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# High score file
high_score_file = 'high_score.txt'

def get_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, 'r') as file:
            try:
                return int(file.read())
            except ValueError:
                return 0
    return 0

def save_high_score(score):
    with open(high_score_file, 'w') as file:
        file.write(str(score))

def welcome_screen():
    running = True
    while running:
        screen.fill(pink)
        img = pygame.image.load('start.jpg')
        size = pygame.transform.scale(img, (600, 600))
        screen.blit(size, (0, 0))
        title_text = font.render("Welcome to Saras Ka spaceship!", True, black)
        start_text = font.render("Press Enter To Start", True, black)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, screen.get_height() // 2 - title_text.get_height() // 2))
        screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, screen.get_height() // 2 + title_text.get_height()))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Exit the welcome_screen function and start the game
        clock.tick(1)

def game_over(score, high_score):
    running = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('game  over.mp3')
    pygame.mixer.music.play()

    while running:
        screen.fill(pink)
        text = font.render(f"Game Over! Score: {score}", True, black)
        high_score_text = font.render(f"High Score: {high_score}", True, black)
        retry_text = font.render("Press Enter To Restart", True, black)
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
        screen.blit(high_score_text, (screen.get_width() // 2 - high_score_text.get_width() // 2, screen.get_height() - high_score_text.get_height() - 10))
        screen.blit(retry_text, (screen.get_width() // 2 - retry_text.get_width() // 2, screen.get_height() // 2 + text.get_height()))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return  # Exit the game_over function and return to main_game
        clock.tick(1)

def main_game():
    running = True
    dt = 0
    score = 0
    pygame.mixer.music.load('song.mp3')
    pygame.mixer.music.play(-1)  # Loop the music
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    image = pygame.image.load('background.jpg')
    size = pygame.transform.scale(image, (600, 600))

    rocket = pygame.image.load('rocket.png')
    rocket = pygame.transform.scale(rocket, (100, 70))

    lines = []
    line_speed = 200
    line_gap = 150
    line_height = 20
    new_line_event = pygame.USEREVENT + 1
    pygame.time.set_timer(new_line_event, 1500)  # Add a new line every 1.5 seconds

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == new_line_event:
                gap_start = random.randint(100, 600 - line_gap)
                lines.append((0, gap_start))  # Initialize at the top of the screen

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_pos.x += 300 * dt

        screen.fill(black)

        if player_pos.x < 0 or player_pos.x > screen.get_width() - rocket.get_width() or player_pos.y < 0 or player_pos.y > screen.get_height() - rocket.get_height():
            return score

        screen.blit(size, (0, 0))
        screen.blit(rocket, (player_pos.x, player_pos.y))

        new_lines = []
        for line_y, gap_start in lines:
            line_y += line_speed * dt  # Move the lines down
            if line_y < screen.get_height():
                new_lines.append((line_y, gap_start))

            if (line_y < player_pos.y < line_y + line_height or line_y < player_pos.y + rocket.get_height() < line_y + line_height):
                if not (gap_start < player_pos.x < gap_start + line_gap or gap_start < player_pos.x + rocket.get_width() < gap_start + line_gap):
                    return score

            if line_y > player_pos.y + rocket.get_height():
                score += 1

            pygame.draw.rect(screen, white, (0, line_y, gap_start, line_height))
            pygame.draw.rect(screen, white, (gap_start + line_gap, line_y, screen.get_width() - (gap_start + line_gap), line_height))

        lines = new_lines

        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    high_score = get_high_score()  # Load the high score from the file at the start
    first_time = True  # Flag to track the first time the game starts
    while True:
        if first_time:
            welcome_screen()  # Display the welcome screen only the first time
            first_time = False
        score = main_game()  # Start the main game loop
        if score > high_score:
            high_score = score
            save_high_score(high_score)  # Save the new high score if it's higher than the previous one
        game_over(score, high_score)  # Transition to the game over screen when main_game returns


