# BlockDodge
# Based off of Sentex's Youtube tutorial: https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ
# Version 0.55

# Known bugs:
# Crossing x axes when moving up causes a crash
# Can't keep counting up when touching red box

import pygame
import time
import random

pygame.init()


display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255,0,0)
bright_green = (0,255,0)
block_color = (53, 114, 255)
green = (0,200,0)
car_width = 42


gameDisplay = pygame.display.set_mode((display_width, display_height))  # Sets height and width
pygame.display.set_caption('Racing')  # title
clock = pygame.time.Clock()  # Game clock


carImg = pygame.image.load('player.png')  # needs to be in the same folder as the .py


def friends_caught(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Caught" + str(count), True, black)
    gameDisplay.blit(text, (0, 30))


def things_dodged(count): # Sets up the scoring system
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged" + str(count), True, black)
    gameDisplay.blit(text, (0,0))


def things(thingx, thingy, thingw, thingh, color):  # Makes the block that comes down that the player needs to avoid
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def things_friendly(friendlyx, friendlyy, friendlyw, friendlyh, color):  # Makes the block that comes down that the player should catch
    pygame.draw.rect(gameDisplay, color, [friendlyx, friendlyy, friendlyw, friendlyh])


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):  # Creates the text box area
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):  # Defines the text box size, font type and location
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)
    game_loop()


def crash():
    message_display("You Crashed")

def caught(caught):
    caught +=1

def button(msg, x, y, w, h, ic, ac, action=None):
    # creates buttons to be used + adds interaction
    # Play game, quit game
    mouse = pygame.mouse.get_pos()  # looks for mouse position
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    # Add text to button
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w) / 2)), (y + (h / 2))
    gameDisplay.blit(textSurf, textRect)


def game_intro(): # Creates an Intro Screen for the game

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("BlockDodge", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Play", 150, 450, 100, 50, green, bright_green, "play")
        button("Quit", 550, 450, 100, 50, red, bright_red, "quit")

        pygame.display.update()
        clock.tick(15)


def game_loop():
    x = (display_width * 0.45)  # These lines dictate where the car will spawn
    y = (display_height * 0.8)

    x_change = 0
    y_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 3  # Speed of the block falling
    thing_width = 100
    thing_height = 100
    thing_count = 1
    dodged = 0

    friendly_startx = random.randrange(0, display_width)
    friendly_starty = -600
    friendly_speed = 3
    friendly_width = 50
    friendly_height = 50
    caught = 0


    gameExit = False  # Racing game, start the game as NOT crashed

    while not gameExit:

        # Below makes the left and right arrow work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Can't quit game without this!!
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:  # Makes sure that when you stop pressing the button, the car stops moving
                    x_change = 0
                    y_change = 0

        x += x_change
        y += y_change
        gameDisplay.fill(white)  # Makes background white

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed # adds 7 to the thing each time so it lowers each time
        car(x, y)  # Makes the car
        things_dodged(dodged)
        friends_caught(caught)

        things_friendly(friendly_startx, friendly_starty, friendly_width, friendly_height, red)  # Makes red box drop down - friendly box
        friendly_starty += friendly_speed

        if x > display_width - car_width or x < 0:  # Exits game at width border using the edge of the car
            crash()
            gameExit = True

        if thing_starty > display_height:
            thing_starty = 0 - thing_height  # immediately makes blocks show up randomely
            thing_startx = random.randrange(0, display_width)  # makes the block spawn in a new place each time
            dodged += 1
            thing_speed +=1  # increases speed of block each turn
            thing_width += (dodged * 1.2)  # increases the block width each turn
            thing_count += 1

        if friendly_starty > display_height:
            friendly_starty = 0 - friendly_height
            friendly_startx = random.randrange(0, display_width)




# The below basically makes it so that whatever part of the car touches the box, you crash.

        if y < thing_starty + thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                print('x crossover')
                crash()

        if y < friendly_starty + friendly_height:
            print ("y friend")

            if x > friendly_startx and x < friendly_startx + friendly_width or x + car_width > friendly_startx and x + car_width < friendly_startx + friendly_width:
                print ("x friend")



        pygame.display.update()  # Shows the above on the screen
        clock.tick(60)  # Frames per second

game_intro()
game_loop()
pygame.quit()
quit()