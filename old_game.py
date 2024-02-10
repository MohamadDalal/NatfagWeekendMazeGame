import pygame
from Levels.level1 import levelList, startPos, endPos

# This script allows keyboard controls, but is not adjusted for changing window size. Also not commented

# Function that uninitializes the pygame module
def close():
    runBool = False
    pygame.display.quit()
    pygame.quit()
    exit()

FPS = 60
ScreenSize = 1080, 640
gridSizeX, gridSizeY = 27, 16
playerX, playerY = startPos[0], startPos[1]
moveSuccessful = True
levelWon = False

def loadLevel(screen:pygame.Surface):
    for i in range(len(levelList)):
        for j in range(len(levelList[i])):
            if levelList[i][j][0] == "1":
                pygame.draw.line(screen, (255,255,255), (j*40, i*40), ((j+1)*40-1,i*40))
            if levelList[i][j][1] == "1":
                pygame.draw.line(screen, (255,255,255), ((j+1)*40-1, i*40), ((j+1)*40-1,(i+1)*40-1))
            if levelList[i][j][2] == "1":
                pygame.draw.line(screen, (255,255,255), ((j+1)*40-1, (i+1)*40-1), (j*40,(i+1)*40-1))
            if levelList[i][j][3] == "1":
                pygame.draw.line(screen, (255,255,255), (j*40, i*40), (j*40,(i+1)*40-1))
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(startPos[0]*40, startPos[1]*40, 40, 40))
    pygame.draw.rect(screen, (0,255,0), pygame.Rect(endPos[0]*40, endPos[1]*40, 40, 40))
            

def drawPlayer(screen:pygame.Surface):
    #for i in range(1,gridSizeX-1):
    #    for j in range(1,gridSizeY-1):
    #        pygame.draw.rect(screen, (255,255,255), pygame.Rect(40*i, 40*j, 40, 40), width=1)
    rect = pygame.draw.circle(screen, (255,0,0), (playerX*40+20, playerY*40+20), 17)
    return rect

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

def playGame():
    global moveSuccessful, levelWon
    pygame.init()
    runBool = True
    screen = pygame.display.set_mode(ScreenSize)
    clock =  pygame.time.Clock()
    screen.fill((0,0,0))
    loadLevel(screen)
    fpsRect = pygame.Rect(0,0,30,30)
    playerRect = pygame.Rect(0,0,30,30)

    while runBool and not levelWon:
        clock.tick(FPS)
        eventList = pygame.event.get()
        #keyPressList = pygame.key.get_pressed()
        screen.fill((0,0,0), fpsRect)

        for e in eventList:
            if e.type == pygame.QUIT:
                close()
            if e.type == pygame.KEYDOWN:
                if (playerX == startPos[0] and playerY == startPos[1]):
                    screen.fill((255,255,255), playerRect)
                elif (playerX == endPos[0] and playerY == endPos[1]):
                    screen.fill((0,255,0), playerRect)
                else:
                    screen.fill((0,0,0), playerRect)
                if e.key == pygame.K_LEFT:
                    moveSuccessful = moveLeft()
                elif e.key == pygame.K_RIGHT:
                    moveSuccessful = moveRight()
                elif e.key == pygame.K_UP:
                    moveSuccessful = moveUp()
                elif e.key == pygame.K_DOWN:
                    moveSuccessful = moveDown()
                elif e.key == pygame.K_ESCAPE:
                    close()
                if (playerX == endPos[0] and playerY == endPos[1]):
                    levelWon = True
        currentFPS = clock.get_fps()
        FPS_Text = pygame.font.SysFont("Arial", 16).render("FPS: " + str(int(currentFPS)), False, (255,255,255))
        fpsRect = screen.blit(FPS_Text, (0,0))
        playerRect = drawPlayer(screen)
        pygame.display.flip()

    screen.fill((0,0,0))

    while runBool:
        eventList = pygame.event.get()
        for e in eventList:
            if e.type == pygame.QUIT:
                close()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    close()
        Win_Text = pygame.font.SysFont("Arial", 64).render("Congratulations!", False, (255,255,255))
        screen.blit(Win_Text,(300,300))
        pygame.display.flip()

if __name__=="__main__":
    playGame()