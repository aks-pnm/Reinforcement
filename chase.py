from random import *
from Tkinter import *
import time
gridX = 10
gridY = 10
root = Tk()
floorImage = PhotoImage(file='./Resources/Image.gif')
cheeseImage = PhotoImage(file='./Resources/cheese.gif')
mouseImage = PhotoImage(file='./Resources/mouse.gif')
labels = []
qvalue={}

class Qlearning:

    def __init__(self):
        self.actions=['N','S','E','W']
        self.alpha = 0.5
        self.gamma=0.1
        self.beta=0.9

    #return the Qvalue from the dictionary based on the (state,action) pair
    def getQvalue(self,state,action):
        qv=qvalue.get((state,action),0.0)
        print 'qvalue:',qv
        return qv

    #Qvalue(St,At)= Qvalue(St,At) + alpha*[reward + gamma* maxQ(St+1,A)- Qvalue(St,At)]
    #gamma= Discount_factor
    #alpha= Learning rate

    def Qlearing(self,prevstate,prevaction,reward,futureOptvalue):
        prevvalue=qvalue.get((prevstate, prevaction), None)
        print('Qvalue-learn',qvalue.get((prevstate, prevaction), None))
        if (prevvalue is None):
          print 'pair1:', (prevstate,prevaction)
          qvalue[(prevstate,prevaction)]=reward
        else:
          print 'pair2:', (prevstate, prevaction)
          qvalue[(prevstate,prevaction)]=prevvalue + self.alpha * (reward + (futureOptvalue-prevvalue))


    #pick_action returns the next action the agent has to take based on the Qvalue obtaened
    #Beta value helps to avoid local optimum
    def pick_action(self,state):
        if random() < self.beta:
            selectaction = choice(self.actions)
            print 'selectaction1:',selectaction
            return selectaction
        else:
            qv = [self.getQvalue(state, act) for act in self.actions]
            maxvalue = max(qv)
            print '^^print action'
            print 'maxvalue:',maxvalue
            total_count = qv.count(maxvalue)
            print 'total_count',total_count

            if(total_count>1):
                pickone=[i for i in range(4) if(qv[i] == maxvalue)]
                print 'pickone:',pickone
                pickIndex=choice(pickone)
                selectaction = self.actions[pickIndex]
                return selectaction
            else:
                pickIndex=qv.index(maxvalue)
                print 'pickIndex:',pickIndex
                selectaction = self.actions[pickIndex]
                return selectaction

        print 'selectaction2:', selectaction
        return selectaction

    #start of the algorithm call
    def learn(self, prevstate, action, reward, futurestate):
        print 'Inside learn'
        values=[]
        maxqvalue = max([self.getQvalue(futurestate, a) for a in self.actions])
        print '^^Maxvalue'
        self.Qlearing(prevstate, action, reward, maxqvalue)

def makeGrid(row, column):
    for i in xrange(gridX):
        labels.append([])
        for j in xrange(gridY):
            labels[i].append(Label(root, image=floorImage, borderwidth=1))
            labels[i][j].grid(row=i, column=j)


def setInitialState():
    cheeseX = randrange(gridX)
    cheeseY = randrange(gridY)
    labels[cheeseX][cheeseY].configure(image=cheeseImage)
    mouseX = randrange(gridX)
    mouseY = randrange(gridY)
    labels[mouseX][mouseY].configure(image=mouseImage)
    return cheeseX,cheeseY,mouseX,mouseY

def updateGrid(cheeseX,cheeseY,mouseX,mouseY):
    labels[cheeseX][cheeseY].configure(image=cheeseImage)
    labels[mouseX][mouseY].configure(image=mouseImage)

def runFormula(cheeseX,cheeseY,mouseX,mouseY,prevS,prevA,wall,RL):
    reward = -1
    done = 0
    position = tuple([mouseX,mouseY])


    if (cheeseX == mouseX) and (cheeseY == mouseY):
        reward = 100
        done = 1
        print 'successful'
        return mouseX,mouseY,done,prevS,prevA

    if [mouseX,mouseY] in wall:
        reward = -100
        done = 1

    if prevS is not None:
        print 'inside prev comparision'
        RL.learn(prevS,prevA,reward,position)
    print RL
    action = RL.pick_action(position)

    prevS = position
    prevA = action

    if(action == 'N'):
        mouseY -= 1

    if(action == 'E'):
        mouseX += 1

    if(action == 'W'):
        mouseX -= 1

    if(action == 'S'):
        mouseY += 1

    return mouseX,mouseY,done,prevS,prevA

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
    done = 0
    prevS = None
    prevA = None
    for z in range(200):
        cheeseX,cheeseY,mouseX,mouseY = setInitialState()
        print 'Initial states:',mouseX,mouseY
        for x in range(500):
            time.sleep(0.2)
            print 'Iteration:',x,'x,y,done:',mouseX, mouseY, done
            mouseX, mouseY, done, prevS, prevA = runFormula(cheeseX,cheeseY,mouseX,mouseY, prevS, prevA,wall,RL)
            if done == 1:
                print 'Done 1'
                break
            if [mouseX,mouseY] not in wall:
                updateGrid(cheeseX,cheeseY,mouseX,mouseY)

    root.mainloop()


if __name__ == "__main__" :
    main()
