import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mr. Park's Grand Adventure")

background_img = pygame.image.load('./images/background.jpg').convert_alpha()
stage_1_img = pygame.image.load('./images/background2.jpg').convert_alpha()

player_img = pygame.image.load('./images/player.jpg').convert_alpha()
enemy_img = pygame.image.load('./images/enemy.png').convert_alpha()

win_img = pygame.image.load('./images/win.png').convert_alpha()
lose_img = pygame.image.load('./images/lose.jpg').convert_alpha()

inventory_img = pygame.image.load('./images/inventory.jpg').convert_alpha()

font = pygame.font.SysFont("Times New Roman", 40)
text_color = (255, 255, 255)

def draw_text(text, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def draw_background():
    screen.blit(background_img, (0, 0))

def draw_stage_1():
    screen.blit(stage_1_img, (0, 0))

def draw_win_img():
    screen.blit(win_img, (150,0))

def draw_lose_img():
    screen.blit(lose_img,(0,0))

def draw_inventory_img():
    screen.blit(inventory_img,(0,0))

class Character:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.equipped_weapon = None

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def attack_target(self, target):
        if self.equipped_weapon:
            damage = random.randint(1, self.equipped_weapon.attack)
        else:
            damage = random.randint(1, self.attack)
        target.take_damage(damage)

class Weapon:
    def __init__(self, name, attack):
        self.name = name
        self.attack = attack

# Define the items in the gacha
weapons = [Weapon("old stick", 5), Weapon("new stick", 10), Weapon("god stick", 20)]

# Define a function to simulate a gacha pull
def gacha_pull():
    return random.choice(weapons)

player = Character("Player", 100, 1)
enemy = Character("Enemy", 50, 25)

run = True
fight = False
game_over = False
inventory = []

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not fight:
                fight = True
            elif event.key == pygame.K_a and fight:
                player.attack_target(enemy)
                enemy.attack_target(player)
                pygame.display.update()
            elif event.key == pygame.K_g:
                pulled_item = gacha_pull()
                inventory.append(pulled_item)
            elif event.key == pygame.K_e:
                screen.fill((0,0,0))
                draw_inventory_img()
                if inventory:
                    for i, item in enumerate(inventory):
                        print(f"{i+1}. {item.name}")
                    equip_num = int(input("Enter the number: ")) - 1
                    if 0 <= equip_num < len(inventory):
                        player.equipped_weapon = inventory[equip_num]
                        print(f"You equipped the {player.equipped_weapon.name}!")
                    else:
                        print("Invalid input. Please try again.")
            elif event.key == pygame.K_r and game_over:
                player.hp = 100
                enemy.hp = 50
                fight = False
                game_over = False
                inventory = []
                player.equipped_weapon = None

    if not fight:
        screen.fill((0,0,0))  # clear the screen
        draw_background()
        draw_text("Press Space to Start", 340, 225)
        draw_text("a to attack", 400, 300)
        draw_text("g to pull from gacha", 400, 350)
        draw_text("e for inventory", 400, 400)
    elif fight and not game_over:
        screen.fill((0,0,0))  # clear the screen
        draw_stage_1()
        screen.blit(player_img, (100, 200))  # draw player character
        screen.blit(enemy_img, (700, 200))  # draw enemy character
        draw_text(f"Player HP: {player.hp}", 10, 10)
        draw_text(f"Enemy HP: {enemy.hp}", 750, 10)
        if not player.is_alive():
            game_over = True
        elif not enemy.is_alive():
            game_over = True
    else:
        if not player.is_alive():
            screen.fill((0,0,0))  # clear the screen
            draw_lose_img()
            draw_text("Game Over", 290, 150)
            draw_text("Press R to restart", 290, 200)
        elif not enemy.is_alive():
            screen.fill((0,0,0))  # clear the screen
            draw_win_img()
            draw_text("You Win!", 290, 150)
            draw_text("Press R to restart", 290, 200)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()