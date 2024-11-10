import pygame
import math
import random
import asyncio

__windowWidth__ = 20
__windowHeight__ = 20
__gridPXWidth__ = 2
__gridPXHeight__ = 2

__upSizeFactor__ = 20

gridWidth = __windowWidth__//__gridPXWidth__
gridHeight = __windowHeight__//__gridPXHeight__


class directions:
        up = 0
        right = 1
        down = 2
        left = 3


class Snake:
    bodyPositions_ = [(gridWidth/2,gridHeight/2,directions.up),(gridWidth/2,gridHeight/2 + 1,directions.up),(gridWidth/2,gridHeight/2 + 2,directions.up),(gridWidth/2,gridHeight/2 + 3,directions.up),(gridWidth/2,gridHeight/2 + 4,directions.up)] # array of tuples (x,y, direction)
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
            pygame.draw.rect(screen,(0,255,0),pygame.Rect(body[0]*__gridPXWidth__*__upSizeFactor__,body[1]*__upSizeFactor__*__gridPXHeight__,__gridPXWidth__*__upSizeFactor__ + 1,__gridPXHeight__*__upSizeFactor__ + 1))
        
    
class Fruit:
    Position:tuple[int,int] = (-1,-1)
    def draw(self,screen:pygame.surface):
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(self.Position[0]*__gridPXWidth__*__upSizeFactor__,self.Position[1]*__gridPXHeight__*__upSizeFactor__,__gridPXWidth__*__upSizeFactor__ + 1,__gridPXHeight__*__upSizeFactor__ + 1))
    def randomize(self):
        self.Position = (random.randint(1,gridWidth - 2),random.randint(1,gridHeight - 2))
    def check(self,snake:Snake):
        if(self.Position== (-1,-1)):
            self.randomize()
        if(snake.bodyPositions_[0][0] == self.Position[0] and snake.bodyPositions_[0][1] == self.Position[1]):
            self.collected(snake)
            flag1 = True
            while(flag1):
                self.randomize()
                flag2 = False
                for pos in snake.bodyPositions_:
                    if abs(pos[0] - self.Position[0]) < 1 and abs(pos[1] - self.Position[1]) < 1:
                        flag2 = True
                if flag2 == False:
                    flag1 = False
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


class neuron:
    inputs:list
    weight:float = 0
    bias:float = 0
    output:float
    def __init__(self,inputs:list,Initweight:float,Initbias:float):
        self.inputs = inputs
        self.weight = random.randrange(0,10)
        self.bias = random.randrange(0,10)
        random.seed(random.random())
    
    def updateOutput(self,inputs:list[float]):
        Toutput = 0
        for i in range(len(self.inputs)):
            Toutput += self.inputs[i].output
        self.output = 1 / (1 + math.exp( 0 - Toutput))

class inputNeuron(neuron):
    index:int
    def updateOutput(self,inputs:list[float]):
        self.inputs = inputs
        self.output = self.inputs[self.index]
    
    def __init__(self, inputs:list, Initweight:float, Initbias:float, index:int):
        super().__init__(inputs, Initweight, Initbias)
        self.index = index

class layer:
    size:int
    neurons:list[neuron]
    layerList:list
    
    def __init__(self,size:int,index,input:list,layerList:list):
        self.size = size
        self.layerList = layerList
        self.neurons = []
        if(index == 0):
            for x in range(size):
                self.neurons.append(inputNeuron(input,1,0,x))
        else:
            for x in range(size):
                self.neurons.append(neuron(self.layerList[index - 1].neurons,1,0))
    
    def update(self,inputs:list[float]):
        for neuron in self.neurons:
            neuron.updateOutput(inputs)
    
class network:
    layers:list[layer] = []
    inputs:list[float] = []
    outputs:list[float] = []
    
    def __init__(self,inputNeurons:int,hiddenLayers:int,hiddenLayerNeurons:int,outputNeurons:int):
        self.layers.append(layer(inputNeurons,0,self.inputs,self.layers))
        for x in range(1,hiddenLayers + 1):
            self.layers.append(layer(hiddenLayerNeurons,x,self.inputs,self.layers))
        self.layers.append(layer(outputNeurons,hiddenLayers + 1,self.inputs,self.layers))

    def update(self,inputs:list[float]):
        for layer in self.layers:
            layer.update(inputs)
        tList = []
        for neuron in self.layers[-1].neurons:
            tList.append(neuron.output)
        self.outputs = tList

def updateInputArray(inputList:list[float],fruit:Fruit,snake:Snake):
    for x in range(__windowWidth__):
        for y in range(__windowHeight__):
            inputList[x*__windowWidth__ + y] = 0
    inputList[int(fruit.Position[0]*__windowWidth__ + fruit.Position[1])] = 10
    for bodyPart in snake.bodyPositions_:
        inputList[int(bodyPart[0]*__windowWidth__ + bodyPart[1])] = -10
    inputList[-3] = snake.bodyPositions_[0][0]
    inputList[-2] = snake.bodyPositions_[0][1]
    inputList[-2] = snake.bodyPositions_[0][2]


def runGame():
    snake = Snake()
    fruit = Fruit()
    nn = network((__windowHeight__*__windowWidth__) + 3,5,30,4)
    inputList = []
    for i in range(__windowWidth__*__windowHeight__ + 3):
        inputList.append(0)
    nn.inputs = inputList
    pygame.init()
    _screen = pygame.display.set_mode((__windowWidth__*__upSizeFactor__,__windowHeight__*__upSizeFactor__))
    _clock = pygame.time.Clock()
    running = True
    while(running):
        #drawGrid(_screen)
        _screen.fill("black")
        snake.drawSnake(_screen)
        fruit.draw(_screen)
        fruit.check(snake)
        if(snake.checkFailure()):
            running = False
        updateInputArray(inputList,fruit,snake)
        nn.update(inputList)
        
        temp1 = 0
        temp2 = 0
        for i in range(len(nn.outputs)):
            if nn.outputs[i] >= temp1:
                temp2 = i
        
        match temp2:
            case 0:
                snake.changeDirection(directions.up)
            case 1:
                snake.changeDirection(directions.down)
            case 2:
                snake.changeDirection(directions.left)
            case 3:
                snake.changeDirection(directions.right)
        
        
        pygame.display.flip()
        _clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    return len(snake.bodyPositions_)


async def evaluate(resultList:list):
    resultList.append(runGame())

result = []

for i in range(100):
    asyncio.run(evaluate(result))

print(result)