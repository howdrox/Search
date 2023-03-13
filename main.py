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
    main()