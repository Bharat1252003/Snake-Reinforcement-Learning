import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init() # initialize all the modules correctly

Point = namedtuple('Point', 'x, y')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

BLOCK_SIZE = 20
SPEED = 60

#rgb colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font('arial.ttf', 25)


class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [
            self.head,
            Point(self.head.x-BLOCK_SIZE, self.head.y),
            Point(self.head.x-BLOCK_SIZE, self.head.y)
        ]
        
        self.score = 0
        self.food = None
        self._place_food() # helper function -  used to assist in providing some functionality, which isn't the main goal of the application or class in which it is used.
        self.frame_iteration = 0

    
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE

        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()
    
    def play_step(self, action):
        self.frame_iteration +=1
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # move snake
        self._move(action)
        self.snake.insert(0, self.head) # not append as it needs to be in the front

        # check game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake): # break if takes too long - time dependent on size of snake
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # place food or move
        if self.head == self.food:
            self.score +=1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # return game over and score

        return reward, game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+2, 12, 12))
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0]) # displaying on the screen
        pygame.display.flip() # updates the window
    
    def _move(self, action):
        # straight - [1, 0, 0]
        # right - [0, 1, 0]
        # left - [0, 0, 1]

        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clockwise[idx] # no change from previous direction
        
        elif np.array_equal(action, [0,1,0]):
            new_idx = (idx+1)%4
            new_dir = clockwise[new_idx]
            
        else:
            new_idx = (idx-1)%4
            new_dir = clockwise[new_idx] # no change from previous direction
        
        self.direction = new_dir                

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        # move to the other end when the snake hits a boundary
        #if x == self.w:
        #    x = 0
        #if x < 0:
        #    x = self.w
        #if y == self.h:
        #    y = 0
        #if y < 0:
        #    y = self.h
        # some error when turning at the edge
        
        self.head = Point(x, y)
    
    def is_collision(self, pt=None):
        if pt == None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        
        # hits itself
        if pt in self.snake[1:]:
            return True
        return False