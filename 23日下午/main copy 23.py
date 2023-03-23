import tkinter as tk
import json
import numpy as np
import random


class Game:
    def __init__(self, height, width):
        self.width = width
        self.height = height  # nbr de case
        self.r_size = 20  # pixel par case

        self.create_window()
        self.create_canvas()
        self.board = Board(self)
        self.board.show_walls()
        self.create_entities()
        # for p in self.persons:
        #     p.show()

        self.root.bind("<KeyPress>", lambda e: self.persons[0].key_press(e.keysym)
                       ,lambda f:self.persons[0].key_muzzle(f.keysym))
        self.root.bind("<KeyRelease>", lambda e: self.persons[0].key_release(e.keysym)
                       ,lambda f:self.persons[0].key_muzzle(f.keysym))
        self.root.mainloop()

    def create_window(self):
        self.c_width = self.width * self.r_size
        self.c_height = self.height * self.r_size  # canvas size (in pixel)
        self.root = tk.Tk()
        self.root.geometry(f"{self.c_width + 20}x{self.c_height + 20}")
        self.root.title("Search")

    def create_canvas(self):
        self.c = tk.Canvas(self.root, width=self.c_width, height=self.c_height)
        self.c.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_entities(self):
        self.persons = []
        self.persons.append(Person(self, False, [1, 4]))
        self.persons.append(Person(self, True, [6, 6]))



class Person:
    def __init__(self, game, evil, spawn_coord):
        self.game = game
        self.evil = evil
        self.j, self.i = spawn_coord
        self.speed_x = 0
        self.speed_y = 0
        self.dt = 40
        self.j_muzzle = 0
        self.i_muzzle = 0

        self.show()
        self.move()

    def show(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.shape = self.game.c.create_rectangle(
            x, y, x + r_size, y + r_size, fill="red" if self.evil else "blue"
        )
        self.muzzle = self.game.c.create_oval(10,10,20,20,fill='yellow', edge = None)#initialise

    def update(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.game.c.moveto(self.shape, x - 1, y - 1)
        

    def key_press(self, k):
        if k in ("Up", "w"):
            self.speed_y = -1
        elif k in ("Left", "a"):
            self.speed_x = -1
        elif k in ("Down", "s"):
            self.speed_y = 1
        elif k in ("Right", "d"):
            self.speed_x = 1


    def key_release(self, k):
        if k in ("Up", "w", "Down", "s"):
            self.speed_y = 0
        elif k in ("Left", "a", "Right", "d"):
            self.speed_x = 0
    
    def key_muzzle(self,k):
        if k in ("Up", "w"):
            self.j_muzzle = -2
        elif k in ("Left", "a"):
            self.i_muzzle = -2
        elif k in ("Down", "s"):
            self.j_muzzle = 2
        elif k in ("Right", "d"):
            self.i_muzzle = 2
        


    def move(self):
        i_test = self.i + self.speed_x
        j_test = self.j + self.speed_y
        if self.check_movement(j_test, i_test):
            self.i += self.speed_x
            self.j += self.speed_y 
        
        i_muzzle_test = self.i + self.i_muzzle
        j_muzzle_test = self.j + self.j_muzzle
        if self.check_muzzle(j_muzzle_test, i_muzzle_test):
            r_size = self.game.r_size
            x= i_muzzle_test * r_size
            y= j_muzzle_test * r_size

            self.game.c.coords(self.muzzle,(x+0.42*r_size,y+0.42*r_size,x+0.58*r_size,y+0.58*r_size))
            # self.i_muzzle, self.j_muzzle = 0,0
        self.update()
        
        self.game.root.after(self.dt, self.move)

    def check_movement(self, j_test, i_test):
        return (
            0 <= j_test < self.game.height
            and 0 <= i_test < self.game.width
            and not self.game.board.walls[j_test, i_test]
        )
    def check_muzzle(self, j_test, i_test):#just for beauty
        return self.check_movement(j_test, i_test)


class Board:
    def __init__(self, game):
        self.game = game
        # where we store SHAPES of canvas.
        self.board_rectangles = np.zeros((self.game.height, self.game.width))
        self.create_walls()

    def create_walls(self):
        self.walls = np.load("gamedata/walls.npy")

    # CODE POUR GENERER ALEATOIREMENT LA CARTE, NE PAS SUPPRIMER

    # def create_walls(self):
    #     self.walls = np.zeros((self.game.height, self.game.width))
    #     for i in range(170):
    #         x = random.randint(0, self.game.width - 1)
    #         y = random.randint(0, self.game.height - 1)
    #         self.walls[y, x] = True
    #     np.save("./gamedata/walls.npy", self.walls)

    def show_walls(self):
        r_size = self.game.r_size
        for j in range(self.game.height):
            for i in range(self.game.width):
                x, y = i * r_size, j * r_size
                self.board_rectangles[j, i] = self.game.c.create_rectangle(
                    x,
                    y,
                    x + r_size,
                    y + r_size,
                    fill="grey" if self.walls[j, i] else "white",
                )


def main():
    game = Game(30, 46)


if __name__ == "__main__":
    main()
