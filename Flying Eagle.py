import pygame
import random
from sys import exit

score = 0
lives = 6

class Cloud(pygame.sprite.Sprite):
    def __init__(self,speed):
        super().__init__()

        cloud = pygame.image.load('game_materials/cloud.png').convert_alpha()

        self.image = cloud
        self.rect = cloud.get_rect(midbottom = (1000,random.randint(80,500)))
        self.speed = speed

    def update(self):
          self.rect.x -= self.speed
          self.destroy()

    def destroy(self):
          if self.rect.x <= -100:
                self.kill
                global score
                score +=1


class Bird(pygame.sprite.Sprite):
    def __init__(self,check,height):
        super().__init__()
    
        self.check_time = check
        self.bird_height = height

        if self.check_time > 50:
            self.image = pygame.image.load('game_materials/bird.png').convert_alpha()
            self.rect = self.image.get_rect(midbottom = (230, self.bird_height))
        else:
            self.image = pygame.image.load('game_materials/bird_up.png').convert_alpha()
            self.rect = self.image.get_rect(midbottom = (230, self.bird_height))

        self.rect = self.image.get_rect(midbottom = (230, self.bird_height))


def collision_sprite(height):
    if pygame.sprite.spritecollide(bird.sprite, cloud_group, False,pygame.sprite.collide_rect_ratio(0.6)) or (height<-100 or height > 600):
        cloud_group.empty()
        return False
    else:
        return True
    

pygame.init()
font = pygame.font.Font('game_materials/font.ttf', 30)

def Score():
    score_surf = font.render(f'Score: {score}',False,(0,0,0))
    score_rect = score_surf.get_rect(center = (130,50))
    screen.blit(score_surf,score_rect)

def Lives():
    lives_surf = font.render(f'Lives left: {lives}',False,(0,0,0))
    lives_rect = lives_surf.get_rect(center = (740,47))
    screen.blit(lives_surf,lives_rect)

def Final():
    font = pygame.font.Font('font.ttf', 70)
    score_surf = font.render(f'Final Score: {score}',False,(0,0,0))
    score_rect = score_surf.get_rect(center = (450,303))
    scor_surf = font.render(f'Game over',False,(0,0,0))
    scor_rect = scor_surf.get_rect(center = (450,170))
    screen.blit(score_surf,score_rect)
    screen.blit(scor_surf,scor_rect)
     

screen = pygame.display.set_mode((900, 507))
clock = pygame.time.Clock()

pygame.display.set_caption('game_materials/Happy Bird')
background = pygame.image.load('game_materials/mountainsbackground.jpg').convert_alpha()
wasted = pygame.image.load('game_materials/wasted.png').convert_alpha()
start = pygame.image.load('game_materials/start.png').convert_alpha()

Music = pygame.mixer.Sound('game_materials/Virginia_Highway.mp3')
Music.set_volume(0.7)
Music.play(loops = -1)


cloud_group = pygame.sprite.Group()
bird = pygame.sprite.GroupSingle()
bird.add(Bird(51,230))

bird_height = 230
bird_speed = 1
bird_time = 0
check_time = 51
speed = 1.5
i = 0
game_active = True 
gap = pygame.USEREVENT + 1
pygame.time.set_timer(gap, 1500)
gapp = pygame.USEREVENT + 2
pygame.time.set_timer(gapp, 30000)
final_gap = pygame.USEREVENT + 3
pygame.time.set_timer(final_gap, 10000)

game_active = False
wasted_check = False
check = False
fly_sound = pygame.mixer.Sound('game_materials/swing_sound.mp3')
fly_sound.set_volume(0.5)

while True:
    bird_time += 0.02
    check_time += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_height -= 75
                bird_time = 0 
                check_time = 0
                check = False
                fly_sound.play()
        
        if event.type == gapp:
             speed += 0.02

        if event.type == gap:
             cloud_group.add(Cloud(speed))
             if i < 1295:
                i += 10
             pygame.time.set_timer(gap, 1400-i)
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True


    
    screen.blit(background, (0, 0))
    if game_active == False and wasted_check == False:
        screen.blit(start, (0, -40))

    Score()

    if game_active:

        bird.add(Bird(check_time,bird_height))

        cloud_group.draw(screen)
        cloud_group.update()

        bird.draw(screen)
        bird.update()

        bird_height += bird_speed + bird_time

        game_active = collision_sprite(bird_height)
        if not game_active:
            wasted_check = True

    else:
        if check == False:
            lives -= 1
            if lives < 0:
                break
        check = True
        if wasted_check == True:
            screen.blit(wasted, (0, 0))
            Lives()
            bird_height = 230
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
                screen.blit(background, (0,0))
                screen.blit(start, (0, -40))
                wasted_check = False

    pygame.display.update()
    clock.tick(90)

i = 0
while i < 500000:
    screen.blit(background, (0,0))
    Final()
    i+=1000
    pygame.display.update()
    clock.tick(90)

    