import pygame
import math
import random

__windowWidth__ = 1280
__windowHeight__ = 720
__gridPXWidth__ = 20
__gridPXHeight__ = 20
gridWidth = __windowWidth__//__gridPXWidth__
gridHeight = __windowHeight__//__gridPXHeight__






def runGame():
    snake = Snake()
    fruit = Fruit()
    pygame.init()
    _screen = pygame.display.set_mode((__windowWidth__,__windowHeight__))
    _clock = pygame.time.Clock()
    running = True
    while(running):
        drawGrid(_screen)
        snake.drawSnake(_screen)
        fruit.draw(_screen)
        fruit.check(snake)
        if(snake.checkFailure()):
            running = False
        pygame.display.flip()
        _clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake.changeDirection(directions.left)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake.changeDirection(directions.right)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake.changeDirection(directions.up)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake.changeDirection(directions.down)


def drawGrid(screen:pygame.surface):
    screen.fill("black")
    
    for x in range(1,(gridWidth)):
        pygame.draw.line(screen,(255,255,255),(__gridPXWidth__*x,0),(__gridPXWidth__*x,__windowHeight__),1)
    for y in range(1,(gridHeight)):
        pygame.draw.line(screen,(255,255,255),(0,__gridPXHeight__*y),(__windowWidth__,__gridPXHeight__*y),1)

class directions:
        up = 0
        right = 1
        down = 2
        left = 3


class Snake:
    bodyPositions_ = [(10,10,directions.up),(10,11,directions.up),(10,12,directions.up),(10,13,directions.up),(10,14,directions.up)] # array of tuples (x,y, direction)
    def changeDirection(self,direction:int):
        self.bodyPositions_[0] = (self.bodyPositions_[0][0],self.bodyPositions_[0][1],direction)
    def UpdateSnake(self,screen:pygame.surface,gridHeight:int,gridWidth:int):
        for i in range(len(self.bodyPositions_)):
            match(self.bodyPositions_[i][2]):
                case directions.up:
                    self.bodyPositions_[i] = (self.bodyPositions_[i][0],self.bodyPositions_[i][1] - 1,self.bodyPositions_[i][2])
                case directions.right:
                    self.bodyPositions_[i] = (self.bodyPositions_[i][0] + 1,self.bodyPositions_[i][1],self.bodyPositions_[i][2])
                case directions.down:
                    self.bodyPositions_[i] = (self.bodyPositions_[i][0],self.bodyPositions_[i][1] + 1,self.bodyPositions_[i][2])
                case directions.left:
                    self.bodyPositions_[i] = (self.bodyPositions_[i][0] - 1,self.bodyPositions_[i][1],self.bodyPositions_[i][2])
            
            if(self.bodyPositions_[i][1] <= 0):
                self.bodyPositions_[i] = (self.bodyPositions_[i][0],0,self.bodyPositions_[i][2])
            elif(self.bodyPositions_[i][0] <= 0):
                self.bodyPositions_[i] = (0,self.bodyPositions_[i][1],self.bodyPositions_[i][2])
            elif(self.bodyPositions_[i][1] >= gridHeight):
                self.bodyPositions_[i] = (self.bodyPositions_[i][0],gridHeight,self.bodyPositions_[i][2])
            elif(self.bodyPositions_[i][0] >= gridWidth):
                self.bodyPositions_[i] = (gridWidth,self.bodyPositions_[i][1],self.bodyPositions_[i][2])
            
            if(i != 0):
                temp = ((self.bodyPositions_[i][0] -self.bodyPositions_[i-1][0]),(self.bodyPositions_[i][1] -self.bodyPositions_[i-1][1]))
                match temp:
                    case (0,1):
                        tempdir = directions.up
                    case (1,0):
                        tempdir = directions.left
                    case (0,-1):
                        tempdir = directions.down
                    case (-1,0):
                        tempdir = directions.right
                    case _:
                        tempdir = self.bodyPositions_[i-1][2]
                self.bodyPositions_[i] = (self.bodyPositions_[i][0],self.bodyPositions_[i][1],tempdir)
            
    def checkFailure(self):
        temp = []
        for pos in self.bodyPositions_:     
            if (pos[0],pos[1]) in temp:
                return True
            else:
                temp.append((pos[0],pos[1]))
        return False
    def drawSnake(self, screen:pygame.surface):
        self.UpdateSnake(screen,gridHeight,gridWidth)
        for body in self.bodyPositions_:
            pygame.draw.rect(screen,(0,255,0),pygame.Rect(body[0]*__gridPXWidth__,body[1]*__gridPXHeight__,__gridPXWidth__ + 1,__gridPXHeight__ + 1))
        
    
class Fruit:
    Position:tuple[int,int] = (gridWidth//2,gridHeight//2)
    def draw(self,screen:pygame.surface):
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(self.Position[0]*__gridPXWidth__,self.Position[1]*__gridPXHeight__,__gridPXWidth__ + 1,__gridPXHeight__ + 1))
    def randomize(self):
        self.Position = (random.randint(0,gridWidth),random.randint(0,gridHeight))
    def check(self,snake:Snake):
        if(snake.bodyPositions_[0][0] == self.Position[0] and snake.bodyPositions_[0][1] == self.Position[1]):
            self.collected(snake)
            flag = True
            while(flag):
                self.randomize()
                flag = False
                for pos in snake.bodyPositions_:
                    if pos[0] == self.Position[0] and pos[1] == self.Position[1]:
                        Flag = True
    def collected(self,snake:Snake):
        match(snake.bodyPositions_[-1][2]):
            case directions.up:
                snake.bodyPositions_.append((snake.bodyPositions_[-1][0],snake.bodyPositions_[-1][1] + 1, directions.up))
            case directions.down:
                snake.bodyPositions_.append((snake.bodyPositions_[-1][0],snake.bodyPositions_[-1][1] - 1, directions.down))
            case directions.left:
                snake.bodyPositions_.append((snake.bodyPositions_[-1][0] + 1,snake.bodyPositions_[-1][1], directions.left))
            case directions.right:
                snake.bodyPositions_.append((snake.bodyPositions_[-1][0] - 1,snake.bodyPositions_[-1][1], directions.right))

    
    
runGame()
