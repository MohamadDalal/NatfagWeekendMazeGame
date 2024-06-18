import pygame
# Import the level you want to play.
#from Levels.level1 import self.currentLevel["levelList"], startPos, endPos
import json


class gameClass():

    def __init__(self, FPS=60, screenSize=(2160, 1280), levelPath = "Levels/level1.json"):
        self.FPS = FPS
        self.ScreenSize = screenSize
        self.gridSizeX, self.gridSizeY = 27, 16
        self.squareSizeX = self.ScreenSize[0] // self.gridSizeX
        self.squareSizeY = self.ScreenSize[1] // self.gridSizeY
        with open(levelPath, "r") as f:
            self.currentLevel = json.load(f)
        self.playerX = self.currentLevel["startPos"][0]
        self.playerY = self.currentLevel["startPos"][1]
        self.moveSuccessful = True
        self.levelWon = False
        self.framesTaken = 0
        # Putting the movement functions in a list makes it easier to turn around using the modulus operation on the index of the list
        # Just have to make sure that turning left makes the player move in the direction of the function in the next index (After Up comes Left etc.)
        self.moveDir = 0
        self.moveFunctions = (self.moveUp, self.moveLeft, self.moveDown, self.moveRight)

    # Function that uninitializes the pygame module
    def close(self, runBool):
        runBool = False
        pygame.display.quit()
        pygame.quit()
        exit()

    
    # Load a level script. Has a grid list with what each block is and a start and end position. Done only at the beginning
    def drawLevel(self, screen:pygame.Surface):
        for i in range(len(self.currentLevel["levelList"])):
            for j in range(len(self.currentLevel["levelList"][i])):
                # If block has a wall up draw it
                if self.currentLevel["levelList"][i][j][0] == "1":
                    pygame.draw.line(screen, (255,255,255), (j*self.squareSizeX, i*self.squareSizeY), ((j+1)*self.squareSizeX-1,i*self.squareSizeY))
                # If block has a wall right draw it
                if self.currentLevel["levelList"][i][j][1] == "1":
                    pygame.draw.line(screen, (255,255,255), ((j+1)*self.squareSizeX-1, i*self.squareSizeY), ((j+1)*self.squareSizeX-1,(i+1)*self.squareSizeY-1))
                # If block has a wall down draw it
                if self.currentLevel["levelList"][i][j][2] == "1":
                    pygame.draw.line(screen, (255,255,255), ((j+1)*self.squareSizeX-1, (i+1)*self.squareSizeY-1), (j*self.squareSizeX,(i+1)*self.squareSizeY-1))
                # If block has a wall left draw it
                if self.currentLevel["levelList"][i][j][3] == "1":
                    pygame.draw.line(screen, (255,255,255), (j*self.squareSizeX, i*self.squareSizeY), (j*self.squareSizeX,(i+1)*self.squareSizeY-1))
        # Draw start as white square and end as green square
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(self.currentLevel["startPos"][0]*self.squareSizeX, self.currentLevel["startPos"][1]*self.squareSizeY, self.squareSizeX, self.squareSizeY))
        pygame.draw.rect(screen, (0,255,0), pygame.Rect(self.currentLevel["endPos"][0]*self.squareSizeX, self.currentLevel["endPos"][1]*self.squareSizeY, self.squareSizeX, self.squareSizeY))

            
    # Draw the player as a circle. Done every frame.
    def drawPlayer(self, screen:pygame.Surface):
        rect = pygame.draw.circle(screen, (255,0,0), (self.playerX*self.squareSizeX+self.squareSizeX//2, self.playerY*self.squareSizeY+self.squareSizeY//2), min(self.squareSizeX,self.squareSizeY)//2-3)
        return rect

    # Movement functions. They are responsible for checking if there is a wall, and changing the player's position if there is no wall.
    def moveLeft(self):
        if (self.currentLevel["levelList"][self.playerY][self.playerX][3] == "0" and self.currentLevel["levelList"][self.playerY][self.playerX-1][1] == "0"):
            self.playerX -= 1
            return True
        else:
            return False

    def moveRight(self):
        if (self.currentLevel["levelList"][self.playerY][self.playerX][1] == "0" and self.currentLevel["levelList"][self.playerY][self.playerX+1][3] == "0"):
            self.playerX += 1
            return True
        else:
            return False
        
    def moveUp(self):
        if (self.currentLevel["levelList"][self.playerY][self.playerX][0] == "0" and self.currentLevel["levelList"][self.playerY-1][self.playerX][2] == "0"):
            self.playerY -= 1
            return True
        else:
            return False
        
    def moveDown(self):
        if (self.currentLevel["levelList"][self.playerY][self.playerX][2] == "0" and self.currentLevel["levelList"][self.playerY+1][self.playerX][0] == "0"):
            self.playerY += 1
            return True
        else:
            return False

    def turnLeft(self):
        self.moveDir = (self.moveDir + 1) % 4

    def turnAround(self):
        self.moveDir = (self.moveDir + 2) % 4

    def turnRight(self):
        self.moveDir = (self.moveDir + 3) % 4

    def movePlayer(self):
        self.moveSuccessful = self.moveFunctions[self.moveDir]()

    # The function with the simple algorithm to solve the game
    def mazeSolver(self):
        # Check if the current square is a straight path (Has left and right wall or up and down wall)
        isStraightPath = self.currentLevel["levelList"][self.playerY][self.playerX] == "0101" or self.currentLevel["levelList"][self.playerY][self.playerX] == "1010"
        # If it was not a straight path then turn left
        if not isStraightPath:
            self.turnLeft()
        # Try to move
        self.movePlayer()
        # If the player couldn't move then turn around
        if not self.moveSuccessful:
            # This is not optimal. If you turn around after turning left it will be as if you turned right
            # This is good however for when you reach a point where you cannot turn left, but you can turn right
            self.turnAround()

    # Function that setups the game, draws the game window, checks for movement and updates all variables.
    def playGame(self):
        # If we want to variables that are outside of functions we need to specify that they are global variables.
        # Otherwise doing levelWon = True will not change the variable we made outside the function
        # Search about global and local variables to learn more
        # Initialize pygame
        pygame.init()
        # A boolean that makes the while loop keep running. Loops stops if this goes false
        self.runBool = True
        # Pygame stuff. Read a pygame tutorial or the documentations for help
        self.screen = pygame.display.set_mode(self.ScreenSize)
        self.clock =  pygame.time.Clock()
        # Make the entire screen black (To remove anything already drawn there)
        self.screen.fill((0,0,0))
        # Run the level loading function to draw the level
        self.drawLevel(self.screen)
        # Create pygame rectangles for the FPS counter and the player circle (They specify where they are located in the windwo)
        fpsRect = pygame.Rect(0,0,20,20)
        playerRect = pygame.Rect(self.playerX*self.squareSizeX, self.playerY*self.squareSizeY, self.squareSizeX, self.squareSizeY)
        # Loop through the level screen until the runBool is set to false or the player beats the level
        while self.runBool and not self.levelWon:
            # Set FPS of the game and get events (for example button presses or keyboard presses. More info in pygame documentation)
            self.clock.tick(self.FPS)
            eventList = pygame.event.get()
            # Paint the FPS counter area black so we can draw a new FPS value. Otherwise they will be drawn on top of each other
            self.screen.fill((0,0,0), fpsRect)
            # Iterate through all events the happened since last frame. Do stuff for the ones you want
            for e in eventList:
                # If the X button to close the window is pressed then close the game
                if e.type == pygame.QUIT:
                    self.close(self.runBool)
                # If the escape key is pressed then close the game
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.close(self.runBool)

            # When the player moves we don't want the old circle to stay. Therefore, we draw over the square the player was last on.
            # If player was on start square we draw white, otherwise we draw black. If player reached goal then we set the levelWon boolean to True.
            if (self.playerX == self.currentLevel["startPos"][0] and self.playerY == self.currentLevel["startPos"][1]):
                self.screen.fill((255,255,255), playerRect)
                pass
            elif (self.playerX == self.currentLevel["endPos"][0] and self.playerY == self.currentLevel["endPos"][1]):
                self.levelWon = True
            else:
                self.screen.fill((0,0,0), playerRect)

            # Run the maze solving algorithm to move the player
            self.mazeSolver()

            # Get current game FPS to display on the window
            currentFPS = self.clock.get_fps()
            # Create the text to be displayed by specifying font, font size, text and color. Check documentation for more into
            FPS_Text = pygame.font.SysFont("Arial", 16).render("FPS: " + str(int(currentFPS)), False, (255,255,255))
            # Draw FPS counter and player
            fpsRect = self.screen.blit(FPS_Text, (0,0))
            playerRect = self.drawPlayer(self.screen)
            # Update window. This displays everything the we have drawn. Without it the drawn stuff won't be displayed
            pygame.display.flip()
            # Increase frame count
            self.framesTaken += 1
    
        # Fill entire screen with black to pringt new stuff
        self.screen.fill((0,0,0))

        # While loop to check if player closes game and display congratulations message
        while self.runBool:
            eventList = pygame.event.get()
            for e in eventList:
                if e.type == pygame.QUIT:
                    self.close(self.runBool)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.close(self.runBool)
            Win_Text = pygame.font.SysFont("Arial", 128).render("Congratulations!", False, (255,255,255))
            Speed_Text = pygame.font.SysFont("Arial", 128).render(f"Frames taken: {self.framesTaken}", False, (255,255,255))
            self.screen.blit(Win_Text,(600,523))
            self.screen.blit(Speed_Text,(560,675))
            pygame.display.flip()


if __name__=="__main__":
    gameObj = gameClass(FPS=60, levelPath="Levels/level1.json")
    gameObj.playGame()