import pygame
import random
from dataclasses import dataclass

max_score = [0]


@dataclass
class Snake:
    x: int
    y: int
    body: list

    def __post_init__(self):
        self.body = [(self.x, self.y)]

    def draw(self, screen):
        self.body.append((self.x, self.y))
        for (i, j) in self.body:
            pygame.draw.rect(screen, "yellow", [i, j, 50, 50])
        del self.body[0]

    def move(self):
        self.body += [(self.x, self.y)]

    def moveX_right(self):
        self.x += 50

    def moveX_left(self):
        self.x -= 50

    def moveY_up(self):
        self.y -= 50

    def moveY_down(self):
        self.y += 50


@dataclass
class Apple:
    x: int
    y: int

    def body(self, screen, snake, apple):
        cord = [a for a in range(0, 750) if a % 50 == 0]
        self.x = random.choice(cord)
        self.y = random.choice(cord)

        if (self.x, self.y) in snake.body:
            apple.body(screen, snake, apple)

    def draw(self, screen):
        pygame.draw.rect(screen, "blue", [self.x, self.y, 50, 50])


def game():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    fps = pygame.time.Clock()
    running = True
    snake = Snake(50, 50, [])
    apple = Apple(100, 100)
    font = pygame.font.Font(None, 18)
    d = "down"
    score = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and d != "right":
                    d = "left"
                if event.key == pygame.K_RIGHT and d != "left":
                    d = "right"
                if event.key == pygame.K_DOWN and d != "up":
                    d = "down"
                if event.key == pygame.K_UP and d != "down":
                    d = "up"
        if d == "left":
            snake.moveX_left()
        elif d == "right":
            snake.moveX_right()
        elif d == "down":
            snake.moveY_down()
        elif d == "up":
            snake.moveY_up()
        if (snake.x, snake.y) in snake.body:
            max_score.append(score)
            running = False
            game()
        if apple.x == snake.x and apple.y == snake.y:
            apple.body(screen, snake, apple)
            score += 1
            snake.move()
        screen.fill("black")
        snake.draw(screen)
        apple.draw(screen)
        text = font.render("SCORE: " + str(score), True, (255, 255, 255))
        text2 = font.render("HIGHSCORE: " + str(max(max_score)), True, (255, 255, 255))
        screen.blit(text, (0, 0))
        screen.blit(text2, (75, 0))
        if snake.x < 0 or snake.x > 800:
            max_score.append(score)
            running = False
            game()
        elif snake.y < 0 or snake.y > 800:
            max_score.append(score)
            running = False
            game()
        pygame.display.update()
        fps.tick(10)
    pygame.quit()


game()