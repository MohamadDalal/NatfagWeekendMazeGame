import pygame
import json
from tkinter.filedialog import asksaveasfilename, askopenfilename

class levelMakerClass():

    def __init__(self, screen:pygame.Surface, clock:pygame.time.Clock, FPS=60):
        self.screen = screen
        self.clock = clock
        self.screenSize = screen.get_size()
        self.menuFontSize = self.screenSize[0]*8//135
        self.menuCursorPos = 0
        # Number of squares to split the window
        self.gridSizeX, self.gridSizeY = 27, 16
        # Size of each square
        self.squareSizeX = self.screenSize[0] // self.gridSizeX
        self.squareSizeY = self.screenSize[1] // self.gridSizeY
        # Position of the player. Starts at the level's start position, changed when moving
        self.playerX, self.playerY = 0,0
        self.runBool = True
        self.currentMenu = self.startMenu
        with open("Levels/level1.json", "r") as f:
            self.currentLevel = json.load(f)
        self.selectedBlock = "0000"

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
        rect = pygame.draw.circle(screen, (255,255,0), (self.playerX*self.squareSizeX+self.squareSizeX//2, self.playerY*self.squareSizeY+self.squareSizeY//2), min(self.squareSizeX,self.squareSizeY)//2-min(self.squareSizeX,self.squareSizeY)//4)
        return rect

    def startNewLevel(self):
        levelGrid = []
        for i in range(self.gridSizeY):
            levelGrid.append([])
            for _ in range(self.gridSizeX):
                levelGrid[i].append("0000")
        self.currentLevel["levelList"] = levelGrid
        self.currentLevel["startPos"] = [self.gridSizeX//2, self.gridSizeY-1]
        self.currentLevel["endPos"] = [self.gridSizeX//2, 0]
        self.currentMenu = self.levelEditor



    def loadLevel(self):
        path = askopenfilename()
        print(path)
        try:
            with open(path, "r") as f:
                self.currentLevel = json.load(f)
                retVal = True
        except Exception as e:
            print(e)
            retVal =  False
        finally:
            pygame.event.clear()
            return retVal

    def saveLevel(self):
        path = asksaveasfilename()
        print(path)
        try:
            if path[-5:] != ".json":
                path = path + ".json"
            with open(path, "w") as f:
                json.dump(self.currentLevel, f)
                retVal =  True
        except Exception as e:
            print(e)
            retVal = False
        finally:
            pygame.event.clear()
            return retVal

    def startMenu(self, eventList):
        screen.fill((0,0,0))
        # Iterate through all events the happened since last frame. Do stuff for the ones you want
        for e in eventList:
            if e.type == pygame.KEYDOWN:
                print(pygame.key.name(e.key))
                if e.key == pygame.K_UP:
                    self.menuCursorPos = (self.menuCursorPos-1)%3
                elif e.key == pygame.K_DOWN:
                    self.menuCursorPos = (self.menuCursorPos+1)%3
                elif e.key == pygame.K_RETURN:
                    if self.menuCursorPos == 0: self.startNewLevel()
                    elif self.menuCursorPos == 1:
                        if self.loadLevel():
                            self.currentMenu = self.levelEditor
                    elif self.menuCursorPos == 2: self.close()
        menu_Text1 = pygame.font.SysFont("Arial", self.menuFontSize).render("New Level", False, (255,255,255))
        menu_Text2 = pygame.font.SysFont("Arial", self.menuFontSize).render("Load Level", False, (255,255,255))
        menu_Text3 = pygame.font.SysFont("Arial", self.menuFontSize).render("Exit Editor", False, (255,255,255))
        menu_Cursor = pygame.font.SysFont("Arial", self.menuFontSize).render("->", False, (255,255,255))
        self.screen.blit(menu_Text1,(self.screenSize[0]//3,self.screenSize[1]*2//7))
        self.screen.blit(menu_Text2,(self.screenSize[0]//3,self.screenSize[1]*3//7))
        self.screen.blit(menu_Text3,(self.screenSize[0]//3,self.screenSize[1]*4//7))
        self.screen.blit(menu_Cursor,(self.screenSize[0]//4,self.screenSize[1]*(2+self.menuCursorPos)//7))

    def helpMenu(self, eventList):
        screen.fill((0,0,0))
        # Iterate through all events the happened since last frame. Do stuff for the ones you want
        for e in eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.currentMenu = self.pauseMenu
        helpText = [[["Arrow keys:", "Move"],
                     ["1:", "Toggle top wall"],
                     ["2:", "Toggle right wall"],
                     ["3:", "Toggle bottom wall"],
                     ["4:", "Toggle left wall"]
                     ],
                    [["Q:", "Set start square"],
                     ["E:", "Set finish square"],
                     ["Enter:", "Set block"],
                     ["Delete:", "Remove block"],
                     ["Escape:", "Pause editor"]
                     ]]
        vertLen = max([len(i) for i in helpText])
        for i in range(len(helpText)):
            for j in range(len(helpText[i])):
                temp_Text = pygame.font.SysFont("Arial", self.menuFontSize*3//4).render(f"{helpText[i][j][0]} {helpText[i][j][1]}", False, (255,255,255))
                self.screen.blit(temp_Text, (self.screenSize[0]*(9*i+1)//20, self.screenSize[1]*(j+1)//(vertLen+2)))

        #menu_Text1 = pygame.font.SysFont("Arial", self.menuFontSize*3//4).render("Save Level", False, (255,255,255))
        #self.screen.blit(menu_Text1,(self.screenSize[0]//3,self.screenSize[1]*2//5))

    def pauseMenu(self, eventList):
        screen.fill((0,0,0))
        # Iterate through all events the happened since last frame. Do stuff for the ones you want
        for e in eventList:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.menuCursorPos = (self.menuCursorPos-1)%3
                elif e.key == pygame.K_DOWN:
                    self.menuCursorPos = (self.menuCursorPos+1)%3
                elif e.key == pygame.K_RETURN:
                    if self.menuCursorPos == 0: self.saveLevel()
                    elif self.menuCursorPos == 1: self.currentMenu = self.helpMenu
                    elif self.menuCursorPos == 2: self.currentMenu = self.startMenu; self.menuCursorPos = 0
                elif e.key == pygame.K_ESCAPE:
                    self.currentMenu = self.levelEditor
        menu_Text1 = pygame.font.SysFont("Arial", self.menuFontSize).render("Save Level", False, (255,255,255))
        menu_Text2 = pygame.font.SysFont("Arial", self.menuFontSize).render("Display Help", False, (255,255,255))
        menu_Text3 = pygame.font.SysFont("Arial", self.menuFontSize).render("Exit Editor", False, (255,255,255))
        menu_Cursor = pygame.font.SysFont("Arial", self.menuFontSize).render("->", False, (255,255,255))
        self.screen.blit(menu_Text1,(self.screenSize[0]//3,self.screenSize[1]*2//7))
        self.screen.blit(menu_Text2,(self.screenSize[0]//3,self.screenSize[1]*3//7))
        self.screen.blit(menu_Text3,(self.screenSize[0]//3,self.screenSize[1]*4//7))
        self.screen.blit(menu_Cursor,(self.screenSize[0]//4,self.screenSize[1]*(2+self.menuCursorPos)//7))

    def levelEditor(self, eventList):
        screen.fill((0,0,0))
        self.drawLevel(self.screen)
        # Iterate through all events the happened since last frame. Do stuff for the ones you want
        for e in eventList:
            if e.type == pygame.KEYDOWN:
                if e.mod == pygame.KMOD_NONE:
                    print(pygame.key.name(e.key))
                    if e.key == pygame.K_UP:
                        self.playerY = (self.playerY-1)%self.gridSizeY
                    if e.key == pygame.K_DOWN:
                        self.playerY = (self.playerY+1)%self.gridSizeY
                    if e.key == pygame.K_LEFT:
                        self.playerX = (self.playerX-1)%self.gridSizeX
                    if e.key == pygame.K_RIGHT:
                        self.playerX = (self.playerX+1)%self.gridSizeX
                    if e.key == pygame.K_RETURN:
                        self.currentLevel["levelList"][self.playerY][self.playerX] = self.selectedBlock
                    if e.key == pygame.K_1 or e.key == pygame.K_KP_1:
                        self.selectedBlock = str((int(self.selectedBlock[0])+1)%2) + self.selectedBlock[1:]
                    if e.key == pygame.K_2 or e.key == pygame.K_KP_2:
                        self.selectedBlock = self.selectedBlock[0] + str((int(self.selectedBlock[1])+1)%2) + self.selectedBlock[2:]
                    if e.key == pygame.K_3 or e.key == pygame.K_KP_3:
                        self.selectedBlock = self.selectedBlock[:2] + str((int(self.selectedBlock[2])+1)%2) + self.selectedBlock[3]
                    if e.key == pygame.K_4 or e.key == pygame.K_KP_4:
                        self.selectedBlock = self.selectedBlock[:3] + str((int(self.selectedBlock[3])+1)%2)
                    if e.key == pygame.K_q:
                        self.currentLevel["startPos"] = [self.playerX, self.playerY]
                    if e.key == pygame.K_e:
                        self.currentLevel["endPos"] = [self.playerX, self.playerY]
                    if e.key == pygame.K_DELETE:
                        self.currentLevel["levelList"][self.playerY][self.playerX] = "0000"
                    if e.key == pygame.K_ESCAPE:
                        self.menuCursorPos = 0
                        self.currentMenu = self.pauseMenu
                elif e.mod & pygame.KMOD_LCTRL:
                    if e.key == pygame.K_s:
                        self.saveLevel()

                #print(self.selectedBlock)
        
        # When the player moves we don't want the old circle to stay. Therefore, we draw over the square the player was last on.
        # If player was on start square we draw white, otherwise we draw black. If player reached goal then we set the levelWon boolean to True.
        if (self.playerX == self.currentLevel["startPos"][0] and self.playerY == self.currentLevel["startPos"][1]):
            self.screen.fill((255,255,255), pygame.Rect(self.playerX*self.squareSizeX, self.playerY*self.squareSizeY, self.squareSizeX, self.squareSizeY))
            pass
        elif (self.playerX == self.currentLevel["endPos"][0] and self.playerY == self.currentLevel["endPos"][1]):
            self.screen.fill((0,255,0), pygame.Rect(self.playerX*self.squareSizeX, self.playerY*self.squareSizeY, self.squareSizeX, self.squareSizeY))
        else:
            self.screen.fill((0,0,0), self.screen.fill((255,255,255), pygame.Rect(self.playerX*self.squareSizeX, self.playerY*self.squareSizeY, self.squareSizeX, self.squareSizeY)))
        
        #pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(self.playerX*self.squareSizeX, self.playerY*self.squareSizeY, self.squareSizeX, self.squareSizeY))
        # If block has a wall up draw it
        if self.selectedBlock[0] == "1":
            pygame.draw.line(screen, (255,255,0), (self.playerX*self.squareSizeX, self.playerY*self.squareSizeY), ((self.playerX+1)*self.squareSizeX-1,self.playerY*self.squareSizeY), 3)
        # If block has a wall right draw it
        if self.selectedBlock[1] == "1":
            pygame.draw.line(screen, (255,255,0), ((self.playerX+1)*self.squareSizeX-1, self.playerY*self.squareSizeY), ((self.playerX+1)*self.squareSizeX-1,(self.playerY+1)*self.squareSizeY-1), 3)
        # If block has a wall down draw it
        if self.selectedBlock[2] == "1":
            pygame.draw.line(screen, (255,255,0), ((self.playerX+1)*self.squareSizeX-1, (self.playerY+1)*self.squareSizeY-1), (self.playerX*self.squareSizeX,(self.playerY+1)*self.squareSizeY-1), 3)
        # If block has a wall left draw it
        if self.selectedBlock[3] == "1":
            pygame.draw.line(screen, (255,255,0), (self.playerX*self.squareSizeX, self.playerY*self.squareSizeY), (self.playerX*self.squareSizeX,(self.playerY+1)*self.squareSizeY-1), 3)
        
        playerRect = self.drawPlayer(self.screen)

        
    # Function that uninitializes the pygame module
    def close(runBool):
        pygame.display.quit()
        pygame.quit()
        exit()
    
    def runLevelEditor(self, eventList):
        self.currentMenu(eventList)

    


# Function that uninitializes the pygame module
def close(runBool):
    runBool = False
    pygame.display.quit()
    pygame.quit()
    exit()

if __name__ == "__main__":
    #ScreenSize = 2160, 1280
    ScreenSize = 1280, 720
    FPS = 60
    # Initialize pygame
    pygame.init()
    # A boolean that makes the while loop keep running. Loops stops if this goes false
    runBool = True
    # Pygame stuff. Read a pygame tutorial or the documentations for help
    screen = pygame.display.set_mode(ScreenSize)
    clock =  pygame.time.Clock()
    pygame.key.set_repeat(300, 100)
    # Make the entire screen black (To remove anything already drawn there)
    screen.fill((0,0,0))
    # Create pygame rectangles for the FPS counter and the player circle (They specify where they are located in the windwo)
    fpsRect = pygame.Rect(0,0,20,20)
    
    levelMakerObj = levelMakerClass(screen, clock)

    while runBool:
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

        levelMakerObj.runLevelEditor(eventList)

        # Get current game FPS to display on the window
        currentFPS = clock.get_fps()
        # Create the text to be displayed by specifying font, font size, text and color. Check documentation for more into
        FPS_Text = pygame.font.SysFont("Arial", 16).render("FPS: " + str(int(currentFPS)), False, (255,255,255))
        # Draw FPS counter and player
        fpsRect = screen.blit(FPS_Text, (0,0))
        # Update window. This displays everything the we have drawn. Without it the drawn stuff won't be displayed
        pygame.display.flip()