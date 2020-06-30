import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors Constants
black = (0, 0, 0)
white = (255, 255, 255)

# Set up screen of given size (600 pixels, 400 pixels)
screen = pygame.display.set_mode(size)

# Setup fonts art and size for user interface
mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
# Initialize board state
board = ttt.initial_state()
# Flag to keep tracking if it is ai's turn
ai_turn = False

while True:
    # Pygame uses event quere to manage event messaging
    # Get the next messaging through a loop, if event.type == QUIT then quite programm
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Set up screen background color
    screen.fill(black)

    # Let user choose a player.
    if user is None:

        '''
        Draw Title
        '''
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        # Get a Rect objects to store the rectangular coordinates of 
        # Title: position of the title' origin and width / height of the title
        titleRect = title.get_rect()
        # Centering Rect Object
        titleRect.center = ((width / 2), 50)
        # Draw title on the centered rect object
        screen.blit(title, titleRect)

        '''
        Draw button
        '''
        # Create Rech object to store the button: Rect(left, top, width, height)
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        # Positioning both rect objects at the center line
        playXRect.center = playXButton.center
        # Draw a rectangle with white background on screen
        pygame.draw.rect(screen, white, playXButton)
        # Draw "Play as X" on the rectangle
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        '''
        Check if button is clicked and select user
        '''
        # get a sequence of booleans representing the state of mouse
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            # get mouse cursor position (x,y) relative to the top-left corner
            mouse = pygame.mouse.get_pos()
            # test if mouse position is inside which button rechts
            if playXButton.collidepoint(mouse):
                # add delay of executing the program 
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:

        '''
        Draw game board
        '''
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        # loop through rows and columns to draw boxes
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                # draw white boxes with line thickness of 3pix
                pygame.draw.rect(screen, white, rect, 3)
                # fill every boxes with rect object
                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.player(board)

        '''
        Show title
        '''
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        '''
        Check for AI move
        '''
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                # Get the coordiate (i,j) of optimal action 
                move = ttt.minimax(board)
                # Update board state
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        '''
        Check for a user move
        '''
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            # loop through tiles[][] to check the active mouse position (i,j) 
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        # Update board state
                        board = ttt.result(board, (i, j))

        '''
        Game over
        '''
        if game_over:
            # Create a white background "Play again" button
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            # Check if user active the "Play again" button
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                # if activated, reset global variables
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    # Update display surface
    pygame.display.flip()
