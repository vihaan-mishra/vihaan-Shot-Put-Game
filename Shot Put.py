#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
import random

class GUIDie(Canvas):
    '''6-sided Die class for GUI'''

    def __init__(self,master,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self,master,width=60,height=60,bg='white',\
                        bd=5,relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top-1]
    
    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1,7)
        self.draw()

    def draw(self):
        '''GUIDie.draw()
        draws the pips on the die'''
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [[(1,1)],
                   [(0,0),(2,2)],
                   [(0,0),(1,1),(2,2)],
                   [(0,0),(0,2),(2,0),(2,2)],
                   [(0,0),(0,2),(1,1),(2,0),(2,2)],
                   [(0,0),(0,2),(1,0),(1,2),(2,0),(2,2)]]
        for location in pipList[self.top-1]:
            self.draw_pip(location,self.colorList[self.top-1])

    def draw_pip(self,location,color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx,centery) = (17+20*location[1],17+20*location[0])  # center
        self.create_oval(centerx-5,centery-5,centerx+5,centery+5,fill=color)
        
    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)

class DecathShotPutFrame(Frame):
    '''frame for a game of ShotPut'''

    def __init__(self,master,name):
        '''Decath1500MFrame(master,name) -> DecathShotPutFrame
        creates a new ShotPut frame
        name is the name of the player'''
        # set up Frame object
        Frame.__init__(self,master)
        self.grid()
        # label for player's name
        Label(self,text=name,font=('Arial',18)).grid(columnspan=3,sticky=W)
        # set up score
        self.scoreLabel = Label(self, text='Score: 0', font=('Arial',15))
        self.scoreLabel.grid(row=0,column=2,columnspan=1)
        self.attemptLabel = Label(self, text='Attempt: 1',font=('Arial',15))
        self.attemptLabel.grid(row=0,column=3,columnspan=2,sticky=W)
        self.highscoreLabel = Label(self,text='Highscore: 0',font=('Arial',18))
        self.highscoreLabel.grid(row=0,column=5,columnspan=3,sticky=E)
        self.gameoverLabel = Label(self,text='Game Over', font=('Arial',18))
        self.foulLabel = Label(self,text='FOULED ATTEMPT', font=('Arial',12))
        
        # initialize game data
        self.score = 0
        self.attempt = 1
        self.highscore = 0
        self.gameround = 0
        # set up dice
        self.dice = []
        for n in range(8):
            self.dice.append(GUIDie(self,[1,2,3,4,5,6],['red']+['black']*5))
            self.dice[n].grid(row=1,column=n)
        # set up buttons
        self.rollButton = Button(self,text='Roll',command=self.roll)
        self.rollButton.grid(row=2)
        self.stopButton = Button(self,text='Stop',command=self.stop)
        self.stopButton.grid(row=3)

    def roll(self):
        '''DecathShotPutFrame.roll()
        handler method for the roll button click'''
        # roll one die
        self.dice[self.gameround].roll()
        value = self.dice[self.gameround].get_top()
        if value == 1:
            self.rollButton['state'] = DISABLED
            self.stopButton['text'] = 'FOUL'
            self.stopButton['state'] = ACTIVE
            self.score = 0
            self.scoreLabel['text'] = 'Score: '+ str(self.score)
            self.highscore = max(self.highscore, self.score)
            
            self.scoreLabel.grid_remove()
            
            self.attemptLabel.grid_remove()
            
            self.foulLabel.grid(row=0,column=2,columnspan=4)
            
        else:        
            self.score += self.dice[self.gameround].get_top()
            self.scoreLabel['text'] = 'Score: '+ str(self.score)
            self.gameround += 1  # go to next round
            if self.gameround < 8:  # move buttons to next die
                self.rollButton.grid(row=2,column=self.gameround)
                self.rollButton['state'] = ACTIVE
                self.stopButton.grid(row=3,column=self.gameround)
                self.stopButton['state'] = ACTIVE

    def stop(self):
        '''DecathShotPutFrame.keep()
        handler method for the keep button click'''
        # add dice to score and update the scoreboard
        if self.attempt == 3:
            self.rollButton.grid(row=2,column=self.gameround)
            self.rollButton['state'] = DISABLED
            self.stopButton.grid(row=3,column=self.gameround)
            self.stopButton['text'] = 'Stop'
            self.stopButton['state'] = DISABLED
            self.highscore = max(self.highscore, self.score)
            self.highscoreLabel['text'] = 'Highscore: ' + str(self.highscore)
            
            self.scoreLabel.grid_remove()
            
            self.attemptLabel.grid_remove()
            
            self.foulLabel.grid_remove()
            
            self.gameoverLabel = Label(self,text='Game Over', font=('Arial',18))
            
            self.gameoverLabel.grid(row=0,column=3,columnspan=2)
            
        else:
            
            self.foulLabel.grid_remove()
            
            self.scoreLabel = Label(self, text='Score: 0', font=('Arial',15))
            
            self.scoreLabel.grid(row=0,column=2,columnspan=1)
            
            self.attemptLabel = Label(self, text='Attempt: 1',font=('Arial',15))
            
            self.attemptLabel.grid(row=0,column=3,columnspan=2,sticky=W)
            
            
            self.attempt += 1
            self.attemptLabel['text'] = 'Attempt: ' + str(self.attempt)
            
            self.highscore = max(self.highscore, self.score)
            self.highscoreLabel['text'] = 'Highscore: ' + str(self.highscore)
            
            self.score = 0
            self.scoreLabel['text'] = 'Score: '+ str(self.score)
            
            self.gameround = 0
            self.rollButton.grid(row=2,column=self.gameround)
            self.rollButton['state'] = ACTIVE
            self.stopButton.grid(row=3,column=self.gameround)
            self.stopButton['text'] = 'Stop'
            self.stopButton['state'] = ACTIVE
            
        for i in range(len(self.dice)):
            self.dice[i].erase()
            
# play the game
name = input("Enter your name: ")
root = Tk()
root.title('ShotPut')
game = DecathShotPutFrame(root,name)
game.mainloop()

'''
GUI as is

ShotPut Class:
    Create:
        6 dice
        Name in top left
        High score in top right
        Attempt and Score in middle (3 attempts max)
        Add possible scores to dice [1, 2, 3, 4, 5, 6]
        Buttons below dice:
            Roll gives random number from list (unlimited)
            Stop resets the die and sums numbers on die to score and then see if it is highscore
            Stop --> Foul button if 1 is rolled
        Erase tool that resets when foul rolled
Way to get numbers on dice, add together and store value. Update highscore. If score greater than highscore: highscore equal to score

'''

