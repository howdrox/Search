import tkinter as tk
import json
import numpy as np
import random


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
        for p in self.persons:
            p.show()

        self.root.bind("<Key>", self.movement)

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
        self.persons.append(Person(self.c, False, [1, 4], self.r_size))
        self.persons.append(Person(self.c, True, [6, 6], self.r_size))

    def movement(self, event):
        k = event.keysym
        if (k == "Up" or k == "w") and self.check(self.persons[0].coord, "w"):
            self.persons[0].coord = [
                self.persons[0].coord[0] - 1, self.persons[0].coord[1]]
            self.c.move(self.persons[0].shape, 0, -self.r_size)
        elif (k == "Left" or k == "a") and self.check(self.persons[0].coord, "a"):
            self.persons[0].coord = [
                self.persons[0].coord[0], self.persons[0].coord[1] - 1]
            self.c.move(self.persons[0].shape, -self.r_size, 0)
        elif (k == "Down" or k == "s") and self.check(self.persons[0].coord, "s"):
            self.persons[0].coord = [
                self.persons[0].coord[0] + 1, self.persons[0].coord[1]]
            self.c.move(self.persons[0].shape, 0, self.r_size)
        elif (k == "Right" or k == "d") and self.check(self.persons[0].coord, "d"):
            self.persons[0].coord = [
                self.persons[0].coord[0], self.persons[0].coord[1] + 1]
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


class Person():
    def __init__(self, canvas, evil, spawn_coord, r_size):
        self.c = canvas
        self.evil = evil
        self.coord = spawn_coord
        self.r_size = r_size

    def show(self):
        self.shape = self.c.create_rectangle(self.coord[1] * self.r_size, self.coord[0] * self.r_size, self.coord[1]
                                             * self.r_size + self.r_size, self.coord[0] * self.r_size + self.r_size, fill="red" if self.evil else "blue")


class Board:
    def __init__(self, game):
        self.game = game
        # where we store SHAPES of canvas.
        self.board_rectangles = np.zeros((self.game.height, self.game.width))
        self.create_walls()

    def create_walls(self):
        with open("./data.json", "r") as f:
            self.walls = np.array(json.load(f)["walls"])

    # CODE POUR GENERER ALEATOIREMENT LA CARTE, NE PAS SUPPRIMER

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
        r_size = self.game.r_size
        for j in range(self.game.height):
            for i in range(self.game.width):
                x, y = i * r_size, j * r_size
                self.board_rectangles[j, i] = self.game.c.create_rectangle(
                    x, y, x + r_size, y + r_size, fill="grey" if self.walls[j, i] else "white")


def main():
    game = Game(19, 23)


if __name__ == "__main__":
    main()
