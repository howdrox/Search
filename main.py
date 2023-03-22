import tkinter as tk
import json
import numpy as np
import random
import time


class Game:
    def __init__(self, height, width):
        self.width = width
        self.height = height  # nbr de case
        self.r_size = 40  # pixel par case

        self.create_window()
        self.create_canvas()
        self.board = Board(self)
        self.board.show_walls()
        self.create_entities()
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
        self.persons = {
            'player': [Person(self, False, [1, 4])],
            'enemy': [Person(self, True, [6, 6])],
        }
        self.root.bind(
            "<KeyPress>", lambda e: self.persons['player'][0].speed_set(e.keysym))
        self.root.bind(
            "<KeyRelease>", lambda e: self.persons['player'][0].speed_cancel(e.keysym))


class Person:
    def __init__(self, game, evil, spawn_coord):
        self.game = game
        self.evil = evil
        self.j, self.i = spawn_coord
        self.speed=15 # cases per second
        self.speed_j=0
        self.speed_i=0
        self.show()
        self.move_control()

    def show(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.shape = self.game.c.create_rectangle(
            x, y, x + r_size, y + r_size, fill="red" if self.evil else "blue"
        )

    def update(self):
        r_size = self.game.r_size
        x, y = self.i * r_size, self.j * r_size
        self.game.c.moveto(self.shape, x - 1, y - 1)

    def speed_set(self, k):
        if k in ("Up", "w"):
            self.speed_i = 0
            self.speed_j = -1
        elif k in ("Left", "a"):
            self.speed_j = 0
            self.speed_i = -1
        elif k in ("Down", "s"):
            self.speed_i = 0
            self.speed_j = 1
        elif k in ("Right", "d"):
            self.speed_j = 0
            self.speed_i = 1

    def speed_cancel(self, k):
        if k in ("Up", "w", "Down", "s"):
            self.speed_j = 0
        elif k in ("Left", "a", "Right", "d"):
            self.speed_i = 0

    def move(self):
        i_test = self.i + self.speed_i
        j_test = self.j + self.speed_j
        if self.check_movement(j_test, i_test):
            self.i += self.speed_i
            self.j += self.speed_j
        self.update()

        self.game.root.after(int(1000/self.speed), self.move_control)

    def check_movement(self, j_test, i_test):
        return (
            0 <= j_test < self.game.height
            and 0 <= i_test < self.game.width
            and not self.game.board.walls[j_test, i_test]
        )

    def move_control(self):
        if self.evil:
            self.pathfinding()
        self.move()

    def pathfinding(self):
        self.speed_set(np.random.choice(['w','a','s','d']))


class Board:
    def __init__(self, game):
        self.game = game
        # where we store SHAPES of canvas.
        self.board_rectangles = np.zeros((self.game.height, self.game.width))
        self.create_walls()

    def create_walls(self):
        density=0.1 #density of  walls
        np.random.seed(2333)
        self.walls=np.random.choice([True,False],size=(self.game.height, self.game.width),p=(density,1-density))
        #self.walls = np.load("gamedata/walls.npy")
        np.save("./gamedata/walls", self.walls)

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
    game = Game(17, 35)


if __name__ == "__main__":
    main()
