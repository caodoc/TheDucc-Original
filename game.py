import pygame, os, random

pygame.init()
pygame.font.init()

#Window's Name
pygame.display.set_caption("The Ducc")

#Windows's Icon
WINDOWICON = pygame.image.load(os.path.join("assets", "duck.png"))

#Window's Resolution
WIDTH, HEIGHT = 1080,600
WINDOWDISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

#Window's Max FPS
FPS = 60

#Player Image
DUCK_RESOLUTION = 88 #Resolution of the image
DUCK_IMAGE = pygame.image.load(os.path.join("assets", "duck.png"))
DUCK = pygame.transform.scale(DUCK_IMAGE, (DUCK_RESOLUTION, DUCK_RESOLUTION))

#Object Image
FISH_RESOLUTION = 44
FISH_IMAGE = pygame.image.load(os.path.join("assets", "fish.png"))
FISH = pygame.transform.scale(FISH_IMAGE, (FISH_RESOLUTION, FISH_RESOLUTION))

#Speed
PLAYER_SPEED = 7

#Check if eats or not
EAT = pygame.USEREVENT

#Font
FONT = pygame.font.SysFont("JetBrains Mono", 15)
THE_END = pygame.font.SysFont("JetBrains Mono", 30)

#Colors
TEXT = (255, 255, 255)
BACKGROUND = (40, 44, 52)

#Begin of the game
def Start(player):
    WINDOWDISPLAY.fill(BACKGROUND) #Clear the sceen after previous movement
    WINDOWDISPLAY.blit(DUCK, (player.x, player.y)) #Set player image & position
    pygame.display.update() #Update it into the window

def Movement(pos, player):
    if pos[pygame.K_a] and player.x - PLAYER_SPEED > 0: #A for Left
        player.x -= PLAYER_SPEED

    if pos[pygame.K_d] and player.x + PLAYER_SPEED < WIDTH - DUCK_RESOLUTION: #D for Right
        player.x += PLAYER_SPEED

    if pos[pygame.K_w] and player.y - PLAYER_SPEED > 0: #W for Up
        player.y -= PLAYER_SPEED

    if pos[pygame.K_s] and player.y + PLAYER_SPEED < HEIGHT - DUCK_RESOLUTION: #S for Down
        player.y += PLAYER_SPEED

def Handle_Ontouch(player, fish):
    if player.colliderect(fish):
        pygame.event.post(pygame.event.Event(EAT)) #Send signal that the fish has been eaten

def Call(fish):
    WINDOWDISPLAY.blit(FISH, (fish.x, fish.y))
    pygame.display.update()

def Update(fish, FX, FY):
    fish.x = FX
    fish.y = FY

def EndGame(point):
    WINDOWDISPLAY.fill(BACKGROUND)
    Ending = "Congratulation! " + str(point) + " fish have been collected!"
    ENDING = THE_END.render(Ending, False, TEXT)
    WINDOWDISPLAY.blit(ENDING, (0, 0))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    ToggleGame = True
    Clock = pygame.time.Clock()

    #Summon Fish & Duck
    Player = pygame.Rect(0, 0, DUCK_RESOLUTION, DUCK_RESOLUTION)
    Fish = pygame.Rect(500, 500, FISH_RESOLUTION, FISH_RESOLUTION)

    #Scores
    Score = 0

    #Summon
    Summon = True

    #Time
    StartTicks = 15000 #1000 ticks = 1 second

    #Random Duck's Position
    FX = random.randint(0 + FISH_RESOLUTION, WIDTH - FISH_RESOLUTION)
    FY = random.randint(0 + FISH_RESOLUTION, HEIGHT - FISH_RESOLUTION)

    pygame.display.set_icon(WINDOWICON) #Set Window's Icon
    WINDOWDISPLAY.fill(BACKGROUND) #Set background color
    pygame.display.update() #Update background color

    while ToggleGame:
        Clock.tick(FPS) #Control FPS

        #Summon our player
        Start(Player)

        # Check what character on keyboard was pressed
        Key_Toggle = pygame.key.get_pressed()
        Movement(Key_Toggle, Player)

        #Random after being eaten
        if Summon:
            FX = random.randint(0 + FISH_RESOLUTION, WIDTH - FISH_RESOLUTION)
            FY = random.randint(0 + FISH_RESOLUTION, HEIGHT - FISH_RESOLUTION)
            Summon = False

        #Update Fish's Position
        Call(Fish)
        Update(Fish, FX, FY)

        #Check if the duck eats the fish
        Handle_Ontouch(Player, Fish)

        #Update Time
        CountDown = (StartTicks - pygame.time.get_ticks()) / 1000

        #Update Texts
        Time_text = "Time Left: " + str(CountDown)
        Score_text = "Fishes Count: " + str(Score)
        TIME_TEXT = FONT.render(Time_text, False, TEXT)
        SCORE_TEXT = FONT.render(Score_text, False, TEXT)

        #Show Texts
        WINDOWDISPLAY.blit(TIME_TEXT, (0, 0))
        WINDOWDISPLAY.blit(SCORE_TEXT, (0, 20))
        pygame.display.update()

        for event in pygame.event.get():
            #Attention: Without this condition code, your game will not close after you click close window.
            if event.type == pygame.QUIT:
                ToggleGame = False

            #Calculate Scores
            if event.type == EAT:
                Score += 1

                Summon = True

                #Enable this will print the score into terminal window
                #Use for checking if anything is working normal
                #print(Score)

        #End the game if time runs out
        if CountDown <= 0:
            EndGame(Score)
            break

    pygame.quit()

#Run the game
if __name__ == "__main__":
    main()