<<<<<<< HEAD
import tkinter as tk
import json
import numpy as np

class Game:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.c_width = width * 50
        self.c_height = height * 50

        self.create_window()
        self.create_canvas()
        self.board=Board(self.c,self.height ,self.width)
        self.board.show_walls()
        self.create_entities()
        for p in self.persons:
            p.show()

        self.root.mainloop()

    def create_window(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.c_width + 20}x{self.c_height + 20}") 
        self.root.title("Search")

    def create_canvas(self):
        self.c = tk.Canvas(self.root, width=self.c_width, height=self.c_height)
        self.c.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


    def create_entities(self):
        self.persons = []
        self.persons.append(Person(self.c,False, [1, 3]))
        self.persons.append(Person(self.c,True, [6, 6]))
    
class Person:
    def __init__(self,canvas, evil, spawn_coord):
        self.c = canvas
        self.evil = evil
        self.coord = spawn_coord

    def show(self):
        self.shape = self.c.create_rectangle(self.coord[1] * 50, self.coord[0]  * 50, self.coord[1]  * 50 + 50, self.coord[0]  * 50 + 50, fill="blue")


class Board:
    def __init__(self, canvas, height, width):
        self.c = canvas
        self.width = width
        self.height = height
        self.board_rectangles = np.zeros((height, width))
        with open("./data.json", "r") as f:
            self.walls = np.array(json.load(f)["board"])
    
    def show_walls(self):
        """Shows walls on canvas"""
        for x in range(self.width):
            for y in range(self.height):
                if self.walls[y, x]:
                    self.board_rectangles[y, x] = self.c.create_rectangle(x * 50, y * 50, x * 50 + 50, y * 50 + 50, fill="grey")
                else:
                    self.board_rectangles[y, x] = self.c.create_rectangle(x * 50, y * 50, x * 50 + 50, y * 50 + 50, fill="white")
    

def main():
    game = Game(7, 9)

if __name__ == "__main__":
=======
import tkinter as tk
import json
import numpy as np
import random

class Game:
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.r_size = 40
        self.c_width = width * self.r_size
        self.c_height = height *  self.r_size

        self.create_window()
        self.create_canvas()
        self.board=Board(self.c,self.height ,self.width, self.r_size)
        self.board.show_walls()
        self.create_entities()
        for p in self.persons:
            p.show()
        
        self.root.bind("<Key>", self.movement)

        self.root.mainloop()

    def create_window(self):
        self.root = tk.Tk()
        self.root.geometry(f"{self.c_width + 20}x{self.c_height + 20}") 
        self.root.title("Search")

    def create_canvas(self):
        self.c = tk.Canvas(self.root, width=self.c_width, height=self.c_height)
        self.c.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


    def create_entities(self):
        self.persons = []
        self.persons.append(Person(self.c, False, [1, 4], self.r_size))
        self.persons.append(Person(self.c, True, [6, 6], self.r_size))
    
    def movement(self, event):
        k = event.keysym
        if (k == "Up" or k == "w") and self.check(self.persons[0].coord, "w"):
            self.persons[0].coord = [self.persons[0].coord[0] - 1, self.persons[0].coord[1]]
            self.c.move(self.persons[0].shape, 0, -self.r_size)
        elif (k == "Left" or k == "a") and self.check(self.persons[0].coord, "a"):
            self.persons[0].coord = [self.persons[0].coord[0], self.persons[0].coord[1] - 1]
            self.c.move(self.persons[0].shape, -self.r_size, 0)
        elif (k == "Down" or k == "s") and self.check(self.persons[0].coord, "s"):
            self.persons[0].coord = [self.persons[0].coord[0] + 1, self.persons[0].coord[1]]
            self.c.move(self.persons[0].shape, 0, self.r_size)
        elif (k == "Right" or k == "d") and self.check(self.persons[0].coord, "d"):
            self.persons[0].coord = [self.persons[0].coord[0], self.persons[0].coord[1] + 1]
            self.c.move(self.persons[0].shape, self.r_size, 0)
            
    
    def check(self, coord, k):
        result = True
        if k == "w" and (coord[0] == 0 or self.board.walls[coord[0] - 1, coord[1]]):
            result = False
        elif k == "a" and (coord[1] == 0 or self.board.walls[coord[0], coord[1] - 1]):
            result = False
        elif k == "s" and (coord[0] == self.height - 1 or self.board.walls[coord[0] + 1, coord[1]]):
            result = False
        elif k == "d" and (coord[1] == self.width - 1 or self.board.walls[coord[0], coord[1] + 1]):
            result = False
        return result
    
class Person:
    def __init__(self,canvas, evil, spawn_coord, r_size):
        self.c = canvas
        self.evil = evil
        self.coord = spawn_coord
        self.r_size = r_size

    def show(self):
        if not self.evil:
            self.shape = self.c.create_rectangle(self.coord[1] * self.r_size, self.coord[0]  * self.r_size, self.coord[1]  * self.r_size + self.r_size, self.coord[0]  * self.r_size + self.r_size, fill="blue")
        else:
            self.shape = self.c.create_rectangle(self.coord[1] * self.r_size, self.coord[0]  * self.r_size, self.coord[1]  * self.r_size + self.r_size, self.coord[0]  * self.r_size + self.r_size, fill="red")


class Board:
    def __init__(self, canvas, height, width, r_size):
        self.c = canvas
        self.width = width
        self.height = height
        self.r_size = r_size
        self.board_rectangles = np.zeros((height, width))
        self.create_walls()
    
    def create_walls(self):
        with open("./data.json", "r") as f:
            self.walls = np.array(json.load(f)["walls"])
    
    # def create_walls(self):
    #     self.walls = np.zeros((self.height, self.width))
    #     for i in range(56):
    #         x = random.randint(0, self.width-1)
    #         y = random.randint(0, self.height-1)
    #         self.walls[y, x] = True
    #     data = {"walls": self.walls.tolist()}
    #     with open("/mnt/insa/lkusno/Home_INSA/Informatique/Algo/A2/Search/data.json", "w") as f:
    #         json.dump(data, f)      

    def show_walls(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.walls[y, x] == 1.0:
                    self.board_rectangles[y, x] = self.c.create_rectangle(x * self.r_size, y * self.r_size, x * self.r_size + self.r_size, y * self.r_size + self.r_size, fill="grey")
                else:
                    self.board_rectangles[y, x] = self.c.create_rectangle(x * self.r_size, y * self.r_size, x * self.r_size + self.r_size, y * self.r_size + self.r_size, fill="white")
    

def main():
    game = Game(19, 23)

if __name__ == "__main__":
>>>>>>> 40ad5f79c8249653b34541b2fe49882e7b07985e
    main()