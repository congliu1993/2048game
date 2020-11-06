import pygame
from game2048.setting import GameSet
import game2048.gamemethod as gm

def start_game():
    pygame.init()
    settings=GameSet()
    screen = pygame.display.set_mode((settings.width, settings.height))
    areas=[]
    pygame.display.set_caption("2048")
    gm.refresh_area(areas, settings, screen)
    allarea=gm.all_area(settings,screen)
    while True:
        gm.check_event(allarea,areas,settings,screen)
        gm.print_screen(screen,areas)
start_game()