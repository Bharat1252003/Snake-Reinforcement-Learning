import pygame

import pygame
pygame.init()
screen = pygame.display.set_mode((400, 400)) #x and y are height and width

while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
         active = False

    pygame.draw.circle(screen, (0,100,200), (100, 100), 50, 10)

    pygame.display.update()
    
