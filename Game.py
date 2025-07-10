import pygame
import random
import json
import time
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Shutter Typing Game")
clock = pygame.time.Clock()

# New Color Palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (13, 19, 33)
LIGHT_BLUE = (100, 149, 237)
TEAL = (0, 128, 128)
GOLD = (255, 215, 0)
CORAL = (255, 127, 80)
LAVENDER = (230, 230, 250)
MINT = (189, 252, 201)
SALMON = (250, 128, 114)
PURPLE = (147, 112, 219)
LIME = (50, 205, 50)
SKY_BLUE = (135, 206, 235)

# Fonts - Adjusted sizes to fit better
try:
    font_tiny = pygame.font.Font(None, 20)  # Reduced from 24
    font_small = pygame.font.Font(None, 28) # Reduced from 36
    font_medium = pygame.font.Font(None, 36) # Reduced from 48
    font_large = pygame.font.Font(None, 60)  # Reduced from 72
except:
    # Fallback if fonts fail to load
    font_tiny = pygame.font.SysFont('arial', 16)
    font_small = pygame.font.SysFont('arial', 20)
    font_medium = pygame.font.SysFont('arial', 28)
    font_large = pygame.font.SysFont('arial', 40)

# Sound effects (unchanged)
try:
    correct_sound = pygame.mixer.Sound("correct.wav")
    error_sound = pygame.mixer.Sound("error.wav")
    level_up_sound = pygame.mixer.Sound("level_up.wav")
    countdown_sound = pygame.mixer.Sound("countdown.wav")
except:
    correct_sound = pygame.mixer.Sound(buffer=bytearray(0))
    error_sound = pygame.mixer.Sound(buffer=bytearray(0))
    level_up_sound = pygame.mixer.Sound(buffer=bytearray(0))
    countdown_sound = pygame.mixer.Sound(buffer=bytearray(0))

# Word pool (unchanged)
word_pool = [
    "cat", "dog", "run", "sun", "code", "game", "type", "word", "key", "fun",
    "box", "zoo", "car", "map", "cup", "hat", "pen", "jam", "fox", "log",
    "python", "typing", "shooter", "keyboard", "display", "program", "develop",
    "rocket", "basket", "garden", "window", "monitor", "laptop", "digital",
    "algorithm", "mechanics", "keyboard", "challenge", "adventure", "programming",
    "beautiful", "dangerous", "happiness", "knowledge", "mountain", "quickly"
]

# Game variables (unchanged except for font size adjustments above)
active_words = []
current_input = ""
score = 0
high_score = 0
words_typed = 0
highest_words_typed = 0
game_over = False
game_started = False
game_playing = False
level = 1
base_speed = 0.5
combo = 0
max_combo = 0
word_count = 0
start_time = 0
countdown = 0
last_word_spawn = 0
paused = False
pause_time = 0
pause_duration = 0
least_time = float('inf')
current_time_taken = 0

# Explosion particles
explosions = []

# Load high scores from file (unchanged)
def load_high_scores():
    try:
        with open("highscores.json", "r") as f:
            data = json.load(f)
            if "score" not in data: data["score"] = 0
            if "words" not in data: data["words"] = 0
            if "least_time" not in data: data["least_time"] = float('inf')
            return data
    except:
        return {"score": 0, "words": 0, "least_time": float('inf')}

# Save high scores to file (unchanged)
def save_high_scores(score, words, least_time):
    with open("highscores.json", "w") as f:
        json.dump({"score": score, "words": words, "least_time": least_time}, f)

high_scores = load_high_scores()
high_score = high_scores["score"]
highest_words_typed = high_scores["words"]
least_time = high_scores["least_time"]

# Spawn word (unchanged)
def spawn_word():
    global word_count, last_word_spawn
    current_time = time.time()
    if current_time - last_word_spawn < max(0.5, 2.0 - (level * 0.05)):
        return
    
    word = random.choice(word_pool)
    word_width = font_medium.size(word)[0]
    x = random.randint(50, WIDTH - word_width - 50)
    y = 0
    
    if len(word) < 5:
        color = MINT
    elif len(word) < 8:
        color = SKY_BLUE
    else:
        color = CORAL
    
    speed = base_speed + (level * 0.02) + (len(word) * 0.02)
    active_words.append({
        "text": word, 
        "x": x, 
        "y": y, 
        "speed": speed,
        "color": color,
        "width": word_width
    })
    word_count += 1
    last_word_spawn = current_time

# Create explosion (unchanged)
def create_explosion(x, y, color):
    for _ in range(15):
        explosions.append({
            "x": x + random.randint(-20, 20),
            "y": y + random.randint(-20, 20),
            "vx": random.uniform(-3, 3),
            "vy": random.uniform(-8, -2),
            "life": random.randint(20, 40),
            "color": color
        })

# Draw text with shadow (unchanged)
def draw_text_shadow(text, font, color, x, y):
    text_width, text_height = font.size(text)
    shadow = font.render(text, True, DARK_BLUE)
    screen.blit(shadow, (x+2, y+2))
    main_text = font.render(text, True, color)
    screen.blit(main_text, (x, y))
    return text_width, text_height

def show_start_screen():
    screen.fill(DARK_BLUE)
    
    # Title with adjusted size and spacing
    title = "WORD SHUTTER"
    subtitle = "TYPING GAME"
    
    # Render title and subtitle separately
    title_surf = font_large.render(title, True, LIGHT_BLUE)
    subtitle_surf = font_medium.render(subtitle, True, GOLD)
    
    # Center both lines
    screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 40))
    screen.blit(subtitle_surf, (WIDTH//2 - subtitle_surf.get_width()//2, 40 + title_surf.get_height() + 5))
    
    # Instructions box with adjusted size
    pygame.draw.rect(screen, (30, 40, 50), (40, 120, WIDTH-80, 340), border_radius=10)
    pygame.draw.rect(screen, LIGHT_BLUE, (40, 120, WIDTH-80, 340), 2, border_radius=10)
    
    # Instructions with adjusted spacing
    instructions = [
        "HOW TO PLAY:",
        "- Type falling words and press ENTER",
        "- Longer words give more points",
        "- Build combos for bonus points",
        "- Game gets harder over time",
        "",
        "CONTROLS:",
        "- Type to input words",
        "- BACKSPACE to correct",
        "- ENTER to submit",
        "- ESC to pause"
    ]
    
    y_offset = 130
    for i, line in enumerate(instructions):
        if i == 0 or i == 6:  # Headers
            color = GOLD if i == 0 else LIGHT_BLUE
            font = font_small
        elif line.startswith("-"):
            color = LAVENDER
            font = font_tiny
        else:
            y_offset += 10  # Extra space for empty lines
            continue
            
        line_width = font.size(line)[0]
        draw_text_shadow(line, font, color, WIDTH//2 - line_width//2, y_offset)
        y_offset += 22  # Reduced from 25
    
    # High scores in a more compact format
    hs_text = f"High Score: {high_score} | Words: {highest_words_typed} | Best Time: {least_time if least_time != float('inf') else '--':.2f}s"
    hs_width = font_small.size(hs_text)[0]
    
    # Ensure it fits by reducing font if necessary
    if hs_width > WIDTH - 40:
        hs_font = pygame.font.Font(None, 20)
    else:
        hs_font = font_small
    
    pygame.draw.rect(screen, (20, 30, 40), (WIDTH//2 - hs_width//2 - 10, 470, hs_width + 20, 30), border_radius=5)
    draw_text_shadow(hs_text, hs_font, GOLD, WIDTH//2 - hs_width//2, 475)
    
    # Start prompt with blinking effect
    if int(time.time() * 2) % 2 == 0:
        start_text = "Press ENTER to Start"
        start_width = font_medium.size(start_text)[0]
        draw_text_shadow(start_text, font_medium, LIME, WIDTH//2 - start_width//2, 520)

def show_countdown():
    screen.fill(DARK_BLUE)
    
    # Draw stars in background
    for _ in range(50):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, WHITE, (x, y), 1)
    
    if countdown > 0:
        count_text = str(countdown)
        count_surf = font_large.render(count_text, True, CORAL)
        screen.blit(count_surf, (WIDTH//2 - count_surf.get_width()//2, HEIGHT//2 - 50))
        
        ready_text = "Get Ready!"
        ready_width = font_medium.size(ready_text)[0]
        draw_text_shadow(ready_text, font_medium, LAVENDER, WIDTH//2 - ready_width//2, HEIGHT//2 + 20)
    else:
        go_text = "GO!"
        go_width = font_large.size(go_text)[0]
        draw_text_shadow(go_text, font_large, LIME, WIDTH//2 - go_width//2, HEIGHT//2 - 50)

def show_pause_screen():
    # Darken the game screen
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    screen.blit(s, (0, 0))
    
    # Paused text
    paused_text = "PAUSED"
    paused_width = font_large.size(paused_text)[0]
    draw_text_shadow(paused_text, font_large, GOLD, WIDTH//2 - paused_width//2, HEIGHT//2 - 70)
    
    # Current time - more compact
    time_text = f"Time: {int(current_time_taken)}s"
    time_width = font_medium.size(time_text)[0]
    draw_text_shadow(time_text, font_medium, SKY_BLUE, WIDTH//2 - time_width//2, HEIGHT//2 - 20)
    
    # Instructions - stacked vertically to save space
    resume_text = "ESC: Resume"
    menu_text = "M: Main Menu"
    
    resume_width = font_medium.size(resume_text)[0]
    menu_width = font_medium.size(menu_text)[0]
    
    draw_text_shadow(resume_text, font_medium, LAVENDER, WIDTH//2 - resume_width//2, HEIGHT//2 + 30)
    draw_text_shadow(menu_text, font_medium, SALMON, WIDTH//2 - menu_width//2, HEIGHT//2 + 70)

def reset_game():
    global score, level, combo, base_speed, active_words
    global current_input, word_count, max_combo, words_typed, start_time, pause_duration
    score = 0
    level = 1
    combo = 0
    max_combo = 0
    base_speed = 0.5
    active_words = []
    current_input = ""
    word_count = 0
    words_typed = 0
    start_time = time.time()
    pause_duration = 0
    explosions.clear()

def update_difficulty():
    global base_speed, level, current_time_taken
    current_time_taken = (time.time() - start_time) - pause_duration
    
    if current_time_taken < 30:
        base_speed = 0.5
        level = 1
    else:
        level = min(20, 1 + int((current_time_taken - 30) / 15))
        base_speed = 0.5 + (level * 0.02)

def show_game_over_screen():
    screen.fill(DARK_BLUE)
    
    # Game over text
    game_over_text = "GAME OVER"
    go_width = font_large.size(game_over_text)[0]
    draw_text_shadow(game_over_text, font_large, CORAL, WIDTH//2 - go_width//2, 50)
    
    # Stats box - made more compact
    pygame.draw.rect(screen, (30, 40, 50), (50, 120, WIDTH-100, 350), border_radius=10)
    pygame.draw.rect(screen, LIGHT_BLUE, (50, 120, WIDTH-100, 350), 2, border_radius=10)
    
    # Stats in two columns to save space
    left_stats = [
        f"Score: {score}",
        f"Words: {words_typed}",
        f"Combo: {max_combo}x",
        f"Time: {int(current_time_taken):.2f}s"
    ]
    
    right_stats = [
        f"High Score: {high_score}",
        f"Best Words: {highest_words_typed}",
        f"Level: {level}",
        f"Best Time: {least_time if least_time != float('inf') else '--':.2f}s"
    ]
    
    left_colors = [LIME, SKY_BLUE, CORAL, TEAL]
    right_colors = [GOLD, PURPLE, MINT, LIGHT_BLUE]
    
    # Left column
    for i, (stat, color) in enumerate(zip(left_stats, left_colors)):
        stat_width = font_medium.size(stat)[0]
        draw_text_shadow(stat, font_medium, color, WIDTH//2 - 150 - stat_width//2, 140 + i * 50)
    
    # Right column
    for i, (stat, color) in enumerate(zip(right_stats, right_colors)):
        stat_width = font_medium.size(stat)[0]
        draw_text_shadow(stat, font_medium, color, WIDTH//2 + 150 - stat_width//2, 140 + i * 50)
    
    # Instructions at bottom
    restart_text = "ENTER: Play Again"
    menu_text = "ESC: Main Menu"
    
    rt_width = font_medium.size(restart_text)[0]
    mt_width = font_medium.size(menu_text)[0]
    
    # Blinking effect for restart text
    if int(time.time() * 2) % 2 == 0:
        draw_text_shadow(restart_text, font_medium, LIME, WIDTH//2 - rt_width//2, 480)
    draw_text_shadow(menu_text, font_medium, LAVENDER, WIDTH//2 - mt_width//2, 530)

# Main game loop
running = True
while running:
    current_time = time.time()
    screen.fill(DARK_BLUE)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if not game_started:
                if event.key == K_RETURN:
                    game_started = True
                    countdown = 3
                    last_countdown = current_time
            elif countdown > 0:
                pass
            elif game_over:
                if event.key == K_RETURN:
                    game_over = False
                    game_started = True
                    countdown = 3
                elif event.key == K_ESCAPE:
                    game_over = False
                    game_started = False
            else:
                if event.key == K_ESCAPE:
                    if not paused:
                        paused = True
                        pause_time = current_time
                        game_playing = False
                    else:
                        paused = False
                        pause_duration += current_time - pause_time
                        game_playing = True
                elif paused:
                    if event.key == K_m:
                        paused = False
                        game_started = False
                        game_playing = False
                elif event.key == K_RETURN:
                    matched = False
                    for word in active_words[:]:
                        if current_input == word["text"]:
                            active_words.remove(word)
                            score += 10 + (len(word["text"]) * 2)
                            words_typed += 1
                            combo += 1
                            if combo > max_combo:
                                max_combo = combo
                            matched = True
                            create_explosion(word["x"] + word["width"]//2, word["y"] + 10, word["color"])
                            correct_sound.play()
                            
                            if combo >= 3:
                                score += combo * 5
                            
                    if matched:
                        if score > high_score:
                            high_score = score
                        if words_typed > highest_words_typed:
                            highest_words_typed = words_typed
                        if current_time_taken < least_time:
                            least_time = current_time_taken
                        save_high_scores(high_score, highest_words_typed, least_time)
                    else:
                        combo = 0
                        if current_input:
                            error_sound.play()
                    current_input = ""
                elif event.key == K_BACKSPACE:
                    current_input = current_input[:-1]
                else:
                    current_input += event.unicode.lower()

    # Game state management
    if countdown > 0 and game_started:
        show_countdown()
        if current_time - last_countdown > 1:
            countdown -= 1
            last_countdown = current_time
            if countdown > 0:
                countdown_sound.play()
        if countdown == 0:
            reset_game()
            game_playing = True
    elif not game_started:
        show_start_screen()
    elif game_over:
        show_game_over_screen()
    elif paused:
        # Draw frozen game state
        for word in active_words:
            text_surface = font_medium.render(word["text"], True, word["color"])
            screen.blit(text_surface, (word["x"], word["y"]))
        
        for explosion in explosions:
            alpha = min(255, explosion["life"] * 6)
            s = pygame.Surface((10, 10))
            s.set_alpha(alpha)
            s.fill(explosion["color"])
            screen.blit(s, (int(explosion["x"]), int(explosion["y"])))
        
        pygame.draw.rect(screen, (30, 40, 50), (10, HEIGHT - 60, 300, 40), border_radius=5)
        pygame.draw.rect(screen, LIGHT_BLUE, (10, HEIGHT - 60, 300, 40), 2, border_radius=5)
        draw_text_shadow(f"Type: {current_input}", font_small, LAVENDER, 20, HEIGHT - 55)
        
        show_pause_screen()
    else:
        update_difficulty()
        spawn_word()

        # Update words and explosions
        for word in active_words[:]:
            word["y"] += word["speed"]
            if word["y"] > HEIGHT:
                active_words.remove(word)
                game_over = True
                if score > high_score:
                    high_score = score
                if words_typed > highest_words_typed:
                    highest_words_typed = words_typed
                if current_time_taken < least_time:
                    least_time = current_time_taken
                save_high_scores(high_score, highest_words_typed, least_time)

        for explosion in explosions[:]:
            explosion["x"] += explosion["vx"]
            explosion["y"] += explosion["vy"]
            explosion["life"] -= 1
            if explosion["life"] <= 0:
                explosions.remove(explosion)

        # Draw game elements
        for word in active_words:
            text_surface = font_medium.render(word["text"], True, word["color"])
            screen.blit(text_surface, (word["x"], word["y"]))

        for explosion in explosions:
            alpha = min(255, explosion["life"] * 6)
            s = pygame.Surface((10, 10))
            s.set_alpha(alpha)
            s.fill(explosion["color"])
            screen.blit(s, (int(explosion["x"]), int(explosion["y"])))

        # Draw UI - made more compact
        # Input box (smaller)
        pygame.draw.rect(screen, (30, 40, 50), (10, HEIGHT - 60, 250, 40), border_radius=5)
        pygame.draw.rect(screen, LIGHT_BLUE, (10, HEIGHT - 60, 250, 40), 2, border_radius=5)
        draw_text_shadow(f"Type: {current_input}", font_small, LAVENDER, 20, HEIGHT - 55)
        
        # Score display (top right)
        score_text = f"{score}"
        score_width = font_small.size(score_text)[0]
        pygame.draw.rect(screen, (30, 40, 50), (WIDTH - score_width - 30, 10, score_width + 20, 30), border_radius=5)
        draw_text_shadow(score_text, font_small, WHITE, WIDTH - score_width - 20, 15)
        
        # Level display (top left)
        level_text = f"Lvl {level}"
        level_width = font_small.size(level_text)[0]
        pygame.draw.rect(screen, (30, 40, 50), (10, 10, level_width + 20, 30), border_radius=5)
        draw_text_shadow(level_text, font_small, WHITE, 20, 15)
        
        # Combo display (below score)
        if combo > 0:
            combo_text = f"{combo}x"
            combo_width = font_small.size(combo_text)[0]
            combo_color = (min(255, 100 + combo * 10), min(255, 200 + combo * 5), 100)
            pygame.draw.rect(screen, (30, 40, 50), (WIDTH - combo_width - 30, 45, combo_width + 20, 30), border_radius=5)
            draw_text_shadow(combo_text, font_small, combo_color, WIDTH - combo_width - 20, 50)
        
        # Words typed (below level)
        words_text = f"{words_typed}"
        words_width = font_small.size(words_text)[0]
        pygame.draw.rect(screen, (30, 40, 50), (10, 45, words_width + 20, 30), border_radius=5)
        draw_text_shadow(words_text, font_small, MINT, 20, 50)
        
        # Time played (center top)
        time_text = f"{int(current_time_taken)}s"
        time_width = font_small.size(time_text)[0]
        pygame.draw.rect(screen, (30, 40, 50), (WIDTH//2 - time_width//2 - 10, 10, time_width + 20, 30), border_radius=5)
        draw_text_shadow(time_text, font_small, SKY_BLUE, WIDTH//2 - time_width//2, 15)
        
        # Progress to next level (only show after 30s)
        if current_time_taken > 30:
            progress = min(1.0, ((current_time_taken - 30) % 15) / 15)
            pygame.draw.rect(screen, (30, 40, 50), (WIDTH//2 - 52, 50, 104, 12), border_radius=5)
            pygame.draw.rect(screen, LIGHT_BLUE, (WIDTH//2 - 50, 50, 100 * progress, 10), border_radius=5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
