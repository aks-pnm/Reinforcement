from random import *
from Tkinter import *
import time

#Define the grid size
gridX = 5
gridY = 5

root = Tk()
floorImage = PhotoImage(file='./Resources/Image.gif')
cheeseImage = PhotoImage(file='./Resources/cheese.gif')
mouseImage = PhotoImage(file='./Resources/mouse.gif')
labels = []
qvalue = {}

class Qlearning:

    #Update the initial values using init function, similar to constructor
    def __init__(self):
        self.actions=['N','S','E','W']
        self.alpha = 0.2
        self.gamma=0.9
        self.beta=0.1

    #return the Qvalue from the dictionary based on the (state,action) pair
    def getQvalue(self,state,action):
        qv=qvalue.get((state,action),0.0)
        #print 'qvalue:',qv
        return qv

    #Qvalue(St,At)= Qvalue(St,At) + alpha*[reward + gamma* maxQ(St+1,A)- Qvalue(St,At)]
    #gamma= Discount_factor
    #alpha= Learning rate

    def Qlearing(self,prevstate,prevaction,reward,futureOptvalue):
        prevvalue=qvalue.get((prevstate, prevaction), None)
        #print('Qvalue-learn',qvalue.get((prevstate, prevaction), None))
        if (prevvalue is None):
          #print 'pair1:', (prevstate,prevaction)
          qvalue[(prevstate,prevaction)]=reward
        else:
          #print 'pair2:', (prevstate, prevaction)
          qvalue[(prevstate,prevaction)]=prevvalue + self.alpha * (reward + (futureOptvalue-prevvalue))


    #pick_action returns the next action the agent has to take based on the Qvalue obtained
    #Beta value helps to avoid local optimum
    def pick_action(self,state):
        if random() < self.beta:
            selectaction = choice(self.actions)
            #print 'selectaction1:',selectaction
            return selectaction
        else:
            qv = [self.getQvalue(state, act) for act in self.actions]
            maxvalue = max(qv)
            #print '^^print action'
            #print 'maxvalue:',maxvalue
            total_count = qv.count(maxvalue)
            #print 'total_count',total_count

            if(total_count>1):
                pickone=[i for i in range(4) if(qv[i] == maxvalue)]
                #print 'pickone:',pickone
                pickIndex=choice(pickone)
                selectaction = self.actions[pickIndex]
                return selectaction
            else:
                pickIndex=qv.index(maxvalue)
                #print 'pickIndex:',pickIndex
                selectaction = self.actions[pickIndex]
                return selectaction

        #print 'selectaction2:', selectaction
        return selectaction

    #start of the algorithm call
    def learn(self, prevstate, action, reward, futurestate):
        #print 'Inside learn'
        values=[]
        maxqvalue = max([self.getQvalue(futurestate, a) for a in self.actions])
        #print '^^Maxvalue'
        self.Qlearing(prevstate, action, reward, reward + self.gamma*maxqvalue)

def makeGrid(row, column):
    for i in xrange(gridX):
        labels.append([])
        for j in xrange(gridY):
            labels[i].append(Label(root, image=floorImage, borderwidth=1))
            labels[i][j].grid(row=i, column=j)


def setCheeseInitialState(wall):

    cheeseX = randrange(gridX)
    cheeseY = randrange(gridY)
    if [cheeseX,cheeseY] in wall:
        while [cheeseX,cheeseY] in wall:
            cheeseX = randrange(gridX)
            cheeseY = randrange(gridY)
    labels[cheeseX][cheeseY].configure(image=cheeseImage)
    return cheeseX,cheeseY


def setMouseInitialState(wall):
    mouseX = randrange(gridX)
    mouseY = randrange(gridY)
    if [mouseX,mouseY] in wall:
        while [mouseX,mouseY] in wall:
            mouseX = randrange(gridX)
            mouseY = randrange(gridY)

    labels[mouseX][mouseY].configure(image=mouseImage)
    return mouseX,mouseY

def updateGrid(cheeseX,cheeseY,mouseX,mouseY):
    labels[cheeseX][cheeseY].configure(image=cheeseImage)
    labels[mouseX][mouseY].configure(image=mouseImage)

def runFormula (cheeseX,cheeseY,mouseX,mouseY,S, A,wall,RL):
    global reward
    reward = -1
    done = 0
    position = tuple([mouseX,mouseY])

    if cheeseX == mouseX:
        if cheeseY == mouseY:
            reward = 100
            done = 2
            if S is not None:
                RL.learn(S, A, reward, position)

        return mouseX,mouseY,done,S,A

    if [mouseX,mouseY] in wall:
        reward = -500
        done = 1
        if S is not None:
            RL.learn(S, A, reward, position)
        return mouseX, mouseY, done, S, A

    if S is not None:
        #print 'inside prev comparision'
        RL.learn(S, A, reward,position)
    #print RL

    action = RL.pick_action(position)

    S = position
    A = action

    if action == 'N':
        mouseY -= 1

    if action == 'E':
        mouseX += 1

    if action == 'W':
        mouseX -= 1

    if action == 'S':
        mouseY += 1

    time.sleep(0.1)
    return mouseX,mouseY,done,S,A

def border(gridX,gridY):
    arr = []
    for i in range(gridX):
        for j in range(gridY):
            if i == 0:
                x = [i,j]
                arr.append(x)
            elif i == gridX-1:
                x = [i,j]
                arr.append(x)
            else:
                if j == 0 or j == gridY -1:
                    x = [i,j]
                    arr.append(x)

    return arr



def main():
    makeGrid(gridX,gridY)
    wall = border(gridX,gridY)
    RL = Qlearning()
    global prevS
    global prevA
    cheeseX, cheeseY = setCheeseInitialState(wall)
    for z in range(150):
        mouseX, mouseY = setMouseInitialState(wall)
        prevS = None
        prevA = None
        #print 'Initial states:',mouseX,mouseY
        for x in range(250):
            #print 'Iteration:',x,'x,y,done:',mouseX, mouseY, done
            #print prevS, prevA
            mouseX, mouseY, done, prevS, prevA = runFormula(cheeseX, cheeseY, mouseX, mouseY, prevS, prevA, wall, RL)
            if done == 2:
                print 'Done in ', x, 'iterations'
                break
            if done == 1:
                print 'In the pit in', x, 'iterations'
                break
            if [mouseX,mouseY] not in wall:
                updateGrid(cheeseX,cheeseY,mouseX,mouseY)

    root.mainloop()


if __name__ == "__main__" :
    main()
