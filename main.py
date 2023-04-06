import pygame
import csv
import constants as const
from pygame import mixer
from character import Character
from weapon import Weapon
from items import Item
from world import World
from button import Button

pygame.init()
mixer.init()

screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')

# create clock for maintaining frame rate
clock = pygame.time.Clock()

# define game variables
screen_scroll = [0, 0]

# define fonts
font = pygame.font.Font('assets/fonts/AtariClassic.ttf', 20)


def scale_img(image, scale):
    # helper function to scale image
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w*scale, h*scale))


# load music and sounds
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
hit_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.5)
heal_fx = pygame.mixer.Sound("assets/audio/heal.wav")
heal_fx.set_volume(0.5)
player_ded_fx=pygame.mixer.Sound("assets/audio/player_ded.wav")
player_ded_fx.set_volume(0.1)

# load button images
start_img = scale_img(pygame.image.load(
    'assets/images/buttons/start_btn.png').convert_alpha(), const.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load(
    'assets/images/buttons/exit_btn.png').convert_alpha(), const.BUTTON_SCALE)
restart_img = scale_img(pygame.image.load(
    'assets/images/buttons/restart_btn.png').convert_alpha(), 3)
resume_img = scale_img(pygame.image.load(
    'assets/images/buttons/button_resume.png').convert_alpha(), const.BUTTON_SCALE)

#load starting bg img
BG=pygame.image.load('assets/misc/background.png').convert_alpha()


#load selection menu images
img1=scale_img(pygame.image.load('assets/images/characters/wizard/idle/0.png').convert_alpha(),10)
img2=scale_img(pygame.image.load('assets/images/characters/elf/idle/0.png').convert_alpha(),10)


# load heart images
heart_empty = scale_img(pygame.image.load(
    'assets/images/items/heart_empty.png').convert_alpha(), const.ITEM_SCALE)
heart_half = scale_img(pygame.image.load(
    'assets/images/items/heart_half.png').convert_alpha(), const.ITEM_SCALE)
heart_full = scale_img(pygame.image.load(
    'assets/images/items/heart_full.png').convert_alpha(), const.ITEM_SCALE)

# load coin images
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(
        f'assets/images/items/coin_f{x}.png').convert_alpha(), const.ITEM_SCALE)
    coin_images.append(img)

# load potion images
red_potion = scale_img(pygame.image.load(
    'assets/images/items/potion_red.png').convert_alpha(), const.POTION_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

# load weapon images
bow_img = scale_img(pygame.image.load(
    'assets/images/weapons/bow.png').convert_alpha(), const.WEAPON_SCALE)
arrow_img = scale_img(pygame.image.load(
    'assets/images/weapons/arrow.png').convert_alpha(), const.WEAPON_SCALE)
fireball_img = scale_img(pygame.image.load(
    'assets/images/weapons/fireball.png').convert_alpha(), const.FIREBALL_SCALE)
spear_img=scale_img(pygame.image.load(
    'assets/images/weapons/spear.png').convert_alpha(), const.WEAPON_SCALE)
staff_img=scale_img(pygame.image.load(
    'assets/images/weapons/staff.png').convert_alpha(), const.WEAPON_SCALE-0.100)

# load tilemap images
tile_list = []
for x in range(const.TILE_TYPES):
    tile_img = pygame.image.load(
        f"assets/images/tiles/{x}.png").convert_alpha()
    tile_img = pygame.transform.scale(
        tile_img, (const.TILE_SIZE, const.TILE_SIZE))
    tile_list.append(tile_img)

#load text image
text_img=pygame.image.load('assets/misc/text.png').convert_alpha()

def load_mobs_images(main_player):

    # load character images
    mob_animations = []
    if main_player=='elf':
        mob_types = ['elf','warrior_orc','masked_orc',
                    'shaman_orc','zombie',
                    'muddy','big_demon','necro',
                    'chort','wogol', 'skeleton']
    else:
        mob_types = ['wizard','warrior_orc','masked_orc',
                    'shaman_orc','zombie',
                    'muddy','big_demon','necro',
                    'chort','wogol', 'skeleton']
        

    animation_types = ['idle', 'run']
    # load images
    for mob in mob_types:
        animation_list = []
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            for i in range(4):
                img = pygame.image.load(
                    f'assets/images/characters/{mob}/{animation}/{i}.png').convert_alpha()
                if mob == 'elf' or mob=='wizard':
                    img = scale_img(img, const.SCALE+0.1)
                else:
                    img = scale_img(img, const.SCALE)
                temp_list.append(img)
            animation_list.append(temp_list)
        mob_animations.append(animation_list)
    main_game(mob_animations,main_player)
    return


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for displaying game info
def draw_info(player,level):
    pygame.draw.rect(screen, const.PANEL, (0, 0, const.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, const.WHITE, (0, 50), (const.SCREEN_WIDTH, 50))
    '''draw hearts/lives (5 full hearts each of 20 health points)
    half heart isnt printed only when the value of heart is 10,it can be printed
    if the players health is 43 or 77 or any number between 2 multiples of 20
    once a half heart is drawn,no hearts are required to draw so we'll draw empty hearts'''
    if level<=4:
        half_heart_drawn = False
        for i in range(5):
            if player.health >= ((i+1)*20):
                screen.blit(heart_full, (10+i*50, 0))
            elif player.health % 20 > 0 and half_heart_drawn == False:
                screen.blit(heart_half, (10+i*50, 0))
                half_heart_drawn = True
            else:
                screen.blit(heart_empty, (10+i*50, 0))

        # show level
        if level==1:
            txt='Goblins'
            color=const.GREEN
        elif level==2:
            txt='Undeads'
            color=const.AQUA
        elif level==3:
            txt='Souleaters'
            color=const.PINK
        elif level==4:
            txt='EVILBOSS'
            color=const.RED


        draw_text(txt,font,color,const.SCREEN_WIDTH/2-120, 15)
        draw_text(" LEVEL:"+str(level)+" ", font,
                const.WHITE, const.SCREEN_WIDTH/2+70, 15)

    # show score
    draw_text(f"X{player.score}", font, const.WHITE,
            const.SCREEN_WIDTH-100, 15)
    if level==5:
        draw_text('YOU WIN',font,const.WHITE,const.SCREEN_WIDTH/2-180, 15)





class DamageText(pygame.sprite.Sprite):
    # damage text class
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # move damage text up, (y coordinate increases down the screen)
        self.rect.y -= 1
        # delete the damage text after a few miliseconds
        self.counter += 1
        if self.counter >= 30:
            self.kill()


class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  # whole screen fade
            pygame.draw.rect(screen, self.colour,
                             (0-self.fade_counter, 0, const.SCREEN_WIDTH//2,
                              const.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour,
                             ((const.SCREEN_WIDTH)//2+self.fade_counter, 0, const.SCREEN_WIDTH,
                              const.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour,
                             (0, 0-self.fade_counter, const.SCREEN_WIDTH,
                              const.SCREEN_HEIGHT//2))
            pygame.draw.rect(screen, self.colour,
                             (0, (const.SCREEN_HEIGHT)//2+self.fade_counter, const.SCREEN_WIDTH,
                              const.SCREEN_HEIGHT))
        elif self.direction == 2:  # vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0,
                             const.SCREEN_WIDTH, 0+self.fade_counter))

        if self.fade_counter >= const.SCREEN_WIDTH:
            fade_complete = True

        return fade_complete


def pause_game():
    run=True
    while run:
        resume_button = Button(const.SCREEN_WIDTH//2-112,
                        const.SCREEN_HEIGHT//2 - 150, resume_img)
        exit_button = Button(const.SCREEN_WIDTH//2-110,
                                const.SCREEN_HEIGHT//2 + 50, exit_img)
        screen.fill(const.MENU_BG)
        screen.blit(BG,(0,0))

        if resume_button.draw(screen):
            return
        if exit_button.draw(screen):
            #run=False
            return False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #run = False
                return False
        pygame.display.update()


def main_game(mob_animations,main_player):
    screen.fill(const.BG)

    level=2
    start_intro = True

    # define player movement variables
    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False

    # function to reset level
    def reset_level():
        damage_text_group.empty()
        arrow_group.empty()
        item_group.empty()
        fireball_group.empty()

        # create empty tile list
        data = []
        for row in range(const.ROWS):
            r = [-1]*const.COLS
            data.append(r)
        return data
    
    # create empty tile list
    world_data = []
    for row in range(const.ROWS):
        r = [-1]*const.COLS
        world_data.append(r)
    # load in level data and create world
    with open(f"levels/level{level}_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    world = World()
    world.process_data(world_data, tile_list, item_images, mob_animations)

    # create player
    player = world.player
    # create player's weapon
    if main_player=='elf':
        weapon = Weapon(bow_img, arrow_img)
    else:
        weapon=Weapon(staff_img,spear_img)

    # extract enemy from world data
    enemy_list = world.character_list

    # create sprite groups
    damage_text_group = pygame.sprite.Group()
    arrow_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    fireball_group = pygame.sprite.Group()

    score_coin = Item(const.SCREEN_WIDTH-115, 23, 0, coin_images, True)
    item_group.add(score_coin)

    # add the items from level data
    for item in world.item_list:
        item_group.add(item)

    # create screen fade
    intro_fade = ScreenFade(1, const.BLACK, 4)
    death_fade = ScreenFade(2, const.PINK, 4)

    run=True
    while run:
        restart_button = Button(const.SCREEN_WIDTH//2-170,
                        const.SCREEN_HEIGHT//2 - 50, restart_img)
        screen.fill(const.BG)
        # control frame rate
        clock.tick(const.FPS)
        
        if player.alive:
            # calculate player movement
            dx = 0
            dy = 0
            '''since top left corner of game screen is (0,0) while going down, y coordinate 
            increases and while going up it decreases because if this wasnt the case 
            then coordinate will go out of the screen.'''
            if moving_right:
                dx = const.SPEED
            if moving_left:
                dx = -const.SPEED
            if moving_down:
                dy = const.SPEED
            if moving_up:
                dy = -const.SPEED

            # move player
            screen_scroll, level_complete = player.move(
                dx, dy, world.obstacle_tiles, world.exit_tile)

            # update all objects
            world.update(screen_scroll)
            for enemy in enemy_list:
                fireball = enemy.ai(player, world.obstacle_tiles,
                                    screen_scroll, fireball_img)
                if fireball:
                    fireball_group.add(fireball)
                if enemy.alive:
                    enemy.update()
                else:
                    enemy_list.remove(enemy)
            player.update()
            arrow = weapon.update(player)
            if arrow:
                arrow_group.add(arrow)
                shot_fx.play()
            for arrow in arrow_group:
                damage, damage_pos = arrow.update(
                    screen_scroll, world.obstacle_tiles, enemy_list)
                if damage:  # damage has some value other than 0, damage_pos.y hasnt been centered to keep the damage text above enemys head
                    damage_text = DamageText(
                        damage_pos.centerx, damage_pos.y, str(damage), const.RED)
                    damage_text_group.add(damage_text)
                    hit_fx.play()
            damage_text_group.update()
            fireball_group.update(screen_scroll, player)
            item_group.update(screen_scroll, player, coin_fx, heal_fx)

        # draw player on screen
        world.draw(screen)
        for enemy in enemy_list:
            enemy.draw(screen)
        player.draw(screen)
        weapon.draw(screen)
        for arrow in arrow_group:
            arrow.draw(screen)
        for fireball in fireball_group:
            fireball.draw(screen)
        damage_text_group.draw(screen)
        item_group.draw(screen)
        draw_info(player,level)
        score_coin.draw(screen)

        # check level complete
        if level_complete == True and len(enemy_list)==0:
            start_intro = True
            level += 1
            world_data = reset_level()
            # load in level data and create world
            with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world = World()
            world.process_data(world_data, tile_list,
                            item_images, mob_animations)
            temp_hp = player.health
            temp_score = player.score
            player = world.player
            player.health = temp_hp
            player.score = temp_score
            enemy_list = world.character_list
            score_coin = Item(const.SCREEN_WIDTH-115,
                            23, 0, coin_images, True)
            item_group.add(score_coin)
            # add the items from level data
            for item in world.item_list:
                item_group.add(item)
        elif level_complete == True and len(enemy_list)!=0:
            screen.blit(text_img,(130,200))



        # show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        # show death screen
        if player.alive == False:
            pygame.mixer.music.stop()
            player_ded_fx.play()
            if death_fade.fade():
                player_ded_fx.stop()
                if restart_button.draw(screen):
                    pygame.mixer.music.play(-1, 0.0, 5000)
                    death_fade.fade_counter = 0
                    start_intro = True
                    world_data = reset_level()
                    # load in level data and create world
                    with open(f"levels/level{level}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    world.process_data(world_data, tile_list,
                                    item_images, mob_animations)
                    player = world.player
                    enemy_list = world.character_list
                    score_coin = Item(const.SCREEN_WIDTH-115,
                                    23, 0, coin_images, True)
                    item_group.add(score_coin)
                    # add the items from level data
                    for item in world.item_list:
                        item_group.add(item)


        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return
            # take keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w:
                    moving_up = True
                if event.key == pygame.K_s:
                    moving_down = True
                if event.key == pygame.K_ESCAPE:
                    status=pause_game()
                    if status==False:
                        return 
                    

            # keyboard buttons released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_s:
                    moving_down = False

        pygame.display.update()
    pygame.quit()


def selection_menu():
    player=None
    run = True
    while run:
        screen.fill(const.MENU_BG)
        screen.blit(BG,(0,0))
        draw_text("CHOOSE YOUR PLAYER", font,const.WHITE, const.SCREEN_WIDTH//2 - 180, 90)
        draw_text("Elf", font,const.WHITE, const.SCREEN_WIDTH//2 + 160, const.SCREEN_HEIGHT//2-60)
        draw_text("Wizard", font,const.WHITE, const.SCREEN_WIDTH//2 - 215, const.SCREEN_HEIGHT//2-60)
        wizard_button=Button(const.SCREEN_WIDTH//2 - 230,const.SCREEN_HEIGHT//2-70,img1)
        elf_button=Button(const.SCREEN_WIDTH//2 + 110,const.SCREEN_HEIGHT//2-70,img2)
        if wizard_button.draw(screen):
            player='wizard'
            load_mobs_images(player)
            return
        elif elf_button.draw(screen):
            player='elf'
            load_mobs_images(player)
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


# main game loop
def main_menu():
    run = True
    while run:
        screen.blit(BG,(0,0))
        start_button = Button(const.SCREEN_WIDTH//2-130,
                      const.SCREEN_HEIGHT//2 - 150, start_img)
        exit_button = Button(const.SCREEN_WIDTH//2-110,
                            const.SCREEN_HEIGHT//2 + 50, exit_img)

        if exit_button.draw(screen):
            run = False
        if start_button.draw(screen):
            selection_menu()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

        pygame.display.update()
            
main_menu()