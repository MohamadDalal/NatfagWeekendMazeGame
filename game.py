import pygame
# Import the level you want to play.
from Levels.level1 import levelList, startPos, endPos

# Function that uninitializes the pygame module
def close(runBool):
    runBool = False
    pygame.display.quit()
    pygame.quit()
    exit()

# Frames Per Second for the game
FPS = 20
# Screen size to display the game. Make smaller if the window is too big
ScreenSize = 2160, 1280
# Number of squares to split the window
gridSizeX, gridSizeY = 27, 16
# Size of each square
squareSizeX, squareSizeY = ScreenSize[0] // gridSizeX, ScreenSize[1] // gridSizeY
# Position of the player. Starts at the level's start position, changed when moving
playerX, playerY = startPos[0], startPos[1]
# True if the player successfully moved last time it tried
moveSuccessful = True
# Becomes true when we reach the goal. Used to switch to win screen
levelWon = False
# Count number of frames taken to solve
framesTaken = 0

# Load a level script. Has a grid list with what each block is and a start and end position. Done only at the beginning
def loadLevel(screen:pygame.Surface):
    for i in range(len(levelList)):
        for j in range(len(levelList[i])):
            # If block has a wall up draw it
            if levelList[i][j][0] == "1":
                pygame.draw.line(screen, (255,255,255), (j*squareSizeX, i*squareSizeY), ((j+1)*squareSizeX-1,i*squareSizeY))
            # If block has a wall right draw it
            if levelList[i][j][1] == "1":
                pygame.draw.line(screen, (255,255,255), ((j+1)*squareSizeX-1, i*squareSizeY), ((j+1)*squareSizeX-1,(i+1)*squareSizeY-1))
            # If block has a wall down draw it
            if levelList[i][j][2] == "1":
                pygame.draw.line(screen, (255,255,255), ((j+1)*squareSizeX-1, (i+1)*squareSizeY-1), (j*squareSizeX,(i+1)*squareSizeY-1))
            # If block has a wall left draw it
            if levelList[i][j][3] == "1":
                pygame.draw.line(screen, (255,255,255), (j*squareSizeX, i*squareSizeY), (j*squareSizeX,(i+1)*squareSizeY-1))
    # Draw start as white square and end as green square
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(startPos[0]*squareSizeX, startPos[1]*squareSizeY, squareSizeX, squareSizeY))
    pygame.draw.rect(screen, (0,255,0), pygame.Rect(endPos[0]*squareSizeX, endPos[1]*squareSizeY, squareSizeX, squareSizeY))
            
# Draw the player as a circle. Done every frame.
def drawPlayer(screen:pygame.Surface):
    rect = pygame.draw.circle(screen, (255,0,0), (playerX*squareSizeX+squareSizeX//2, playerY*squareSizeY+squareSizeY//2), min(squareSizeX,squareSizeY)//2-3)
    return rect

# Movement functions. They are responsible for checking if there is a wall, and changing the player's position if there is no wall.
def moveLeft():
    global playerX, playerY
    if (levelList[playerY][playerX][3] == "0" and levelList[playerY][playerX-1][1] == "0"):
        playerX -= 1
        return True
    else:
        return False

def moveRight():
    global playerX, playerY
    if (levelList[playerY][playerX][1] == "0" and levelList[playerY][playerX+1][3] == "0"):
        playerX += 1
        return True
    else:
        return False
    
def moveUp():
    global playerX, playerY
    if (levelList[playerY][playerX][0] == "0" and levelList[playerY-1][playerX][2] == "0"):
        playerY -= 1
        return True
    else:
        return False
    
def moveDown():
    global playerX, playerY
    if (levelList[playerY][playerX][2] == "0" and levelList[playerY+1][playerX][0] == "0"):
        playerY += 1
        return True
    else:
        return False
    
# Putting the movement functions in a list makes it easier to turn around using the modulus operation on the index of the list
# Just have to make sure that turning left makes the player move in the direction of the function in the next index (After Up comes Left etc.)
moveDir = 0
moveFunctions = (moveUp, moveLeft, moveDown, moveRight)

def turnLeft():
    global moveDir
    moveDir = (moveDir + 1) % 4

def turnAround():
    global moveDir
    moveDir = (moveDir + 2) % 4

def turnRight():
    global moveDir
    moveDir = (moveDir + 3) % 4

def movePlayer():
    global moveSuccessful
    moveSuccessful = moveFunctions[moveDir]()

# The function with the simple algorithm to solve the game
def mazeSolver():
    # Check if the current square is a straight path (Has left and right wall or up and down wall)
    isStraightPath = levelList[playerY][playerX] == "0101" or levelList[playerY][playerX] == "1010"
    # If it was not a straight path then turn left
    if not isStraightPath:
        turnLeft()
    # Try to move
    movePlayer()
    # If the player couldn't move then turn around
    if not moveSuccessful:
        # This is not optimal. If you turn around after turning left it will be as if you turned right
        # This is good however for when you reach a point where you cannot turn left, but you can turn right
        turnAround()

# Function that setups the game, draws the game window, checks for movement and updates all variables.
def playGame():
    # If we want to variables that are outside of functions we need to specify that they are global variables.
    # Otherwise doing levelWon = True will not change the variable we made outside the function
    # Search about global and local variables to learn more
    global moveSuccessful, levelWon, framesTaken
    # Initialize pygame
    pygame.init()
    # A boolean that makes the while loop keep running. Loops stops if this goes false
    runBool = True
    # Pygame stuff. Read a pygame tutorial or the documentations for help
    screen = pygame.display.set_mode(ScreenSize)
    clock =  pygame.time.Clock()
    # Make the entire screen black (To remove anything already drawn there)
    screen.fill((0,0,0))
    # Run the level loading function to draw the level
    loadLevel(screen)
    # Create pygame rectangles for the FPS counter and the player circle (They specify where they are located in the windwo)
    fpsRect = pygame.Rect(0,0,20,20)
    playerRect = pygame.Rect(playerX*squareSizeX, playerY*squareSizeY, squareSizeX, squareSizeY)
    # Loop through the level screen until the runBool is set to false or the player beats the level
    while runBool and not levelWon:
        # Set FPS of the game and get events (for example button presses or keyboard presses. More info in pygame documentation)
        clock.tick(FPS)
        eventList = pygame.event.get()
        # Paint the FPS counter area black so we can draw a new FPS value. Otherwise they will be drawn on top of each other
        screen.fill((0,0,0), fpsRect)
        # Iterate through all events the happened since last frame. Do stuff for the ones you want
        for e in eventList:
            # If the X button to close the window is pressed then close the game
            if e.type == pygame.QUIT:
                close(runBool)
            # If the escape key is pressed then close the game
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    close(runBool)

        # When the player moves we don't want the old circle to stay. Therefore, we draw over the square the player was last on.
        # If player was on start square we draw white, otherwise we draw black. If player reached goal then we set the levelWon boolean to True.
        if (playerX == startPos[0] and playerY == startPos[1]):
            screen.fill((255,255,255), playerRect)
            pass
        elif (playerX == endPos[0] and playerY == endPos[1]):
            levelWon = True
        else:
            screen.fill((0,0,0), playerRect)

        # Run the maze solving algorithm to move the player
        mazeSolver()

        # Get current game FPS to display on the window
        currentFPS = clock.get_fps()
        # Create the text to be displayed by specifying font, font size, text and color. Check documentation for more into
        FPS_Text = pygame.font.SysFont("Arial", 16).render("FPS: " + str(int(currentFPS)), False, (255,255,255))
        # Draw FPS counter and player
        fpsRect = screen.blit(FPS_Text, (0,0))
        playerRect = drawPlayer(screen)
        # Update window. This displays everything the we have drawn. Without it the drawn stuff won't be displayed
        pygame.display.flip()
        # Increase frame count
        framesTaken += 1
 
    # Fill entire screen with black to pringt new stuff
    screen.fill((0,0,0))

    # While loop to check if player closes game and display congratulations message
    while runBool:
        eventList = pygame.event.get()
        for e in eventList:
            if e.type == pygame.QUIT:
                close(runBool)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    close(runBool)
        Win_Text = pygame.font.SysFont("Arial", 128).render("Congratulations!", False, (255,255,255))
        Speed_Text = pygame.font.SysFont("Arial", 128).render(f"Frames taken: {framesTaken}", False, (255,255,255))
        screen.blit(Win_Text,(600,523))
        screen.blit(Speed_Text,(560,675))
        pygame.display.flip()


if __name__=="__main__":
    playGame()