import asyncio    
import pygame     
import os         

pygame.init()

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # WIN = WINDOW 
pygame.display.set_caption("Blob the jelly!")  

WHITE = (255,255,255)   # RGB waarden
BLACK = (0,0,0)
YELLOW = (255,255,0)
RED = (255,0,0)
PURPLE = (142,56,142)
INDIGO = (75,0,130)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 7, HEIGHT) # x en y positie , width en height
LEFT_BORDER = pygame.Rect(0, 0, 7, HEIGHT)
RIGHT_BORDER = pygame.Rect(WIDTH - 7, 0, 7, HEIGHT)
UPPER_BORDER = pygame.Rect(0, 0, WIDTH, 7)
LOWER_BORDER = pygame.Rect(0, HEIGHT - 7, WIDTH, 7)

#BULLET_HIT_SOUND = pygame.mixer.Sound('Asset/Grenade+1.mp3') 
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('aptos', 45) # lettertype en grootte
WINNER_FONT = pygame.font.SysFont('TradeGothicInline', 130)

FPS = 60    
VEL = 5     # velocity/snelheid wordt gebruikt voor snelheid waarmee pionnen kunnen bewegen
BULLET_VEL = 7    
MAX_BULLETS = 5
IMG_WIDTH, IMG_HEIGHT = 55, 45 

RED_HIT = pygame.USEREVENT + 1 
YELLOW_HIT = pygame.USEREVENT + 2

YELLOW_SMILEY = pygame.image.load(
    os.path.join('Assets', 'yellowjelly.png'))
YELLOW_SMILEY = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SMILEY, (IMG_WIDTH, IMG_HEIGHT)), 360)

RED_SMILEY = pygame.image.load(
    os.path.join('Assets', 'purplejelly.png'))
RED_SMILEY = pygame.transform.rotate(pygame.transform.scale(
    RED_SMILEY, (IMG_WIDTH, IMG_HEIGHT)), 360)

BACKGROUND = pygame.transform.scale(pygame.image.load(                   # achtergrond foto opgeschaald naar window
    os.path.join('Assets', 'skyy.png')), (WIDTH, HEIGHT))                # vergeet niet in de draw window functie het op te roepen

def draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, red_health):
    WIN.fill((WHITE))                            
    WIN.blit(BACKGROUND, (0,0))                 
    pygame.draw.rect(WIN, INDIGO, BORDER)
    pygame.draw.rect(WIN, INDIGO, LEFT_BORDER)
    pygame.draw.rect(WIN, INDIGO, RIGHT_BORDER)
    pygame.draw.rect(WIN, INDIGO, LOWER_BORDER)
    pygame.draw.rect(WIN, INDIGO, UPPER_BORDER)
    
    red_health_text = HEALTH_FONT.render("Health: "+ str(red_health), 1, INDIGO)
    yellow_health_text = HEALTH_FONT.render("Health: "+ str(yellow_health), 1, INDIGO)
    WIN.blit(red_health_text, (10, 10)) 
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10)) #-10 pixels op y positie 10

    WIN.blit(RED_SMILEY, (red.x, red.y))           # blit to get services on the screen like the smileys met x en y waardes
    WIN.blit(YELLOW_SMILEY, (yellow.x, yellow.y))  # x en y worden beschreven in red en yellow
    

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, BLACK, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, BLACK, bullet)

    pygame.display.update() 

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x + 10: #LEFT
            yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL < WIDTH - IMG_WIDTH: #RIGHT
            yellow.x += VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL < HEIGHT - IMG_HEIGHT: #DOWN
            yellow.y += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0: #UP
            yellow.y -= VEL

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0: #LEFT
            red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL < BORDER.x - IMG_WIDTH: #RIGHT
            red.x += VEL
    if keys_pressed[pygame.K_s] and red.y + VEL < HEIGHT - IMG_HEIGHT : #DOWN
            red.y += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0: #UP
            red.y -= VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, INDIGO)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) # 5000 = 5 seconds (daarna restart)

async def main():   #async voor export naar web
    red = pygame.Rect(100, 300, IMG_WIDTH, IMG_HEIGHT)    # zodat smileys kunnen bewegen 100, 300 = x en y positie in bepaald oppervlak
    yellow = pygame.Rect(700,300, IMG_WIDTH, IMG_HEIGHT)  # vergeet niet red en yellow in draw window function te doen

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)                     # consistentie van game voor iedere pc
        for event in pygame.event.get():   
            if event.type == pygame.QUIT:   # zorgt dat loop eindigt
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + red.width, red.y + red.height//2 - 2, 10, 5) # zodat kogel direct van unit komt, posities + width en height
                    red_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet) 
                    #BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                yellow_health -= 1
                #BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT: 
                red_health -= 1
                #BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Purple Wins!"
                 
        if yellow_health <= 0:       
            winner_text = "Yellow Wins"

        if winner_text != "":
            draw_winner(winner_text)
            break #someone won

        await asyncio.sleep(0)

        

        keys_pressed = pygame.key.get_pressed()     # zorgt ervoor dat je meerder keys kunt gebruiken
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

    main()

    
if __name__=="__main__":    
    asyncio.run(main())              

        

