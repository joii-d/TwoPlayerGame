import pygame
import numpy as np
from GameBoard import GameBoard

########### DEFINES ##################
# board size in tiles
SCREEN_HEIGHT_IN_TILES = 8
SCREEN_WIDTH_IN_TILES = 8
BOARD_DIMENSIONS = (SCREEN_WIDTH_IN_TILES, SCREEN_HEIGHT_IN_TILES)

# board size in pixels
TILE_HEIGHT = 70
TILE_WIDTH = 70
MENU_HEIGHT = 50
SCREEN_HEIGHT = SCREEN_HEIGHT_IN_TILES * TILE_HEIGHT + MENU_HEIGHT
SCREEN_WIDTH = SCREEN_WIDTH_IN_TILES * TILE_WIDTH

# colors
TILE_COLOR = (240, 240, 240)
BORDER_COLOR = (200, 200, 200)
TOM_COLOR = (50,90,150)
JERRY_COLOR = (150,100,26)
TRAP_COLOR = "red"
CHEESE_COLOR = (230, 195, 60)

############### HELPER FUNCTIONS FOR DRAWING STUFF USING PYGAME #########################
def DrawTiles(screen):
    for x in range(0, SCREEN_WIDTH_IN_TILES):
        for y in range(0,SCREEN_HEIGHT_IN_TILES):
            tile = pygame.Rect(x*TILE_WIDTH, y*TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
            pygame.draw.rect(screen, BORDER_COLOR, tile, 2)

def DrawTraps(screen, traps):
    for (x,y) in traps:
        pygame.draw.circle(screen, TRAP_COLOR, (x*TILE_WIDTH + TILE_WIDTH / 2, y*TILE_HEIGHT + TILE_HEIGHT/2), TILE_HEIGHT/2 - 10)

def DrawCheese(screen, cheese):
    for (x,y) in cheese:
        pygame.draw.circle(screen, CHEESE_COLOR, (x*TILE_WIDTH + TILE_WIDTH / 2, y*TILE_HEIGHT + TILE_HEIGHT/2), TILE_HEIGHT/2 - 10)

def DrawTom(screen, tom_pos):
    x = tom_pos[0]
    y = tom_pos[1]
    pygame.draw.circle(screen, TOM_COLOR, (x*TILE_WIDTH + TILE_WIDTH / 2, y*TILE_HEIGHT + TILE_HEIGHT/2), TILE_HEIGHT/2 - 15)

def DrawJerry(screen, jerry_pos):
    x = jerry_pos[0]
    y = jerry_pos[1]
    pygame.draw.circle(screen, JERRY_COLOR, (x*TILE_WIDTH + TILE_WIDTH / 2, y*TILE_HEIGHT + TILE_HEIGHT/2), TILE_HEIGHT/2 - 15)

def DrawJerryPath(screen, path):
    for (x,y) in list(path)[1:-1]:
        pygame.draw.circle(screen, JERRY_COLOR, (x*TILE_WIDTH + TILE_WIDTH / 2, y*TILE_HEIGHT + TILE_HEIGHT/2), TILE_HEIGHT/8)

def DrawTomPath(screen, path):
    for (x,y) in list(path)[1:-1]:
        pygame.draw.circle(screen, TOM_COLOR, (x*TILE_WIDTH + TILE_WIDTH / 2, y*TILE_HEIGHT + TILE_HEIGHT/2), TILE_HEIGHT/8)

######################## MAIN ##########################################
if __name__=="__main__":
    # Pygame Setup
    pygame.init()
    pygame.display.set_caption("Tom and Jerry Sim")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 32)
    running = True


    # Board Setup
    NUM_CHEESE = 2  
    NUM_TRAPS = 2
    turn = "jerry"
    board = GameBoard(BOARD_DIMENSIONS)
    board.InitRandomCheeseAndTraps(NUM_CHEESE, NUM_TRAPS)


    # Game Loop
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    turn = "jerry"
                    board = GameBoard(BOARD_DIMENSIONS)
                    board.InitRandomCheeseAndTraps(NUM_CHEESE, NUM_TRAPS)
                if event.key == pygame.K_SPACE:

                    if turn == "jerry":
                        board.JerryDeterministicUpdate()
                        turn = "tom"
                    else:
                        board.TomDeterministicUpdate()
                        turn = "jerry"

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(TILE_COLOR)

        # Render the screen
        DrawTiles(screen)
        DrawTraps(screen, board.trapLocations)
        DrawCheese(screen, board.cheeseLocations)
        DrawTomPath(screen, board.tomCurrentPath)
        DrawJerryPath(screen, board.jerryCurrentPath)
        DrawJerry(screen, board.jerryPosition)
        DrawTom(screen, board.tomPosition)

        # draw bottom text
        turn_text = font.render('Next turn: ' + turn, True, "black")
        turn_text_rect = turn_text.get_rect()
        turn_text_rect.topleft = (5, SCREEN_HEIGHT_IN_TILES*TILE_HEIGHT + 5)
        screen.blit(turn_text, turn_text_rect)

        win_string = ""
        if board.tomWon: win_string = "Tom won"
        if board.jerryWon: win_string = "Jerry won"
        win_text = font.render(win_string, True, "black")
        win_text_rect = win_text.get_rect()
        win_text_rect.topright = (SCREEN_WIDTH - 5, SCREEN_HEIGHT_IN_TILES*TILE_HEIGHT + 5)
        screen.blit(win_text, win_text_rect)

        # flip bufferes to output to screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

