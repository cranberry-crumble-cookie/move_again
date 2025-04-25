import pygame, math
from sys import exit
import random
from random import randint
import time
import cv2
import threading
import serial

#ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

try: ser = serial.Serial('COM6', 115200, timeout=1)
except: print("poort wordt al gebruikt")

COM_EVENT = pygame.USEREVENT + 1

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("music/Les-feuilles-mortes.ogg")
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1200, 700))  # size screen
pygame.display.set_caption('MBC-project')  # name screen
clock = pygame.time.Clock()  # get time
font_1 = pygame.font.Font(None, 50)  # Check file path for the font


# images/surfaces
music1_color = (255, 255, 255)
music1_surf = font_1.render('Les feuilles mortes', False, (music1_color))
music1_rect = music1_surf.get_rect(midleft=(0, 670))
music1_playing = True




spring_touw_i_surf = pygame.image.load('graphics/spring_touw.jpg').convert_alpha()
spring_touw_i_surf = pygame.transform.scale(spring_touw_i_surf, (1300, 758))
spring_touw_i_rect = spring_touw_i_surf.get_rect(topleft=(-17, -10))
 
ski_i_surf = pygame.image.load('graphics/ski_view.jpg').convert_alpha()
ski_i_surf = pygame.transform.scale(ski_i_surf, (1300, 758))
ski_i_rect = ski_i_surf.get_rect(topleft=(-17, -10))
 
hinkel_i_surf = pygame.image.load('graphics/hinkel_view.jpg').convert_alpha()
hinkel_i_surf = pygame.transform.scale(hinkel_i_surf, (1300, 758))
hinkel_i_rect = hinkel_i_surf.get_rect(topleft=(-17, -10))
 
starttrans_surf = pygame.Surface((600, 500))
starttrans_surf.fill('pink')
starttrans_rect = starttrans_surf.get_rect(center=(600, 350))
 

# text
spring_touw_t_surf = font_1.render('spring touw', False, (251, 72, 196))
spring_touw_t_surf = pygame.transform.scale(spring_touw_t_surf, (250, 70))
spring_touw_t_rect = spring_touw_t_surf.get_rect(center=(250, 350))
 
ski_t_surf = font_1.render('Ski', False, (251, 72, 196))
ski_t_surf = pygame.transform.scale(ski_t_surf, (130, 70))
ski_t_rect = ski_t_surf.get_rect(center=(600, 350))
 
hinkel_t_surf = font_1.render('hinkel', False, (251, 72, 196))
hinkel_t_surf = pygame.transform.scale(hinkel_t_surf, (250, 70))
hinkel_t_rect = hinkel_t_surf.get_rect(center=(900, 350))
 
play_surf = font_1.render('Select', False, (251, 72, 196))
play_surf = pygame.transform.scale(play_surf, (200, 70))
play_rect = play_surf.get_rect(center=(600, 450))

tut_surf = font_1.render('Tutorials', False, (200, 60, 170))
tut_surf = pygame.transform.scale(tut_surf, (150, 40))
tut_rect = tut_surf.get_rect(topright=(1190, 10))




spring_tut_surf = font_1.render('Play springtouw turorial', False, (200, 60, 170))
spring_tut_surf = pygame.transform.scale(spring_tut_surf, (230, 60))
spring_tut_rect = spring_tut_surf.get_rect(center=(600, 100))

ski_tut_surf = font_1.render('Play ski tutorial', False, (200, 60, 170))
ski_tut_surf = pygame.transform.scale(ski_tut_surf, (230, 60))
ski_tut_rect = ski_tut_surf.get_rect(center=(600, 300))

hinkel_tut_surf = font_1.render('Play hinkel tutorial', False, (200, 60, 170))
hinkel_tut_surf = pygame.transform.scale(hinkel_tut_surf, (230, 60))
hinkel_tut_rect = hinkel_tut_surf.get_rect(center=(600, 500))


tut_back_surf = pygame.Surface(screen.get_size())
tut_back_surf.fill('blue')
tut_back_rect = tut_back_surf.get_rect(topleft=(0, 0))
tut_active = False




spel_opstart_surf = font_1.render('Opstarten van het spel...', False, (200, 60, 170))
#spel_opstart_surf = pygame.transform.scale(spel_opstart_surf, (230, 60))
spel_opstart_rect = spel_opstart_surf.get_rect(center=(600, 100))




 
start_view = 'spring_touw'
game_status = 'unstarted'
screen_center = (600, 350)
game_ready = 'not_ready'
game_choice = 'not choosed yet'
rect_width, rect_height = 0, 0
growth_rate = 50
pink = (255, 105, 180)
underline_color = pink
underline_thickness = 3



lock = threading.Lock()
def read_serial():
    global game_ready
    left_pressed = False
    right_pressed = False
    count_started = False
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode("utf-8")
            event = pygame.event.Event(COM_EVENT, message=data)
            pygame.event.post(event)

            if event.message.strip() == "left_button_pressed":
                left_pressed = True
            if event.message.strip() == "left_button_released":
                left_pressed = False
            if event.message.strip() == "right_button_pressed":
                right_pressed = True
            if event.message.strip() == "right_button_released":
                right_pressed = False



        '''
        if left_pressed == True and right_pressed == True:
            if count_started == False:
                start_hold = time.time()
                print("Count started")
                count_started = True
            elif count_started == True:
                if time.time() - start_hold >= 10:
                    with lock:
                        game_ready = "not_ready"
                    print("Back to menu")
                    count_started = False

        else:
            count_started = False

            #TIME.TIME() PROBLEM
            '''
            


def springtouw(game_state):
    global springtouw_i_surf, springtouw_i_rect, spring_touw_t_surf, spring_touw_t_rect, starttrans_surf, starttrans_rect, screen_y, screen_x, springtouwdeel_grootte, uitrekking, springtouwdeel_grootte, springtouw_draairichting, springtouw_achter, player, grond_hoogte, moeilijkheid, moeilijkheid_text, start_delay, end_delay, startup, end_delay, game_status, score, middelste_springtouwdeel, springtouw_group, springtouw_functie, grond, begin_achtergrond, achtergrond, player_breedte, player_lengte, player_grootte, springtouw_draairichting_save, springtouwdeel_grootte, springtouw_i_rect, springtouw_i_surf, spring_touw_t_surf, spring_touw_t_rect, starttrans_surf, starttrans_rect, verander_springtouwgrootte\
        ,snelheid_touw,tolerantie,groen_hoogte, x,move_springtouw,groen_jump,rood_jump,blit_tutorial_text1,blit_tutorial_text2,blit_tutorial_text3,plyr_kan_gekilled_wrdn
    
    #aanpasbare variabele, misschien in game class plaatsen voor overzichtelijkheid?
    hoogste_y = 0 #afblijven!!!!
    moeilijkheid = 1
    dood_delay = 300 #miliseconden
    start_delay = 1000
    snelheid_touw = 0.04
    zwaartekracht = 0.3
    spronghoogte = 5
    player_grootte = None
    tolerantie = 1 #hoe hoger, hoe makkelijker de player het springtouw raakt
    springtouwdeel_grootte = 10
    uitrekking = 120
    groen_hoogte = 320
    player_breedte=166
    player_lengte=250
    springtouw_draairichting = True #False or True elk voor een andere richting
    springtouw_draairichting_save = springtouw_draairichting#slaat de originele draairichting op soadt deze opnieuw kan toegewezen worden bij het opnieuw opstarten
    springtouw_achter = springtouw_draairichting
    startup = True
    end_delay = False
    move_springtouw = False
    groen_jump = False
    rood_jump = False
    blit_tutorial_text1 = False
    blit_tutorial_text2 = True
    blit_tutorial_text3 = False
    plyr_kan_gekilled_wrdn = True

    #initieer pygame en andere geralteerde zaken
    screen = pygame.display.set_mode((1000,500))
    screen_x = screen.get_width()
    screen_y = screen.get_height()
    pygame.display.set_caption('springtouw')
    game_status = game_state #starting_screen, playing, end_screenn instellingen, tutorial
    clock = pygame.time.Clock()
    none_font = pygame.font.Font(None,int(screen_y*(70/500)))
    start_font = pygame.font.Font(None,int(screen_y*(95/500)))
    instellingen_font = pygame.font.Font(None,int(screen_y*(60/500)))
    moeilijkheid_font = pygame.font.Font(None,int(screen_y*(70/500)))
    



    def relativeer(waarde,x_y = "y"):
        global screen_x, screen_y
        if x_y == "x":
            return screen_x*waarde/1000
        if x_y == "y":
            return screen_y*waarde/500
    groen_hoogte = relativeer(groen_hoogte)
    zwaartekracht = relativeer(zwaartekracht)
    spronghoogte = relativeer(spronghoogte)
    springtouwdeel_grootte = int(relativeer(springtouwdeel_grootte))
    uitrekking = relativeer(uitrekking)

    def springtouw_functie(invoerwaarde, x):
        global screen_y, screen_x, uitrekking, math
        return screen_y/2 + (math.sin(x)*math.sin(invoerwaarde*math.pi/screen_x)*uitrekking)

    minimum = springtouw_functie(screen_x/2, x = math.pi/2)
    maximum = springtouw_functie(screen_x/2, x = -math.pi/2)
    grond_hoogte = minimum + springtouwdeel_grootte/2

    def select_difficulty(difficulty): # nog implementeren
        global snelheid_touw, tolerantie, groen_hoogte
        if difficulty ==1:
            snelheid_touw = 0.02
            tolerantie =  1
            groen_hoogte = 350
        
        elif difficulty ==2:
            snelheid_touw = 0.03
            tolerantie = 2
            groen_hoogte = 315

        elif difficulty ==3:
            snelheid_touw = 0.04
            tolerantie = 3
            groen_hoogte = 280
       
    def restart_game():
        global startup, x, springtouw_draairichting,  springtouw_achter, player
        player.rect.bottom = grond_hoogte
        startup = True
        x = math.pi/2 + 0.5
        score.score = 0
        springtouw_draairichting = springtouw_draairichting_save
        springtouw_achter = springtouw_draairichting_save

    #veranderd de springtouwgrootte om een realistisch effect te geven, wordt gebruikt in "draairichting_springtouw"
    def verander_springtouwgrootte(groep,grootte):
        for springtouw in groep:
            springtouw.image = pygame.transform.scale(springtouw.image,(grootte,grootte))
            
    #bepaalt de draairiching van het springtouw, draairichting v.h. springtouw: True of False
    def draairichting_springtouw(richting):
        global springtouw_achter, game_status, verander_springtouwgrootte, middelste_springtouwdeel, end_delay

        if springtouw_achter:
            screen.blit(player.image,player.rect)

        #checkt of het srpingtouw op de grond is door naar de positie van het middelste deelte te kijken
        if middelste_springtouwdeel.rect.y >= minimum-tolerantie:
            springtouw_achter = richting  
            if richting:# als het srpingtouw achter de player is wordt het kleiner
                verander_springtouwgrootte(springtouw_group,springtouwdeel_grootte-1)

            else:#als het springtouw voor de player is wordt het groter
                verander_springtouwgrootte(springtouw_group,springtouwdeel_grootte+1) 

            if player.y_status == 'staan':#als de player niet heeft gesprongen verlies je
                end_delay = True
                if game_status == "tutorial":
                    select_difficulty(1)
                game_status = 'end_screen'
            
        #checkt of het springtouw aan de top is aan de hand van het middelste deel
        elif middelste_springtouwdeel.rect.y <= maximum+tolerantie:
            
            #afhankelijk van de richting(True of False) zal het de bepaald worden of het springtouw achter is of niet
            springtouw_achter = not richting
            if richting:
                verander_springtouwgrootte(springtouw_group,springtouwdeel_grootte+1)
       
            else:
                verander_springtouwgrootte(springtouw_group,springtouwdeel_grootte-1)
          
            if player.rect.top <= maximum+tolerantie:
                end_delay = True
                if game_status == "tutorial":
                    select_difficulty(1)
                game_status = 'end_screen'

    class Achtergrond:
        def __init__(self,achtergrond,x,y):
            self.image = pygame.image.load(achtergrond)
            self.image = pygame.transform.scale(self.image, (screen_x,screen_y))
            self.rect = self.image.get_rect(topleft = (x,y))

            self.green = pygame.Surface((screen_x,screen_y))
            self.green_rect = self.green.get_rect()
            self.green.fill("Green",self.green_rect)
            self.red = pygame.Surface((screen_x,screen_y))
            self.red_rect = self.red.get_rect()
            self.red.fill("Red",self.red_rect)
            self.air = pygame.Surface((screen_x,screen_y))
            self.air.fill("Lightblue")
            self.air_rect = self.air.get_rect()
        
        def blit(self,image,rect):
            screen.blit(image,rect)

    class Score():
        def __init__(self,x,y):
            self.score = 0
            self.image = none_font.render(f"score: {self.score}", True, (255,255,255))
            self.rect = self.image.get_rect(center = (x,y))
        
        def blit(self,x=screen_x/2,y=screen_y/10):
            self.rect.center = (x,y)
            screen.blit(self.image,self.rect)
    
        def update(self):
            self.image = none_font.render(f"score: {self.score}", True, (255,255,255))

    

    class Grond(Achtergrond):
        def __init(self,achtergrond,x,y):
            super().__init__(achtergrond,x,y)
            self.image = pygame.transform.scale(self.image, (screen_x,screen_y/2))
            self.rect = self.image.get_rect(topleft = (x,y))
        
    class Obstacle:
        def __init__(self,obstacle_image,pos_x,pos_y):
            self.image = pygame.image.load(obstacle_image)
            self.image = pygame.transform.scale(self.image,(screen_x/4,screen_y/3))
            self.image.set_colorkey((255,255,255))
            self.rect = self.image.get_rect(center = (pos_x,pos_y))
        
    class Springtouw_deel(Obstacle):
        def __init__(self,image,pos_x,pos_y,grootte):
            super().__init__(image,pos_x,pos_y)
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image,(grootte,grootte))
            self.rect = self.image.get_rect(center = (pos_x,pos_y))
        
    class Player(Obstacle):
        def __init__(self,obstacle_image,pos_x,pos_y,breedte,lengte):
            super().__init__(obstacle_image,pos_x,pos_y)
            self.image = pygame.transform.scale(self.image,(screen_y*breedte/500,screen_y*lengte/500))
            #self.image = pygame.transform.scale(self.image,(breedte,lengte))
            self.rect = self.image.get_rect()
            self.rect.centerx = screen_x/2
            self.image.set_colorkey((255,255,255))
            self.gravity = 0
            self.y_status = 'bestaan'
        
        def vallen(self):
            self.gravity -= zwaartekracht
            self.rect.y -= self.gravity
    
        def update_status(self):
            self.rect.y = self.rect.y - self.gravity
            if self.rect.bottom >= grond_hoogte: 
                self.rect.bottom = grond_hoogte
                self.y_status = 'staan'
            else: 
                self.vallen()
                self.y_status = 'vallen'
    
        def springen(self,hoogte):
            self.gravity = hoogte
        
    class Text():
        def __init__(self, text = "text",x=screen_x/2, y=screen_y/2, kleur=(255,255,255), font=none_font):
            self.font = font
            self.kleur = kleur
            self.image = self.font.render(text, True, self.kleur)
            self.rect = self.image.get_rect(center = (x,y))
            screen.blit(self.image,self.rect)
    
        def blit(self):
            screen.blit(self.image,self.rect)
        
        def update(self, text):
            self.image = self.font.render(text, True,self.kleur )

    start_text = Text(text = "druk op rechts om te beginnen", font=start_font, y = screen_y/2 -120)
    start_text2 = Text (text = "druk op links om ", font=start_font,y =screen_y/2 -50)
    start_text3 = Text(text = "moeilijkheid aan te passen",font=start_font, y =screen_y/2+20)
    moeilijkheid_text = Text(text=f"huidige moeilijkheid: {moeilijkheid}", font = moeilijkheid_font, y = screen_y/2 + screen_y/3)
    end_text = Text(text="verloren, druk op rechts", font = none_font,y=screen_y/2 - 25)
    end_text2 = Text(text="om opnieuw te beginnen", font = none_font,y=screen_y/2 + 25)
    instellingen_text = Text(text = "druk op b voor instellingen", font=instellingen_font, x=screen_x/2, y=screen_y/2 + screen_y/4)
    instellingenTerugkeer_text = Text(text="druk op b op terug te keren",font=instellingen_font)
    instellingenTerugkeer_text.rect.top=0
    tutorial_text1 = Text(text = "Spring bij groen!",font=start_font,y = screen_y/4)
    tutorial_text2 = Text(text = "elke sprong is een punt",font =start_font,y=screen_y/4 - 20)
    tutorial_text2_1 = Text(text = "knijp om te springen!", font = start_font,y=screen_y/4 + 50)
    tutorial_text3 = Text(text = "je verliest als je het springtouw raakt",font = none_font, y = screen_y/4 - 20)
    tutorial_text3_1 = Text(text = "probeer het eens uit", font = none_font, y = 7*screen_y/8)

    #maakt van de classes bruikbare objects
    player = Player('graphics/player2.png',screen_x/2,screen_y/2,250,166)
    player.rect.bottom = grond_hoogte
    grond = Grond('graphics/muur.png',0,grond_hoogte)
    begin_achtergrond = Achtergrond('graphics/muur.png',0,0)
    score = Score(screen_x/2,screen_y/10)
    achtergrond = Achtergrond('graphics/muur.png',0,0)
     
    #bepaal de x pos voor elk sprintouwdeel
    springtouw_group = []
    aantal_springtouwdelen = 300
    aantal_springtouw_gemaakt = 0
    for springtouw_deel in range(aantal_springtouwdelen):
        pos_x = aantal_springtouw_gemaakt*(screen_x)/(aantal_springtouwdelen-1)
        springtouw_deel = Springtouw_deel('graphics/muur.png',pos_x, screen_y/2, springtouwdeel_grootte)
        springtouw_group.append(springtouw_deel)
        aantal_springtouw_gemaakt += 1
        #print(aantal_springtouw_gemaakt)
    middelste_springtouwdeel = springtouw_group[int(aantal_springtouwdelen/2)]
    x = math.pi/2 + 0.5





    while True:
        if game_status == "tutorial":
            plyr_kan_gekilled_wrdn = False
            startup = False
    
        if middelste_springtouwdeel.rect.y > hoogste_y:
            hoogste_y = middelste_springtouwdeel.rect.y
            #print(hoogste_y)
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                    
            if game_status == 'starting_screen':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        select_difficulty(moeilijkheid)
                        restart_game()
                        game_status = 'playing'
                
                    if event.key == pygame.K_l:
                        if moeilijkheid == 3:
                            moeilijkheid = 1
                        else: moeilijkheid += 1
                        moeilijkheid_text.update(text = f"huidige moeilijkheid: {moeilijkheid}")
                    
                    if event.key == pygame.K_b:
                        game_status = 'instellingen'
                        print("instellingen")
                        
                if event.type == COM_EVENT:
                    if event.message.strip() == "right_button_pressed":
                        select_difficulty(moeilijkheid)
                        restart_game()
                        game_status = 'playing'
                    if event.message.strip() == "left_button_pressed":
                        if moeilijkheid == 3:
                            moeilijkheid = 1
                        else: moeilijkheid += 1
                        moeilijkheid_text.update(text = f"huidige moeilijkheid: {moeilijkheid}")
                        
                        
 #              elif event.type == COM_EVENT:
  #                  print(f"Received from COM port:{event.message}")
   #                 if event.message.strip() == "left_button_pressed":
#
 #                       if event.message.strip() == "left_button_released":   
                    
            elif game_status == 'playing':
                if player.y_status == 'staan':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            player.springen(spronghoogte)
                            score.score += 1
                    if event.type == COM_EVENT:
                        if event.message.strip() == "right_button_pressed" or "left_bitton_pressed":
                            player.springen(spronghoogte)
                            score.score += 1
                    
            elif game_status == 'end_screen':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_game()
                        game_status = 'playing'
                    if event.key == pygame.K_b:
                        game_status = 'instellingen'
                        print("instellingen")

                if event.type == COM_EVENT:
                    if event.message.strip() == "right_button_pressed":
                        restart_game()
                        game_status = 'playing'
        
            elif game_status == 'instellingen':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        game_status = 'starting_screen'
                        print("starting_screen")

                if event.type == COM_EVENT:
                    if event.message.strip() == "right_button_pressed" and "left_button_pressed":
                        pass
    
            elif game_status == 'tutorial':
                if player.y_status == 'staan':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            player.springen(spronghoogte)
                            score.score += 1
                            if move_springtouw == False:
                                move_springtouw = True
                                groen_jump = True
                                rood_jump = True
                    if event.type == COM_EVENT:
                        if event.message.strip() == "right_button_pressed" or "left_button_pressed":
                           player.springen(spronghoogte)
                           score.score += 1
                           if move_springtouw == False:
                               move_springtouw = True
                               groen_jump = True
                               rood_jump = True                           
                        
                        
                        
                        

        if game_status == 'starting_screen':
            begin_achtergrond.blit(achtergrond.image,achtergrond.rect)
            start_text.blit()
            start_text2.blit()
            start_text3.blit()
            moeilijkheid_text.blit()
            instellingen_text.blit()
        
        elif game_status == 'playing':
            screen.fill((255, 255, 255))

            #maakt het scherm groen als je moet springen
            if middelste_springtouwdeel.rect.y >= groen_hoogte and springtouw_draairichting != springtouw_achter:
                achtergrond.blit(achtergrond.green,achtergrond.green_rect)
            else:
                screen.blit(achtergrond.air,achtergrond.air_rect)
            
            screen.blit(grond.image,grond.rect)
            #print(score.score)
            score.update()
            score.blit()
            player.update_status()
        
            if springtouw_achter == False:
                screen.blit(player.image,player.rect)
            
            #springtouw y positite berkenen
            for springtouw in springtouw_group:
                springtouw.rect.y = springtouw_functie(springtouw.rect.center[0],x)
                #springtouw.rect.y = (screen_y/2 + (math.sin(x)*math.sin(springtouw.rect.x*math.pi/screen_x)*uitrekking))
                screen.blit(springtouw.image,springtouw.rect)
            x += snelheid_touw
            draairichting_springtouw(springtouw_draairichting)
        
            if startup == True:
                pygame.display.update()
                pygame.time.wait(start_delay)
                for event in pygame.event.get():#werkt opgestapelde events weg
                    pass
                startup = False
            #screen.blit(springtouw.image,springtouw.rect)
        
        
        elif game_status == 'end_screen':
            achtergrond.blit(achtergrond.image,achtergrond.rect)
            end_text.blit()
            end_text2.blit()
            instellingen_text.blit()
            score.blit(y=screen_y/2-screen_y/6)
            pygame.display.update()
            if end_delay == True: #zorgt ervoor dat je niet direct per ongeluk opnieuw start met spelen
                pygame.time.wait(dood_delay)
                for event in pygame.event.get():
                    pass
                end_delay = False
            
        elif game_status == 'instellingen':
            achtergrond.blit(achtergrond.image,achtergrond.rect)
            instellingenTerugkeer_text.blit()
            
        elif game_status == "tutorial":
            if score.score >= 3:
                plyr_kan_gekilled_wrdn = True
            
            #maakt het scherm groen als je moet springen
            if middelste_springtouwdeel.rect.y >= groen_hoogte and springtouw_draairichting != springtouw_achter:
                achtergrond.blit(achtergrond.green,achtergrond.green_rect)
                if groen_jump == False:
                    move_springtouw = False
                    blit_tutorial_text1 = True
            else:
                screen.blit(achtergrond.air,achtergrond.air_rect)
                if groen_jump == True:
                    move_springtouw = True
                groen_jump = False
                blit_tutorial_text1 = False
            
            #maakt het scherm rood als je niet moet springen
            if middelste_springtouwdeel.rect.y < (maximum+30) and middelste_springtouwdeel.rect.y > (maximum+10) and springtouw_draairichting == springtouw_achter and score.score >= 3:
                screen.blit(achtergrond.red,achtergrond.red_rect)
                if rood_jump == False:
                    move_springtouw = False
                    blit_tutorial_text3 = True
            else:
                if rood_jump == True:
                    move_springtouw = True
                rood_jump = False
                blit_tutorial_text3
                
                
            screen.blit(grond.image,grond.rect)
            #print(score.score)
            score.update()
            score.blit()
            player.update_status()
            
            if springtouw_achter == False:
                screen.blit(player.image,player.rect)
                
            #springtouw y positite berkenen
            for springtouw in springtouw_group:
                springtouw.rect.y = springtouw_functie(springtouw.rect.center[0],x)
                #springtouw.rect.y = (screen_y/2 + (math.sin(x)*math.sin(springtouw.rect.x*math.pi/screen_x)*uitrekking))
                screen.blit(springtouw.image,springtouw.rect)
            if move_springtouw:
                x += snelheid_touw
            draairichting_springtouw(springtouw_draairichting)
                
            if springtouw_achter:
                screen.blit(player.image,player.rect)
                
            #blit de tuturial text voor over het touw springen
            if blit_tutorial_text1:
                tutorial_text1.blit()       
            #blit de tutorial text voor punten halen
            elif blit_tutorial_text2:
                tutorial_text2.blit()
                tutorial_text2_1.blit()
                if move_springtouw == True and player.y_status == "staan":
                    blit_tutorial_text2 = False
            elif blit_tutorial_text3:
                tutorial_text3.blit()
                tutorial_text3_1.blit()
                if move_springtouw == True and player.y_status == "staan":
                    blit_tutorial_text2 = False
    
            if startup == True:
                pygame.display.update()
                pygame.time.wait(start_delay)
                for event in pygame.event.get():#werkt opgestapelde events weg
                    pass
                startup = False
        
        
        clock.tick(60)
        pygame.display.update() 









 
def ski_game():
    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption('Runner')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    
    class Sphere:
        def __init__(self):
            self.x = 300
            self.y = 0
            self.radius = 20
            self.color = (255, 255, 255)
            self.velocity_y = 0
            self.gravity = 0.22
            self.slow_fall_gravity = 0.04
            self.is_jumping = False
            self.is_space_held = False
            self.max_color_y = 700

        def update(self, points):
            if self.velocity_y > 0 and self.is_space_held:
                self.velocity_y += self.slow_fall_gravity
            else:
                self.velocity_y += self.gravity

            on_ground = False

            for point in points:
                if abs(point.rect.x - self.x) < 5:
                    if self.y + self.radius >= point.rect.y:
                        self.y = point.rect.y - self.radius
                        self.velocity_y = 0
                        on_ground = True

            if on_ground and self.is_jumping:
                self.velocity_y = -10
                self.is_jumping = False

            self.y += self.velocity_y
            
            normalized_height = max(0, min(self.max_color_y - self.y, self.max_color_y))
            red_intensity = int((normalized_height / self.max_color_y) * 255)
            self.color = (red_intensity, 100, 200)
            
            return on_ground

        def draw(self, surface):
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
    
    class Point(pygame.sprite.Sprite):
        def __init__(self, point_x, point_y, mountain_color=(100, 100, 100)):
            super().__init__()
            self.image = pygame.Surface((4, 1000))
            self.image.fill(mountain_color)
            self.rect = self.image.get_rect(topleft=(point_x, point_y))

        def update(self):
            self.rect.x -= 5
            
    class Snowflake:
        def __init__(self):
            self.x = random.randint(0, 1750)
            self.y = 0
            self.size = random.randint(2, 4)
            self.color = (255, 255, 255)
            self.speed = random.uniform(1, 3)
            self.horizontal_speed = random.uniform(-3,-3)

        def update(self):
            self.y += self.speed
            self.x += self.horizontal_speed
            
        def draw(self, surface):
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)
            
    class Deco:
        def __init__(self):
            #snoopy and woodstock
            self.sn_wo_width = 152
            self.sn_wo_hight = 96
            self.sn_wo_surf = pygame.image.load('graphics/snoopy_woodstock-removebg-preview.png').convert_alpha()
            self.sn_wo_surf = pygame.transform.scale(self.sn_wo_surf, (self.sn_wo_width, self.sn_wo_hight))
            self.sn_wo_y = 700
            self.sn_wo_x = 2000
            
            #snoopy on plane
            self.sn_pl_width = 115
            self.sn_pl_hight = 68
            self.sn_pl_surf = pygame.image.load('graphics/snoopy_plane-removebg-preview.png').convert_alpha()
            #self.sn_pl_surf = pygame.transform.flip(self.sn_pl_surf, True, False)
            self.sn_pl_surf = pygame.transform.scale(self.sn_pl_surf, (self.sn_pl_width, self.sn_pl_hight))
            self.sn_pl_y = 100
            self.sn_pl_x = -500
            
            #snoopy and snowman
            self.sn_sn_width = 85
            self.sn_sn_hight = 77
            self.sn_sn_surf = pygame.image.load('graphics/snoopy_snowman-removebg-preview.png').convert_alpha()
            self.sn_sn_surf = pygame.transform.scale(self.sn_sn_surf, (self.sn_sn_width, self.sn_sn_hight))
            self.sn_sn_y = 700
            self.sn_sn_x = 4000
            
            #snoopy and 3 woodstock
            self.sn_3wo_width = 115
            self.sn_3wo_hight = 68
            self.sn_3wo_surf = pygame.image.load('graphics/snoopy_3woodstock-removebg-preview.png').convert_alpha()
            self.sn_3wo_surf = pygame.transform.scale(self.sn_3wo_surf, (self.sn_3wo_width, self.sn_3wo_hight))
            self.sn_3wo_y = 700
            self.sn_3wo_x = 6000
            
            #snoopy and woodstock
            self.sn_ho_width = 152
            self.sn_ho_hight = 96
            self.sn_ho_surf = pygame.image.load('graphics/peanuts-snoopy-et-la-niche-du-chien-poster-poster-removebg-preview.png').convert_alpha()
            self.sn_ho_surf = pygame.transform.scale(self.sn_ho_surf, (self.sn_ho_width, self.sn_ho_hight))
            self.sn_ho_y = 700
            self.sn_ho_x = 8000
            
        def move(self):
            #snoopy and woodstock
            self.sn_wo_x -= 5
            if (self.sn_wo_x + self.sn_wo_width) < 0:
                self.sn_wo_x = randint(2000, 4000)
            self.sn_wo_rect = self.sn_wo_surf.get_rect(bottomleft=(self.sn_wo_x, self.sn_wo_y))
            
            #snoopy on plane
            self.sn_pl_x += 3
            if (self.sn_pl_x) > 1200:
                self.sn_pl_x = randint(-1000, -400)
                self.sn_pl_y = randint(60, 220)
            self.sn_pl_rect = self.sn_pl_surf.get_rect(bottomleft=(self.sn_pl_x, self.sn_pl_y))
            
            #snoopy and snowman
            self.sn_sn_x -= 5
            if (self.sn_sn_x + self.sn_sn_width) < 0:
                self.sn_sn_x = randint(2000, 4000)
            self.sn_sn_rect = self.sn_sn_surf.get_rect(bottomleft=(self.sn_sn_x, self.sn_sn_y))
            
            #snoopy and 3 woodstocks
            self.sn_3wo_x -= 5
            if (self.sn_3wo_x + self.sn_3wo_width) < 0:
                self.sn_3wo_x = randint(2000, 4000)
            self.sn_3wo_rect = self.sn_3wo_surf.get_rect(bottomleft=(self.sn_3wo_x, self.sn_3wo_y))
            
            #snoopy and woodstock
            self.sn_ho_x -= 5
            if (self.sn_ho_x + self.sn_ho_width) < 0:
                self.sn_ho_x = randint(2000, 4000)
            self.sn_ho_rect = self.sn_ho_surf.get_rect(bottomleft=(self.sn_ho_x, self.sn_ho_y))
            
        def draw(self):
            screen.blit(self.sn_wo_surf, self.sn_wo_rect)
            screen.blit(self.sn_pl_surf, self.sn_pl_rect)
            screen.blit(self.sn_sn_surf, self.sn_sn_rect)
            screen.blit(self.sn_3wo_surf, self.sn_3wo_rect)
            screen.blit(self.sn_ho_surf, self.sn_ho_rect)
    
    """def reset_game():
        global score, point_y, mountain_dir, sphere, points_group, last_point_time, was_on_ground, space_pressed, snowflakes
        score = 0
        point_y = 690
        mountain_dir = 'up'
        sphere = Sphere()
        points_group.empty()
        last_point_time = pygame.time.get_ticks()
        was_on_ground = True
        space_pressed = False
        snowflakes = []"""
        
        
    point_y = 1000
    points_group = pygame.sprite.Group()
    mountain_dir = 'up'
    sphere = Sphere()
    score = 0
    score_increment_timer = 0
    SCORE_INCREMENT_INTERVAL = 100

    deco = Deco()

    POINT_CREATION_INTERVAL = 40
    SNOWFLAKE_CREATION_INTERVAL = 1
    last_point_time = pygame.time.get_ticks()
    last_snowflake_time = pygame.time.get_ticks()

    snowflakes = []
    was_on_ground = True
    space_pressed = False
    game_state = 'playing'
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not sphere.is_jumping:
                        sphere.is_jumping = True 
                        space_pressed = True
                    sphere.is_space_held = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    sphere.is_space_held = False

                    


            elif event.type == COM_EVENT:
                print(f"Received from COM port:{event.message}")
                if event.message.strip() == "left_button_pressed":
                    if not sphere.is_jumping:
                        sphere.is_jumping = True 
                        space_pressed = True
                    sphere.is_space_held = True

                if event.message.strip() == "left_button_released":
                    sphere.is_space_held = False

                


        current_time = pygame.time.get_ticks()


        if game_state == 'playing':
            if sphere.velocity_y < 0:
                score_increment_timer += clock.get_time()
                if score_increment_timer >= SCORE_INCREMENT_INTERVAL:
                    score += 1
                    score_increment_timer = 0

            if current_time - last_point_time >= POINT_CREATION_INTERVAL:
                if mountain_dir == 'up':
                    
                    point_y -= 2
                    points_group.add(Point(1200, point_y, (130, 100, 100)))
                    if point_y < 570:
                        if random.random() < 0.028 or point_y < 450:
                            mountain_dir = 'down'
                elif mountain_dir == 'down':
                    point_y += 2

                    points_group.add(Point(1200, point_y, (100, 130, 100)))
                    if point_y > 600:
                        mountain_dir = 'up'


            if current_time - last_snowflake_time >= SNOWFLAKE_CREATION_INTERVAL:
                snowflakes.append(Snowflake())
                last_snowflake_time = current_time

            for snowflake in snowflakes[:]:
                snowflake.update()
                if snowflake.y > 700:
                    snowflakes.remove(snowflake)
                else:
                    for point in points_group:
                        if (snowflake.x >= point.rect.x and snowflake.x <= point.rect.x + point.rect.width) and \
                           (snowflake.y + snowflake.size >= point.rect.y and snowflake.y - snowflake.size <= point.rect.y + point.rect.height):
                            snowflakes.remove(snowflake)
                            break

            points_group.update()
            on_ground = sphere.update(points_group.sprites())

            if on_ground and not was_on_ground:
                if space_pressed:
                    ground_y_positions = []
                    for point in points_group:
                        if abs(point.rect.x - sphere.x) < 50:
                            ground_y_positions.append(point.rect.y)

                    if len(ground_y_positions) > 1:
                        slope = ground_y_positions[-1] - ground_y_positions[0]
                        if slope > 0:
                            print("The sphere has landed after jumping on falling ground!")
                        elif slope < 0:
                            print("GAME OVER")
                            print(f"Final Score: {score}")
                            game_state = 'over'
                        else:
                            print("The sphere has landed after jumping on flat ground!")
                    space_pressed = False

            was_on_ground = on_ground

            for point in points_group:
                if point.rect.x < 0:
                    points_group.remove(point)

            screen.fill((0, 0, 0))
            points_group.draw(screen)
            deco.move()
            deco.draw()
            
            if current_time >= 5000:
                sphere.draw(screen)
            elif 4970 <= current_time <=5030:
                print("GO!")
            else:
                print("Be ready!")
            

            # Draw each snowflake
            for snowflake in snowflakes:
                snowflake.draw(screen)

            score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
            screen.blit(score_surface, (10, 10))

        elif game_state == 'over':
            screen.fill((0, 0, 0))
            game_over_surface = font.render("GAME OVER", True, (255, 0, 0))
            score_surface = font.render(f'Final Score: {score}', True, (255, 255, 255))
            screen.blit(game_over_surface, (500, 300))
            screen.blit(score_surface, (500, 350))
            
            if space_pressed:
                points_group.empty()
                score = 0
                point_y = 690
                mountain_dir = 'up'
                sphere = Sphere()
                last_point_time = pygame.time.get_ticks()
                was_on_ground = True
                space_pressed = False
                snowflakes = []
                game_state = 'playing'
            
        
        pygame.display.update()
        clock.tick(60)




def hinkel_spel():
    global tegel_group, player, zet_tegel, tegel_move, player_op_tegel, jump, corrigeer_eerste_tegel, soort_beweging, score_indicator_speed, tegels_tussen, valsnelheid, tijd_om_te_springen, aantal_enkelvoudige_tegels_tussen, score, combo, afwijkingtegelplayer_corrigeren
    print('playing hinkel')
    #variabelen
    screen_x = 500
    screen_y = 700
    tegelgrootte = 65
    begin_tegelsnelheid = 10
    valsnelheid = 0
    zwaartekracht = 0.23
    spronggrootte = 2.3
    tijd_om_te_springen = 0
    aantal_enkelvoudige_tegels_tussen = 2
    #afblijven!!!, wordt gebruik voor berekeningen
    tegels_tussen = 1 
    score = 0
    score_indicator_speed = 6
    combo = 0

    zet_tegel = True
    tegel_move = False
    player_op_tegel = False
    jump = True
    corrigeer_eerste_tegel = True
    soort_beweging = "normaal"



    #initieer pygame
    screen = pygame.display.set_mode((screen_x,screen_y))
    pygame.display.set_caption('hinkelen')
    clock = pygame.time.Clock()
    none_font = pygame.font.Font(None,int(70))

    def afwijkingtegelplayer_corrigeren(obj1,obj2):
        global tegel_group
        for tegel in tegel_group:
            tegel.werkelijke_y -= (obj1.rect.centery-obj2.rect.centery)
            tegel.werkelijke_x -= (obj1.rect.centerx - obj2.rect.centerx)
            #tegel.werkelijke_y -= (obj1-obj2)
            #tegel.werkelijke_x -= (obj1.rect.centerx - obj2.rect.centerx)
        for tegel in tegel_group:
            tegel.update()

    def draw_object(screen,object):
        screen.blit(object.image,object.rect)
    
    def nieuwe_tegel_als_allen_dood_zijn():
        global tegel_group, zet_tegel, Tegel, corrigeer_eerste_tegel, screen_x
        if len(tegel_group) == 0: #maakt nieuwer begintegel wanneer alle tegels dood zijn
            zet_tegel = True
            tegel_group.add(Tegel(screen_x/2,0,True,"enkelvoudig"))
            corrigeer_eerste_tegel = True

    def momentele_tegel():
        global player, tegel_group
        return pygame.sprite.spritecollide(player,tegel_group,False)[0]

    class Tegel(pygame.sprite.Sprite):
        def __init__(self,x,y,zet_tegel,tegel_type):
            super().__init__()
            self.image = pygame.Surface((tegelgrootte,tegelgrootte))
            self.rect = self.image.get_rect(midbottom = (x,y))
            self.image.fill('Grey',self.image.get_rect().inflate(-2, -2))
            self.zet_tegel = zet_tegel
            self.werkelijke_y = self.rect.y
            self.werkelijke_x = self.rect.centerx
            self.tegel_type = tegel_type
    
        def update(self):
            self.rect.y = self.werkelijke_y
            self.rect.centerx = self.werkelijke_x
        
        def move(self,snelheid,richting= "y"):
            global zet_tegel,tegels_tussen
            if richting == "x":
                self.werkelijke_x += snelheid
                self.update()
            if richting == 'y':
                self.werkelijke_y += snelheid
                self.update()
                self.generate_tegel()
                if self.rect.top >= screen_y: #dood de tegels als ze uit het scherm gaan
                    self.kill()
    #                zet_tegel = False
        #     else:
            #      self.generate_tegel()
        
        def generate_tegel(self):
            global zet_tegel, tegels_tussen, aantal_enkelvoudige_tegels_tussen
        
            if zet_tegel == True and self.zet_tegel == True and self.rect.top >= 0:
                #print(self.rect.centerx, self.werkelijke_x)
                if tegels_tussen == aantal_enkelvoudige_tegels_tussen:
                    tegel_group.add(Tegel(self.werkelijke_x-(tegelgrootte/2),self.rect.top,True,"dubbel1"))
                    tegel_group.add(Tegel(self.werkelijke_x+(tegelgrootte/2),self.rect.top,False,"dubbel2"))
                    tegels_tussen = 0
                else:
                    tegels_tussen += 1
                    if "enkelvoudig" in self.tegel_type:
                        tegel_group.add(Tegel(self.werkelijke_x,self.rect.top,True,f"enkelvoudig{tegels_tussen}"))
                    
                    if  "dubbel" in self.tegel_type:    
                        tegel_group.add(Tegel(self.werkelijke_x + tegelgrootte/2,self.rect.top,True,f"enkelvoudig{tegels_tussen}"))
                self.zet_tegel = False
    
        def change_color(self, color):
            self.image.fill(color,self.image.get_rect().inflate(-2,-2))

            
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((40,40))
            self.rect = self.image.get_rect(center = (screen_x/2, ((screen_y/tegelgrootte)-4)*tegelgrootte + (tegelgrootte/2) ))
            self.image.fill('Red',self.image.get_rect().inflate(-2,-2))
            self.werkelijke_image_grootte = self.image.get_width()
            self.kan_jumpen = False
            self.werkelijke_x = self.rect.centerx
        
        def update_grootte(self,nieuwe_grootte):
            self.image = pygame.transform.scale(self.image,nieuwe_grootte)
            self.rect = self.image.get_rect(center = (self.rect.centerx, ((screen_y/tegelgrootte)-4)*tegelgrootte + (tegelgrootte/2) ))
            self.image.fill('Black')
            self.image.fill('Red',self.image.get_rect().inflate(-2,-2))
            self.rect.centerx = self.werkelijke_x
        
        def vallen(self):
            global valsnelheid, tijd_om_te_springen, tegel_move, spring_schuin,tegel_group, afwijkingtegelplayer_corrigeren, player_staat, soort_beweging
            print(f"tegel_move: {tegel_move}")
            if self.image.get_width() <= 40:
                #self.update_grootte((40,40))
                tijd_om_te_springen = 0
                if player_op_tegel == True:
                    self.kan_jumpen = True
                    tegel_move = False
                    #corigeer de tegels zodat ze in het midden staan wanneer de speler neer komt
                    afwijkingtegelplayer_corrigeren(momentele_tegel(), self)
            else:
                valsnelheid += zwaartekracht 
                self.werkelijke_image_grootte-=valsnelheid
        #        for tegel in pygame.sprite.spritecollide(player,tegel_group,False): 
         #           if tegel.tegel_type == "enkelvoudig2":
          #              self.werkelijke_x += tegelgrootte/22
                self.update_grootte((self.werkelijke_image_grootte,self.werkelijke_image_grootte))
                tijd_om_te_springen += 1
            

            if tegel_move:
                if soort_beweging == "dubbel_beweging1":
                    for tegel in tegel_group:
                        tegel.move(tegelgrootte/41, "x")
                        tegel.move(tegelgrootte/22)
                elif soort_beweging == "dubbel_beweging2":
                    for tegel in tegel_group:
                        tegel.move(-tegelgrootte/22, "x")
                elif soort_beweging == "dubbel_beweging3":
                    for tegel in tegel_group:
                        tegel.move(tegelgrootte/41, "x")
                        tegel.move(tegelgrootte/22)
            
                else:
                    for tegel in tegel_group:
                        tegel.move(tegelgrootte/22)
            
                
            else: #maakt de tegel rood als je er op staat en de andere grijs
                if self.kan_jumpen == True:
                    soort_beweging = "normaal"
                for tegel in tegel_group:
                    if tegel.rect.colliderect(player) == False:
                        tegel.change_color("Grey")
                    else: 
                        tegel.change_color("Red")
                    
            if len(pygame.sprite.spritecollide(player,tegel_group,False)) != 0:
                #checkt of de voorwaarde voor eerste dubbelsprong waar te maken
                if self.kan_jumpen == True:
                    if momentele_tegel().tegel_type == f"enkelvoudig{aantal_enkelvoudige_tegels_tussen}":
                        soort_beweging = "dubbel_beweging1"
                    elif momentele_tegel().tegel_type == "dubbel1":
                        soort_beweging = "dubbel_beweging2"
                    elif momentele_tegel().tegel_type == "dubbel2":
                        soort_beweging = "dubbel_beweging3"


        def springen(self):
            global valsnelheid, tegel_move, score, player_staat
            if event.message.strip() == "left_button_pressed" and self.kan_jumpen:
                score_indicator.check_kleur()
                self.kan_jumpen = False
                valsnelheid = -spronggrootte
                self.werkelijke_image_grootte-=valsnelheid
                self.update_grootte((self.werkelijke_image_grootte,self.werkelijke_image_grootte))
                if player_op_tegel == True:
                    tegel_move = True
                
    class Score:
        def __init__(self):
            self.image = none_font.render(f'score: {score}',True, "White")
            self.rect = self.image.get_rect(center = (screen_x/2, 50))
        def secret_button(self):
            global score
            if event.key == pygame.K_m:
                score += 1
                self.update()
        def update(self):
            global score
            self.image = none_font.render(f'score: {score}',True, "White")


    class Score_balk:
        def __init__(self, color, width):
            self.image = pygame.surface.Surface((width,50))
            self.image.fill(color)
            self.rect = self.image.get_rect(center = (screen_x/2,screen_y-50))
            score_balk_group.append(self)
            self.range = range(self.rect.left,self.rect.right)
        
    class Score_indicator:
        def __init__(self):
            self.image = pygame.Surface((10,50))
            self.rect = self.image.get_rect(center = (screen_x/2,screen_y-50))
        def move(self):
            global score_indicator_speed
            if self.rect.right >= score_balk_red.rect.right or self.rect.left <= score_balk_red.rect.left:
                score_indicator_speed = -score_indicator_speed
            self.rect.centerx += score_indicator_speed
        def check_kleur(self):
            global score
            if self.rect.centerx in score_balk_green.range:
                score += 1
                #print("score plus 1")
            elif self.rect.centerx in score_balk_yellow.range:
                score += 0.5
                #print(" score plus 0.5")
            elif self.rect.centerx in score_balk_red.range:
                score -= 1
                #print("score min 1")
            score_text.update()
            #print(score)
            #print("---"*5)

    #maakt player, player groep, eerste tegel en tegel groep
    begintegel = Tegel(screen_x/2,0,True,"enkelvoudig1")
    tegel_group = pygame.sprite.Group()
    tegel_group.add(begintegel)
    player = Player()

    score_balk_group = []
    score_balk_yellow = Score_balk("Yellow",200/1.75)
    score_balk_red = Score_balk("Red",200)
    score_balk_green = Score_balk("Green",200/5)
    score_indicator = Score_indicator()
    score_text = Score()



    draw_group = [score_text,score_balk_red,score_balk_yellow,score_balk_green,score_indicator,player]
    while True:
        if len(pygame.sprite.spritecollide(player,tegel_group,False)) != 0 and len(tegel_group.sprites()) >= 6:
       #     print(tegel_group.sprites().index(pygame.sprite.spritecollide(player,tegel_group,False)[0]))
            #print(momentele_tegel().tegel_type)
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == COM_EVENT:
                #score_text.secret_button()
                player.springen()

        player.vallen()
            
            
        if player_op_tegel == False: #aan het begin van de game komen de tegels naar beneden tot de player
            for tegel in tegel_group:
                tegel.move(begin_tegelsnelheid)
                if corrigeer_eerste_tegel == True:
                    if tegel.rect.centery > player.rect.centery: #tegels stoppen wanneer ze bij player komen
                        player_op_tegel = True
                        player.kan_jumpen = True
                        afwijkingtegelplayer_corrigeren(tegel, player)
                        corrigeer_eerste_tegel = False
        elif pygame.sprite.spritecollide(player,tegel_group,False) == []:#player is niet meer op tegel als er geen collisions zijn
            player_op_tegel = False
        


        nieuwe_tegel_als_allen_dood_zijn()#gaat alleen iets doen als er een limiet op aantal tegels staat
        score_indicator.move()

        screen.fill((100, 100, 100))
        tegel_group.draw(screen)
        for object in draw_group:
            draw_object(screen,object)

        clock.tick(60)
        pygame.display.update()
        
 
 








 












'''
ski_tut_video = 'graphics/ski_tut_video.mp4'
cap = cv2.VideoCapture(ski_tut_video)

if not cap.isOpened():
    print("Error opening ski tutorial video")
    sys.exit()
    
     '''


















def spring_tutorial():
    global game_status
    running = True
    while running:
        screen.fill('red')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # to quit
                exit_main_code
            if event.type == pygame.MOUSEBUTTONDOWN:  # Click to exit tutorial
                running = False
        
        springtouw("tutorial")

        pygame.display.update()
        clock.tick(60)

    #game_status = 'menu'  # Return to menu when done
    pass


'''
def ski_tutorial():
    global game_status, ski_tut_paused
    running = True
    while running:
        screen.fill('green')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # to quit
                exit_main_code()
            elif event.type == pygame.KEYDOWN:  # Click to exit tutorial
                if event.key == pygame.K_SPACE:
                    ski_tut_paused = not ski_tut_paused

        if not ski_tut_paused:
            ret, frame = ski_tut_cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1200, 700))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame, (0, 0))
            last_frame = frame
        else:
            if last_frame is not None:
                screen.blit(last_frame, (0, 0))


            

        pygame.display.update()
        clock.tick(60)

    ski_tut_cap.release()
    game_status = 'menu'  # Return to menu when done
'''




#spring_tut_video = 'graphics/spring_tut_video.mp4'
ski_tut_video = 'graphics/ski_tut_video.mp4'
ski_tut_cap = cv2.VideoCapture(ski_tut_video)
if not ski_tut_cap.isOpened():
    print("Error opening ski tutorial video")
    exit()

ski_tut_paused = False



def ski_tutorial():
    global game_status, ski_tut_paused, game_mode, start_view

    comment = "No comment"
    com_surf = font_1.render(comment, False, (200, 60, 170))
    com_rect = com_surf.get_rect(midtop=(600, 0))
    show_comment = False

    running = True
    first_tick = pygame.time.get_ticks()
    second_tick = None
    second_tick_checked = False
    last_frame = None
    space_pressed = False
    third_tick = None
    wrong_release = False
    release_start = None
    total_release_duration = 0
    
    frames_passed = 0

    while running:
        #print(f"running while loop ski tutorial for testing on 10:47 23/04/2025: {running}")
        screen.fill('green')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_main_code()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                    # If space is pressed again after wrong release, measure release duration
                    if wrong_release:
                        wrong_release = False
                        release_end = pygame.time.get_ticks()
                        total_release_duration += release_end - release_start
                # No need to reset second_tick here — handled below
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
                    if second_tick:  # Only start tracking wrong release *after* second_tick is active
                        wrong_release = True
                        release_start = pygame.time.get_ticks()

        current_time = pygame.time.get_ticks()

        # After 1800ms: first pause
        if current_time - first_tick >= 1800 and not third_tick:
            ski_tut_paused = True
            show_comment = True
            comment = "Keep space pressed to continue"
            com_surf = font_1.render(comment, False, (200, 60, 170))
            com_rect = com_surf.get_rect(midtop=(600, 0))

            

            if space_pressed:
                if not second_tick_checked:
                    second_tick_checked = True
                    second_tick = current_time
                ski_tut_paused = False
                show_comment = False
                comment = "No comment"
                com_surf = font_1.render(comment, False, (200, 60, 170))
                com_rect = com_surf.get_rect(midtop=(600, 0))


        # Continuously update second_tick if needed
        if second_tick is not None and not ski_tut_paused and not third_tick:
            adjusted_elapsed = current_time - second_tick - total_release_duration
            if adjusted_elapsed >= 1200:
                ski_tut_paused = True
                third_tick = current_time
                show_comment = True
                comment = "Release space to make the skyer fall in the downhill"
                com_surf = font_1.render(comment, False, (200, 60, 170))
                com_rect = com_surf.get_rect(midtop=(600, 0))


        if third_tick:
            if not space_pressed:
                ski_tut_paused = False
                show_comment = False
            else:
                ski_tut_paused = True
                comment = "Release space to make the skyer fall in the downhill"
                com_surf = font_1.render(comment, False, (200, 60, 170))
                com_rect = com_surf.get_rect(midtop=(600, 0))
                show_comment = True        





        # Display logic
        if not ski_tut_paused:
            ret, frame = ski_tut_cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1200, 700))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame, (0, 0))
            last_frame = frame
            frames_passed += 1
        else:
            if last_frame is not None:
                screen.blit(last_frame, (0, 0))

        # Display comment if needed
        if show_comment:
            screen.blit(com_surf, com_rect)

        if frames_passed > 300:
            ski_tut_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            game_status = 'menu'
            running = False


        pygame.display.update()
        clock.tick(60)

    
    ski_tut_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    #game_mode = 'ski'
    running = False
    '''
    game_status = 'tutorial_menu_selected'
    game_mode = 'tutorial_menu'
    start_view = 'tutorial_menu'
'''
    #print(f"running: {running}")
    pass



'''
hinkel1_tut_surf = font_1.render("Hinkel Tutorial", True, (255, 255, 255))
hinkel1_tut_rect = hinkel_tutorial_surf.get_rect(midtop=(600, 0))

hinkel2_tut_surf = font_1.render("Hinkel Tutorial", True, (255, 255, 255))
hinkel2_tut_rect = hinkel2_tut_surf.get_rect(center=(600, 350))

def hinkel_tutorial():
    global game_status
    running = True
    while running:
        screen.fill('magenta')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # to quit
                exit_main_code()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Click to exit tutorial
                running = False


        screen.blit(hinkel1_tut_surf, hinkel1_tut_rect)

        pygame.display.update()
        clock.tick(60)

    game_status = 'menu'  # Return to menu when done

'''
def hinkel_tutorial():
    pass

def exit_main_code():
    ski_tut_cap.release()
    pygame.quit()
    exit()






game_mode = None
mouse_x, mouse_y = 900, 350


# Run serial reading in a separate thread
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

left_pressed, right_pressed = False, False
old_left_press, old_right_press = False, False


tut_option = 'spring'
back_to_menu = False

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit event
            exit_main_code()
            
        elif event.type == COM_EVENT:
            print(f"Received from COM port:{event.message}")
            if event.message.strip() == "left_button_pressed":
                left_pressed = True

            if event.message.strip() == "right_button_pressed":
                right_pressed = True

            if event.message.strip() == "left_button_released":
                left_pressed = False

            if event.message.strip() == "right_button_released":
                right_pressed = False
                
                
            if left_pressed == False and right_pressed == False:
                if old_left_press == True and old_right_press == False:
                    if game_status == 'tutorial_menu_selected':
                        if tut_option == 'spring':
                            tut_option = 'hinkel'
                        elif tut_option == 'hinkel':
                            tut_option = 'ski'
                        elif tut_option == 'ski':
                            tut_option = 'spring'
                        
                    else:
                        if mouse_x == 900:
                            mouse_x = 600
                            mouse_y = 350
                        elif mouse_x == 600:
                            mouse_x = 260
                            mouse_y = 350
                        elif mouse_x == 260:
                            mouse_x = 1180
                            mouse_y = 11
                        elif mouse_x == 1180:
                            mouse_x = 900
                            mouse_y = 350

                if old_left_press == False and old_right_press == True:
                    if game_status == 'tutorial_menu_selected':
                        if tut_option == 'spring':
                            tut_option = 'ski'
                        elif tut_option == 'ski':
                            tut_option = 'hinkel'
                        elif tut_option == 'hinkel':
                            tut_option = 'spring'
                            
                    else:
                        if mouse_x == 900:
                            mouse_x = 1180
                            mouse_y = 11
                        elif mouse_x == 1180:
                            mouse_x = 260
                            mouse_y = 350
                        elif mouse_x == 260:
                            mouse_x = 600
                            mouse_y = 350
                        elif mouse_x == 600:
                            mouse_x = 900
                            mouse_y = 350


            if game_status == 'tutorial_menu_selected':
                if left_pressed == True and right_pressed == True:
                    if tut_option == 'spring':
                        spring_tutorial()
                        back_to_menu = True
                    elif tut_option == 'ski':
                        ski_tutorial()
                        back_to_menu = True
                    elif tut_option == 'hinkel':
                        hinkel_tutorial()
                        back_to_menu = True
            
            else:
                back_to_menu = False
                if left_pressed == True and right_pressed == True:
                    mouse_x, mouse_y = 600, 600



            old_left_press, old_right_press = left_pressed, right_pressed

        # Handle start page (before game starts)
        if game_ready == 'not_ready':
            if (mouse_x, mouse_y) == (260, 350):
                print('springtouw selected')
                start_view = 'spring_touw'
            elif (mouse_x, mouse_y) == (600, 350):
                start_view = 'ski'
                print('ski selected')
            elif (mouse_x, mouse_y) == (900, 350):
                start_view = 'hinkel'
                print('hinkel selected')
            elif (mouse_x, mouse_y) == (600, 600):
                game_status = 'started'
            elif (mouse_x, mouse_y) == (1180, 11):
                start_view = 'tutorial_menu'
                print('tut selected')
                
            if game_mode == 'tutorial_menu':
                if (mouse_x, mouse_y) == (600, 100):
                    tut_option = 'spring'
                elif (mouse_x, mouse_y) == (600, 300):
                    tut_option = 'ski'
                elif (mouse_x, mouse_y) == (600, 500):
                    tut_option = 'hinkel'
            
            
            
            
            
            '''
            if spring_tut_rect.collidepoint(mouse_x, mouse_y):
                game_status = 'spring_tutorial'
            elif ski_tut_rect.collidepoint(mouse_x, mouse_y):
                game_status = 'ski_tutorial'
            elif hinkel_tut_rect.collidepoint(mouse_x, mouse_y):
                game_status = 'hinkel_tutorial'
            '''


            


    if game_ready == 'ready':
        #time.sleep(0.7)
        # Handle game screen logic when ready
        screen.fill('pink')
        #print(game_mode)
        if game_mode == 'spring_touw':
            springtouw("starting_screen")
            print('playing spring touw')
        elif game_mode == 'ski':
            ski_game()
            print('playing ski')
        elif game_mode == 'hinkel':
            hinkel_spel()
            print('playing hinkel')
        elif game_mode == 'tutorial_menu':
            game_status = 'tutorial_menu_selected'
    

    distance_x = mouse_x - screen_center[0]
    distance_y = mouse_y - screen_center[1]
    # Update background images and game view
    if start_view == 'spring_touw':
        spring_touw_i_rect.center = (screen_center[0] + distance_x / 20, screen_center[1] + distance_y / 20)
        screen.blit(spring_touw_i_surf, spring_touw_i_rect)
        underline_rect = pygame.Rect(spring_touw_t_rect.left, spring_touw_t_rect.bottom - 5, spring_touw_t_rect.width, underline_thickness)
        pygame.draw.rect(screen, underline_color, underline_rect)
        game_mode = 'spring_touw'
    
    elif start_view == 'ski':
        ski_i_rect.center = (screen_center[0] + distance_x / 20, screen_center[1] + distance_y / 20)
        screen.blit(ski_i_surf, ski_i_rect)
        underline_rect = pygame.Rect(ski_t_rect.left, ski_t_rect.bottom - 5, ski_t_rect.width, underline_thickness)
        pygame.draw.rect(screen, underline_color, underline_rect)
        game_mode = 'ski'
    
    elif start_view == 'hinkel':
        hinkel_i_rect.center = (screen_center[0] + distance_x / 20, screen_center[1] + distance_y / 20)
        screen.blit(hinkel_i_surf, hinkel_i_rect)
        underline_rect = pygame.Rect(hinkel_t_rect.left, hinkel_t_rect.bottom - 5, hinkel_t_rect.width, underline_thickness)
        pygame.draw.rect(screen, underline_color, underline_rect)
        game_mode = 'hinkel'
    
    elif start_view == 'tutorial_menu':
        screen.fill((50, 20, 20))
        game_mode = "tutorial_menu"
    
    # Draw buttons and options
    screen.blit(spring_touw_t_surf, spring_touw_t_rect)
    screen.blit(ski_t_surf, ski_t_rect)
    screen.blit(hinkel_t_surf, hinkel_t_rect)
    screen.blit(play_surf, play_rect)
    screen.blit(tut_surf, tut_rect)
    
    screen.blit(music1_surf, music1_rect)

    # Transition effects for game start
    if game_status == 'started':
        rect_width += growth_rate
        rect_height += growth_rate
        if rect_width >= screen.get_width():
            game_ready = 'ready'
        elif rect_height >= screen.get_height():
            rect_height = screen.get_height()
        starttrans_surf = pygame.Surface((rect_width, rect_height))
        starttrans_surf.fill('pink')
        starttrans_rect = starttrans_surf.get_rect(center=screen_center)
        screen.blit(starttrans_surf, starttrans_rect)
        screen.blit(spel_opstart_surf, spel_opstart_rect)
    
        
        
    # Handle tutorials
    #print(f"game status: {game_status}")
    if game_status == 'tutorial_menu_selected':
        tut_active = True
        screen.blit(tut_back_surf, tut_back_rect)
        screen.blit(spring_tut_surf, spring_tut_rect)
        screen.blit(ski_tut_surf, ski_tut_rect)
        screen.blit(hinkel_tut_surf, hinkel_tut_rect)
        
        if tut_option == 'spring':
            print("playing spring tutorial")
            pygame.draw.circle(screen, 'pink', (470, 100), 10)
            
        elif tut_option == 'ski':
            print("playing ski tutorial")
            pygame.draw.circle(screen, 'pink', (470, 300), 10)
            
        elif tut_option == 'hinkel':
            print("playing hinkel tutorial")
            pygame.draw.circle(screen, 'pink', (470, 500), 10)
    
    '''
    elif game_status == 'spring_tutorial':
        tut_active = True
        spring_tutorial()
    elif game_status == 'ski_tutorial':
        tut_active = True
        ski_tutorial()
    elif game_status == 'hinkel_tutorial':
        tut_active = True
        hinkel_tutorial()
    else:
        tut_active = False
    '''
    
    old_game_status = game_status
    #print(f"game status: {game_status} | old game status: {old_game_status}")
    if back_to_menu:
        game_status = 'menu'
        back_to_menu = False
        game_ready = 'not_ready'
        start_view = start_view
        game_mode = None
        mouse_x, mouse_y = 900, 350
        tut_option = 'spring'
        tut_active = False
        left_pressed, right_pressed = False, False
        old_left_press, old_right_press = False, False
            
    
    pygame.display.update()
    clock.tick(60)
