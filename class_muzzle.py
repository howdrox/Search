import tkinter as tk
from main import Game
from main import Person

class muzzle(Game,Person):
    def __init__(self):
        
        # self.game = game
        # self.person = Person
        self.j_muzzle = 0
        self.i_muzzle = 0
        self.pi,self.pj = Person.j, Person.i
        self.move_muzzle()
    '''
    AttributeError: type object 'Person' has no attribute 'j' ??????????????????????????????????????????????????????????????
    '''

    def create_muzzle(self):
        Game.muzzle = Game.c.create_oval(0,0,0,0,fill='yellow', edge = None)#initialise

    def key_muzzle(self,k):
        if k in ("Up", "w"):
            self.j_muzzle = -1
        elif k in ("Left", "a"):
            self.i_muzzle = -1
        elif k in ("Down", "s"):
            self.j_muzzle = 1
        elif k in ("Right", "d"):
            self.i_muzzle = 1    
    
    def check_muzzle(self, j_test, i_test):#just for beauty
        # return self.person.check_movement(self,j_test, i_test)
        return (
            0 <= j_test < self.game.height
            and 0 <= i_test < self.game.width
            and not self.game.board.walls[j_test, i_test]
        )
    
    # def update(self):
    #     self.j_muzzle = 0
    #     self.i_muzzle = 0

    def move_muzzle(self):
        
        i_muzzle_test = self.pi + self.i_muzzle
        j_muzzle_test = self.pj + self.j_muzzle
        if self.check_muzzle(j_muzzle_test, i_muzzle_test):
            r_size = self.game.r_size
            x= i_muzzle_test * r_size
            y= j_muzzle_test * r_size
            self.game.c.coords(self.game.c.muzzle,(x+0.42*r_size,y+0.42*r_size
                                   ,x+0.58*r_size,y+0.58*r_size))

        # self.update()


'''
Need add to Person:
__init__:
self.muzzle = muzzle()
self.c_muzzle.create_muzzle()      

def run_muzzle(self):
    self.root.bind(
            "<KeyPress>", lambda f: self.c_muzzle.move_muzzle(f.keysym)

'''

