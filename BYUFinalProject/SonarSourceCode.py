#sonar game - find the 3 treasures

import random
import sys
from SonarModule import SonarBoard

game = SonarBoard()

# Where the player is asked if they want to see instructions for the game

print('S O N A R - 2 player edition!')
print()
print('Would you like to view the instructions? (y/n)')
if input().lower().startswith('y'):
    game.showInstructions()


numberOfPlayers = 2
names = []

# This loop asks for the player name twice
for i in range(int(numberOfPlayers)):
    print("Enter the next player's name")
    next_name = input()
    names.append(next_name)
    print("Players:" + str(names))

Player1 = str(names[0])
Player2 = str(names[1])
randomPlayer = random.choice(names)
lastPlayer = randomPlayer


while True:
    # Game setup
    print("How many sonar devices would you like?? (Easy = 50, Medium = 30 , Hard = 20, Expert = 10)")
    gameMode = input()
    sonarDevices = int(gameMode)
    theBoard = game.getNewBoard()
    theChests = game.getRandomChests(3)
    game.drawBoard(theBoard)
    previousMoves = []

    # Move counter to help determine which player's move it is
    turn1 = 0
    turn2 = 0

    while sonarDevices > int(0):
        # Determines which player's turn it is
        if turn1 == 0 and turn2 == 0:
            print('%s  has %s sonar device(s) left. %s treasure chest(s) remaining.' % (Player1, sonarDevices, len(theChests)))
            turn1 += 1
        else:
            if turn1 > turn2:
                print('%s  has %s sonar device(s) left. %s treasure chest(s) remaining.' % (Player2, sonarDevices, len(theChests)))
                turn2 += 1
            else:
                print('%s  has %s sonar device(s) left. %s treasure chest(s) remaining.' % (Player1, sonarDevices, len(theChests)))
                turn1 += 1
        # Show sonar device and chest statuses
        x, y = game.enterPlayerMove(previousMoves)
        previousMoves.append([x, y]) # We must track all moves so that sonar devices can be updated.

        moveResult = game.makeMove(theBoard, theChests, x, y)
        if moveResult == False:
            continue
        else:
            if moveResult == 'You have found a sunken treasure chest!':
                # Update all the sonar devices currently on the map.
                for x, y in previousMoves:
                    game.makeMove(game.theBoard, theChests, x, y)
            game.drawBoard(theBoard)
            print(moveResult)

        if len(theChests) == 0:
            print('You have found all the sunken treasure chests! Congratulations and good game!')
            break

        sonarDevices -= 1

    # In the senario that the players lose (run out of sonar devices)
    if sonarDevices == 0:
        print('We\'ve run out of sonar devices! Now we have to turn the ship around and head')
        print('for home with treasure chests still out there! Game over.')
        print(' The remaining chests were here:')
        for x, y in theChests:
            print(' %s, %s' % (x, y))

    #Asks player if they want to replay
    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        sys.exit()
