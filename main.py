# Getting started
import os
import random
import pygame
import time

pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Load the background music file
background_music_file_path = "galaxy_music.mp3"
pygame.mixer.music.load(background_music_file_path)

# Set the volume (optional)
pygame.mixer.music.set_volume(0.3)  # Adjust the volume as needed (0.0 to 1.0)

# Start playing the background music in a loop
pygame.mixer.music.play(-1)
laser_file_path = "laser_sound.mp3"
explosion_file_path = "explosion_sound.mp3"

# import the turtle module
import turtle


screen = turtle.Screen()
screen.bgpic("galaxy_design.gif")  # Update file extension to PNG
screen.setup(width=900, height=900)
turtle.speed(0)
screen.bgcolor("black")
turtle.title("Space Wars")
turtle.ht()
turtle.setundobuffer(1)
screen.tracer(0)

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed_value = 1

    def move(self):
        self.fd(self.speed_value)
        # Boundary
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        if (
            (self.xcor() >= (other.xcor() - 20))
            and (self.xcor() <= (other.xcor() + 20))
            and (self.ycor() >= (other.ycor() - 20))
            and (self.ycor() <= (other.ycor() + 20))
        ):
            return True
        else:
            return False


class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed_value = 4
        self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed_value += 1

    def decelerate(self):
        self.speed_value -= 1


class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed_value = 6
        self.setheading(random.randint(0, 360))

    def increase_speed(self):
        self.speed_value += 1


class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed_value = 6
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed_value)
        # Boundary
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)


class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed_value = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            laser_sound = pygame.mixer.Sound(laser_file_path)
            laser_sound.play()
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)
        if self.status == "firing":
            self.fd(self.speed_value)
        # border check
        if (
            self.xcor() < -290
            or self.xcor() > 290
            or self.ycor() > 290
            or self.ycor() < -290
            or self.ycor() > 290
        ):
            self.goto(-1000, 1000)
            self.status = "ready"


class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1
        if self.frame > 20:
            self.frame = 0
            self.goto(-1000, -1000)


class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.penup()
        self.pen.goto(-300, 300)
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = f"Level: {self.level}  Score: {self.score}  Lives: {self.lives}"
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

    def next_level(self):
        self.level += 1
        self.score += 100
        self.show_status()

        # Increase the difficulty for the next level
        for enemy in enemies:
            enemy.increase_speed()

        for ally in allies:
            ally.increase_speed()

        self.pen.clear()
        self.draw_border()
        self.show_status()

# Create game object
game = Game()

# Draw game border
game.draw_border()

# Show the game status
game.show_status()

# Create my sprites
player = Player("triangle", "white", 0, 0)
player.goto(0, 0)
missile = Missile("triangle", "yellow", 0, 0)

enemies = []
for i in range(3):
    enemy = Enemy("circle", "red", random.randint(-250, 250), random.randint(-250, 250))
    enemies.append(enemy)

allies = []
for i in range(3):
    ally = Ally("square", "blue", random.randint(-250, 250), random.randint(-250, 250))
    allies.append(ally)

particles = []
for i in range(20):
    particles.append(Particle("circle", "orange", 0, 0))

# Keyboard bindings
turtle.listen()
turtle.onkeypress(player.turn_left, "Left")
turtle.onkeypress(player.turn_right, "Right")
turtle.onkeypress(player.accelerate, "Up")
turtle.onkeypress(player.decelerate, "Down")
turtle.onkeypress(missile.fire, "space")

# Main game Loop
while game.lives > 0:
    turtle.update()
    time.sleep(0.025)

    player.move()
    missile.move()

    # enemies
    for enemy in enemies:
        enemy.move()
        if player.is_collision(enemy):
            explosion_sound = pygame.mixer.Sound(explosion_file_path)
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.lives -= 1
            game.show_status()

        if missile.is_collision(enemy):
            explosion_sound = pygame.mixer.Sound(explosion_file_path)
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            game.score += 100
            game.show_status()
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    # allies
    for ally in allies:
        ally.move()
        if player.is_collision(ally):
            explosion_sound = pygame.mixer.Sound(explosion_file_path)
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            game.lives -= 1
            game.show_status()

        if missile.is_collision(ally):
            explosion_sound = pygame.mixer.Sound(explosion_file_path)
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            game.score -= 50
            game.show_status()

    for particle in particles:
        particle.move()

    # Check if the player has cleared the current level
    if all(enemy.xcor() > 290 for enemy in enemies):
        game.next_level()

# Game over
turtle.bye()
print("Game Over")
