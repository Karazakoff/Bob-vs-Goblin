import pygame
import random


pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1000,680))

pygame.display.set_caption("Mario")

walk_right = [pygame.image.load('Pictures/R1.png'), pygame.image.load('Pictures/R2.png'), pygame.image.load('Pictures/R3.png'),
              pygame.image.load('Pictures/R4.png'),pygame.image.load('Pictures/R5.png'), pygame.image.load('Pictures/R6.png'),
              pygame.image.load('Pictures/R7.png'), pygame.image.load('Pictures/R8.png'), pygame.image.load('Pictures/R9.png')]

walk_left = [pygame.image.load('Pictures/L1.png'), pygame.image.load('Pictures/L2.png'), pygame.image.load('Pictures/L3.png'),
             pygame.image.load('Pictures/L4.png'), pygame.image.load('Pictures/L5.png'), pygame.image.load('Pictures/L6.png'),
             pygame.image.load('Pictures/L7.png'), pygame.image.load('Pictures/L8.png'), pygame.image.load('Pictures/L9.png')]

#bullet_sound = pygame.mixer.Sound("musics/bullet.mp3")

music = pygame.mixer.music.load('musics/music.mp3')
pygame.mixer.music.play(-1)

bg1 = pygame.image.load('Pictures/bg.jpg')
char = pygame.image.load('Pictures/standing.png')
bg2 = pygame.image.load('Pictures/bg2.jpg')
changer = [bg1, bg2]

class player(object):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.is_jump = False
        self.jump_count = 10
        self.san = 0
        self.counter = 0
        self.standing = True
        self.hit_box = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, screen):
        if self.counter != 200:
            screen.blit(changer[self.san], (0, 0))
        elif self.counter == 200:
            self.san = self.san + 1
            if self.san == 2:
                self.san = 0
            self.counter = 0
        self.counter = self.counter + 1

        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if self.standing == False:
            if self.left:
                screen.blit(walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count = self.walk_count + 1
            elif self.right:
                screen.blit(walk_right[self.walk_count // 3], (self.x, self.y))
                self.walk_count = self.walk_count + 1
        else:
            if self.right:
                screen.blit(walk_right[0], (self.x, self. y))
            else:
                screen.blit(walk_left[0], (self.x, self.y))

        self.hit_box = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(screen, (255, 0, 0), self.hit_box, 2)

    def hit(self):
        self.jump_count = 10
        self.is_jump = False
        self.x = 50
        self.y = 580
        self.walk_count = 0
        font_1 = pygame.font.SysFont('comicsans', 150)
        text = font_1.render('-10', 1, (255, 0, 0))
        screen.blit(text, (500 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 20 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)



class Enemy(object):
    walk_right = [pygame.image.load('Pictures/R1E.png'), pygame.image.load('Pictures/R2E.png'), pygame.image.load('Pictures/R3E.png'),
                 pygame.image.load('Pictures/R4E.png'), pygame.image.load('Pictures/R5E.png'), pygame.image.load('Pictures/R6E.png'),
                 pygame.image.load('Pictures/R7E.png'), pygame.image.load('Pictures/R8E.png'), pygame.image.load('Pictures/R9E.png'),
                 pygame.image.load('Pictures/R10E.png'), pygame.image.load('Pictures/R11E.png')]

    walk_left = [pygame.image.load('Pictures/L1E.png'), pygame.image.load('Pictures/L2E.png'), pygame.image.load('Pictures/L3E.png'),
                pygame.image.load('Pictures/L4E.png'), pygame.image.load('Pictures/L5E.png'), pygame.image.load('Pictures/L6E.png'),
                pygame.image.load('Pictures/L7E.png'), pygame.image.load('Pictures/L8E.png'), pygame.image.load('Pictures/L9E.png'),
                pygame.image.load('Pictures/L10E.png'), pygame.image.load('Pictures/L11E.png')]

    def __init__(self, x, y, w, h, end, vel):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.vel = vel
        self.hit_box = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0

            if self.vel > 0:
                screen.blit(self.walk_right[self.walk_count // 3], (self.x , self.y))
                self.walk_count = self.walk_count + 1
            else:
                screen.blit(self.walk_left[self.walk_count // 3], (self.x, self.y))
                self.walk_count = self.walk_count + 1
            pygame.draw.rect(screen, (255, 0, 0), (self.hit_box[0], self.hit_box[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0, 128, 0), (self.hit_box[0], self.hit_box[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hit_box = (self.x + 17, self.y + 2, 31, 57)
        else:
            self.hit_box = (0,0,1,1)
            #pygame.draw.rect(screen, (255, 0, 0), self.hit_box, 2)
    def move(self):

        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.walk_count = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.walk_count = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("I can feel it")


def redraw_game_window():
    screen.blit(bg1, (0,0))
    text = font.render('Score: ' + str(score), 1, (255, 0, 0))
    man.draw(screen)
    screen.blit(text, (390, 10))
    goblin.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.update()



#         main loop

font = pygame.font.SysFont('kariepulli', 30, True)
man = player(50, 580, 64, 64)
goblin = Enemy(200, 580, 64, 64, 950, 5)
bullets = []
shoot_loop = 0
score = 0
run = True
while run:

    clock.tick(27)
    if goblin.visible == True:
        if man.hit_box[1] < goblin.hit_box[1] + goblin.hit_box[3] and man.hit_box[1] + man.hit_box[3] > goblin.hit_box[1]:
            if man.hit_box[0] + man.hit_box[2] > goblin.hit_box[0] and man.hit_box[0] < goblin.hit_box[0] + goblin.hit_box[2]:
                man.hit()
                score  = score - 10
    else:
        speed = goblin.vel
        del goblin
        speed += 2
        goblin = Enemy(200,580, 64, 64, 950, speed)
    if shoot_loop > 0:
        shoot_loop += 1
    if shoot_loop > 3:
        shoot_loop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
            if bullet.y - bullet.radius < goblin.hit_box[1] + goblin.hit_box[3] and bullet.y + bullet.radius > goblin.hit_box[1]:
                if bullet.x + bullet.radius > goblin.hit_box[0] and bullet.x - bullet.radius < goblin.hit_box[0] + goblin.hit_box[2]:
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))

            if bullet.x < 1000 and bullet.x > 0:
                bullet.x = bullet.x + bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot_loop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 3:
            a = random.randrange(0, 255)
            b = random.randrange(0, 255)
            c = random.randrange(0, 255)
            bullets.append(Projectile(round(man.x + man.w // 2), round(man.y + man.h // 2), 8, (a, b, c), facing))
        shoot_loop = 1


    if keys[pygame.K_a] and man.x > man.vel:
        man.x = man.x - man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_d] and man.x < 1000 - man.w - man.vel:
        man.x = man.x + man.vel
        man.left = False
        man.right = True
        man.standing = False

    else:
        man.standing = True
        man.walk_count = 0


    if man.is_jump == False:
        if keys[pygame.K_w]:
            man.is_jump = True
            man.walk_count = 0
    else:
        if man.jump_count >= -10:
            neg = 1
            if man.jump_count < 0:
                neg = -1
            man.y = man.y - (man.jump_count ** 2) * 0.5 * neg
            man.jump_count = man.jump_count - 1
        else:
            man.is_jump = False
            man.jump_count = 10


    redraw_game_window()

pygame.quit()
