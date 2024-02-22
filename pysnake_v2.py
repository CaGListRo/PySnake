import pygame as py
from random import randint

py.init()
clock = py.time.Clock()
RES = (750, 600)
GAME_RES = (500, 500)
ROW = GAME_RES[0] // 25

SNAKE = [[GAME_RES[0] // 2 + ROW // 2, GAME_RES[1] // 2 - ROW // 2], 
         [GAME_RES[0] // 2 - ROW // 2, GAME_RES[1] // 2 - ROW // 2], 
         [GAME_RES[0] // 2 - ROW // 2 - ROW, GAME_RES[1] // 2 - ROW // 2]]

GAME_OVER_FONT = py.font.SysFont("comicsans", ROW * 3)
GAME_OVER_TEXT = GAME_OVER_FONT.render("!!! GAME OVER !!!", 1, "green")
SCORE_FONT = py.font.SysFont("comicsans", ROW * 2, True)

FPS = 60
WIN = py.display.set_mode(RES)
GAME_WIN = py.Surface(GAME_RES)

bg_image = py.transform.scale(py.image.load("images/graue-schlangenhaut.jpg"), (RES[0], RES[1]))

def get_highscore():
    try:
        with open ("data/snake_highscore") as f:
            return f.readline()
    except FileNotFoundError:
        with open ("data/snake_highscore", "w") as f:
            f.write("0")

def set_highscore(highscore, score):
    check_highscore = max(int(highscore), score)
    with open ("data/snake_highscore", "w") as f:
        f.write(str(check_highscore))

def check_bit_tail(snake):
    for i in range(1, len(snake)):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            return True
    return False

def check_eating(food, snake, direction):
    if direction == "left":
        if snake[0][0] - ROW == food[0] * ROW and snake[0][1] == food[1] * ROW:
            return True
    elif direction == "right":
        if snake[0][0] + ROW == food[0] * ROW and snake[0][1] == food[1] * ROW:
            return True
    elif direction == "up":
        if snake[0][1] - ROW == food[1] * ROW and snake[0][0] == food[0] * ROW:
            return True   
    elif direction == "down":
        if snake[0][1] + ROW == food[1] * ROW and snake[0][0] == food[0] * ROW:
            return True
    return False

def create_food(snake):
    c = 0
    while True:
        c += 1
        food_x = randint(1, ROW -1)
        food_y = randint(1, ROW -1)
        # print(c, ": ", food_x * ROW, food_y * ROW)
        if [food_x * ROW, food_y * ROW] in snake:
            continue
        else:
            break      
    return [food_x, food_y]
     
def move_snake(snake, direction, grow=False):
    if direction == "left":
            new_pos = [snake[0][0] - ROW, snake[0][1]]
            if new_pos[0] < 0:
                 new_pos[0] = GAME_RES[0] - ROW
    elif direction == "right":
            new_pos = [snake[0][0] + ROW, snake[0][1]]
            if new_pos[0] >= GAME_RES[0]:
                 new_pos[0] = 0
    elif direction == "up":
            new_pos = [snake[0][0], snake[0][1] - ROW]
            if new_pos[1] < 0:
                 new_pos[1] = GAME_RES[1] - ROW
    elif direction == "down":
            new_pos = [snake[0][0], snake[0][1] + ROW]
            if new_pos[1] >= GAME_RES[1]:
                 new_pos[1] = 0
    for i in range(len(snake)):
        old_pos = snake[i]
        snake[i] = new_pos
        new_pos = old_pos
    if grow:
        snake.append(old_pos)
    return snake

def set_snake(snake):
    del snake[:]
    for i in range(len(SNAKE)):
        snake.append(SNAKE[i])
    return snake

def draw_window(win, snake, direction, food, score, highscore):
    py.display.set_caption(f"             PySnake V2             Score: {score}             Highscore: {highscore}")
    WIN.blit(bg_image, (0, 0))
    py.draw.rect(WIN, "white", (530, 180, 220, 300))
    py.draw.rect(WIN, (10, 10, 10), (532, 182, 216, 296))
    score_text = SCORE_FONT.render("Score:", 1, "yellow")
    score_value_text = SCORE_FONT.render(str(score), 1, "yellow")
    WIN.blit(score_text, (580, 200))
    WIN.blit(score_value_text, (680, 250))
    highscore_text = SCORE_FONT.render("Highscore:", 1, "darkorange")
    highscore_value_text = SCORE_FONT.render(str(highscore), 1, "darkorange")
    WIN.blit(highscore_text, (540, 350))
    WIN.blit(highscore_value_text, (680, 400))
    py.draw.rect(WIN, "white", (18, 48, GAME_RES[0] + 4, GAME_RES[0] + 4))
    WIN.blit(win, (20, 50))
    win.fill("black")
    # draw grid
    for i in range(GAME_RES[0]):
        py.draw.line(win, (20, 20, 20), (i * ROW, 0), (i * ROW, GAME_RES[0]))
        py.draw.line(win, (20, 20, 20), (0, i * ROW), (GAME_RES[0], i * ROW))
    # draw food
    py.draw.circle(win, "orange", (food[0] * ROW + ROW // 2, food[1] * ROW + ROW // 2), ROW // 3)
    # draw snake
    for i in range(len(snake)):
        py.draw.rect(win, "green", (snake[i][0], snake[i][1], ROW, ROW))
        if i != 0:
            py.draw.rect(win, "darkgreen", (snake[i][0] + 5, snake[i][1] + 5, ROW - 10, ROW - 10))
        if i == 0:
            if direction == "right":
                py.draw.circle(win, "red", (snake[i][0] + ROW // 4 * 3, snake[i][1] + ROW // 4 * 3), ROW // 5)
                py.draw.circle(win, "red", (snake[i][0] + ROW // 4 * 3, snake[i][1] + ROW // 4), ROW // 5)
            elif direction == "left":
                py.draw.circle(win, "red", (snake[i][0] + ROW // 4, snake[i][1] + ROW // 4), ROW // 5)
                py.draw.circle(win, "red", (snake[i][0] + ROW // 4, snake[i][1] + ROW // 4 * 3), ROW // 5)
            elif direction == "up":
                py.draw.circle(win, "red", (snake[i][0] + ROW // 4, snake[i][1] + ROW // 4), ROW // 5)
                py.draw.circle(win, "red", (snake[i][0] + ROW // 4 * 3, snake[i][1] + ROW // 4), ROW // 5)
            elif direction == "down":
                py.draw.circle(win, "red", (snake[i][0] + ROW // 4, snake[i][1] + ROW // 4 * 3), ROW // 5)
                py.draw.circle(win, "red", (snake[i][0] + ROW // 4 * 3, snake[i][1] + ROW // 4 * 3), ROW // 5)

    py.display.update()

def main():
    anim_count, anim_speed, anim_limit = 0, 60, 2000
    highscore = get_highscore()
    direction = "right"
    snake = []
    run = True
    snake = set_snake(snake)
    food_there = False
    game_over = False
    score = 0
    while run:
        clock.tick(FPS)
        anim_count += anim_speed
        if not food_there:
            food = create_food(snake)
            food_there = True
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                exit()
            keys = py.key.get_pressed()
            if keys[py.K_ESCAPE]:
                run = False
                exit()
            if keys[py.K_LEFT] and direction != "right":
                direction = "left" 
            elif keys[py.K_RIGHT] and direction != "left":
                direction = "right"
            elif keys[py.K_UP] and direction != "down":
                direction = "up"
            elif keys[py.K_DOWN] and direction != "up":
                direction = "down"
        if anim_count >= anim_limit:
            grow = check_eating(food, snake, direction)
            snake = move_snake(snake, direction, grow)
            game_over = check_bit_tail(snake)
            if game_over:
                set_highscore(highscore, score)
                GAME_WIN.blit(GAME_OVER_TEXT, (GAME_RES[0] // 2 - GAME_OVER_TEXT.get_width() // 2, GAME_RES[1] // 2 - GAME_OVER_TEXT.get_height() // 2))
                draw_window(GAME_WIN, snake, direction, food, score, highscore)
                py.display.update()
                py.time.delay(3000)
                highscore = get_highscore()
                score, anim_count, anim_speed, anim_limit = 0, 0, 60, 2000
                direction = "right"
                snake = set_snake(snake)
            if grow:
                food_there = False
                anim_speed += 1
                score += 1
            anim_count = 0
        draw_window(GAME_WIN, snake, direction, food, score, highscore)



if __name__ == "__main__":
    main()